# Module 21 — The GIL, Threads, and Processes

**Time budget:** 5 hours lesson, 7 hours exercises
**Prerequisite:** Part 3 complete

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

"Python can't do threads because of the GIL" is the most repeated and least
accurate thing said about the language. The truth is narrower and more useful:

> The GIL prevents **two threads from executing Python bytecode at the same
> time**. It does not prevent concurrency, it does not affect I/O, and it does
> not apply to code that releases it — which includes most of NumPy, most
> compression and hashing, and every blocking system call.

Getting this precise lets you choose correctly between threads, processes and
async, which is the single highest-leverage performance decision you will make.

---

## 1. What the GIL actually is

A single mutex in the CPython interpreter. A thread must hold it to execute
bytecode. It is released:

- every 5 milliseconds by default (`sys.setswitchinterval`), so other threads
  get a turn;
- around **every blocking I/O call** — file reads, socket operations, `sleep`;
- inside C extensions that explicitly release it (NumPy's array operations,
  `hashlib`, `zlib`, `lxml`, database drivers).

So the accurate statement is: **CPython cannot run pure-Python CPU work in
parallel across threads.** Everything else is available.

```python
import sys
sys.getswitchinterval()          # 0.005
```

**Why it exists:** it makes reference counting (Module 02) safe without a lock
on every object, which makes single-threaded code fast and C extensions simple
to write. Removing it has been attempted repeatedly since 1999; every previous
attempt made single-threaded code substantially slower.

**PEP 703 and free-threading.** Python 3.13 ships an optional build
(`python3.13t`) with no GIL, using biased reference counting and per-object
locks. It is real and it works. The caveats: single-threaded code is currently
somewhat slower, most C extensions need updating, and it is not the default. By
3.15 or so this section may need rewriting — but the *decision framework* below
does not change, because it is about the nature of the work, not the
interpreter.

---

## 2. The decision, first

| Workload | Use | Why |
|---|---|---|
| Waiting on network, disk, database | **threads** or **asyncio** | The GIL is released while waiting |
| Pure-Python CPU work | **processes** | Threads cannot run it in parallel |
| NumPy / pandas / hashing / compression | **threads** | Those libraries release the GIL |
| Thousands of concurrent connections | **asyncio** | Threads cost ~8 MB of stack each |
| A few dozen blocking calls | **threads** | Simpler; no async rewrite needed |
| Mixed CPU and I/O | **processes** with async or threads inside | |

**Measure before choosing.** The most common mistake is reaching for
`multiprocessing` for an I/O-bound workload, where it adds process overhead and
serialization cost for no benefit at all.

---

## 3. Threads

```python
from threading import Thread, Lock, RLock, Event, Condition, Semaphore, local
import queue

def worker(n: int, results: list[int]) -> None:
    results.append(n * 2)

threads = [Thread(target=worker, args=(i, results)) for i in range(4)]
for t in threads: t.start()
for t in threads: t.join()          # ALWAYS join, or the program may exit first
```

Prefer `concurrent.futures` (section 5) to raw threads for almost everything.

### Race conditions

```python
counter = 0

def increment() -> None:
    global counter
    for _ in range(100_000):
        counter += 1          # NOT atomic: LOAD, ADD, STORE
```

Run this on eight threads and the result is not 800,000. `counter += 1` is
three bytecode operations (Module 24 shows them), and a thread switch between
the LOAD and the STORE loses an increment.

**What is atomic in CPython?** A single bytecode operation. `list.append`,
`dict[k] = v`, and `x = y` are atomic *as a consequence of the GIL* — an
implementation detail you should not build on. Anything that reads then writes
is not.

```python
lock = Lock()

def increment() -> None:
    global counter
    for _ in range(100_000):
        with lock:                 # always `with`, never acquire/release
            counter += 1
```

### The primitives

| Primitive | For |
|---|---|
| `Lock` | Mutual exclusion. Cannot be re-acquired by the same thread. |
| `RLock` | Re-entrant: the same thread may acquire it repeatedly |
| `Event` | One-shot signalling: "the thing has happened" |
| `Condition` | Wait for a predicate to become true |
| `Semaphore` | Limit concurrency to N |
| `Barrier` | Wait until N threads arrive |
| `local()` | Per-thread storage |
| `queue.Queue` | **A thread-safe queue. Use this instead of shared state.** |

**The best concurrency primitive is not sharing state at all.** A `queue.Queue`
between a producer and consumers eliminates the entire class of race condition,
because only the queue is shared and it is already correct.

### Deadlock

```python
# thread 1: with lock_a: with lock_b: ...
# thread 2: with lock_b: with lock_a: ...      -> deadlock
```

Two rules that prevent essentially all of it: **acquire locks in a consistent
global order**, and **use `timeout=` so a deadlock becomes an error rather than
a hang**.

---

## 4. Processes

```python
from multiprocessing import Process, Pool, Queue, Value, Array, shared_memory

with Pool(processes=4) as pool:
    results = pool.map(cpu_heavy, items)
```

Separate memory, separate interpreters, separate GILs — so true parallelism, at
a price:

- **Everything crossing the boundary is pickled** (Module 19). Lambdas, closures,
  open files, locks and database connections cannot be sent.
- **Startup costs milliseconds.** `fork` is fast; `spawn` (the default on macOS
  and Windows, and on Linux from 3.14) re-imports your module in the child.
- **Under `spawn`, module-level code runs again in every child.** Without an
  `if __name__ == "__main__":` guard (Module 01), you get a process bomb.

```python
if __name__ == "__main__":          # MANDATORY with spawn
    with Pool() as pool: ...
```

For large data, `multiprocessing.shared_memory` avoids the copy entirely — and
is what `numpy` users reach for when the array is bigger than the pickle budget.

---

## 5. `concurrent.futures`: use this

One API, two backends, and swapping between them is one word.

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

with ThreadPoolExecutor(max_workers=8) as ex:        # I/O bound
    futures = {ex.submit(fetch, url): url for url in urls}
    for future in as_completed(futures):
        url = futures[future]
        try:
            data = future.result()          # re-raises the worker's exception
        except Exception:
            logger.exception("failed: %s", url)

with ProcessPoolExecutor() as ex:                    # CPU bound
    results = list(ex.map(cpu_heavy, items))
```

Three things worth knowing:

**`executor.map` returns results in order and re-raises on iteration;
`as_completed` yields futures as they finish.** Use `map` when you want the
results in order, `as_completed` when you want to handle each as it arrives.

**Exceptions are stored in the future**, not raised in the worker. If you never
call `.result()`, the exception disappears silently — the most common
`concurrent.futures` bug.

**`max_workers` defaults** to `min(32, cpu_count + 4)` for threads and
`cpu_count` for processes. For I/O-bound work the right number is usually far
higher than the CPU count and is found by measuring.

---

## Common mistakes in this module

| Mistake | Symptom | Fix |
|---|---|---|
| Threads for pure-Python CPU work | No speedup, sometimes slower | Processes |
| Processes for I/O work | Slower than threads, high memory | Threads or asyncio |
| `x += 1` without a lock | Lost updates, only under load | `Lock`, or `queue` |
| Never calling `.result()` | Exceptions vanish silently | Always consume results |
| No `__main__` guard with spawn | Process bomb | Add it |
| Inconsistent lock order | Deadlock under load | One global order, plus timeouts |
| Sharing mutable state | Races that appear in production only | Pass messages via a queue |
| Not joining threads | Program exits with work in flight | `join()`, or an executor's `with` |
| A lock held across I/O | Serialised throughput | Hold locks for as few lines as possible |
| Assuming `list.append` is contractually atomic | Breaks on other implementations | It is a GIL side effect |

---

## Self-check quiz

1. State precisely what the GIL prevents and what it does not.
2. Name three situations in which the GIL is released.
3. Why does the GIL exist? What has removing it historically cost?
4. Why is `counter += 1` not atomic?
5. When are threads the right answer for CPU-bound work?
6. What must be true of an object for it to cross a process boundary?
7. Why does `spawn` require `if __name__ == "__main__":`?
8. What happens to an exception raised inside a `ThreadPoolExecutor` worker?
9. Give two rules that prevent almost all deadlocks.
10. Why is a `Queue` better than a shared list plus a lock?

---

## Exercises

1. **[`ex01_gil_lab.py`](exercises/ex01_gil_lab.py)** — Measure four workloads
   under threads, processes and serial execution. Predict each first.
2. **[`ex02_races.py`](exercises/ex02_races.py)** — Six race conditions.
   Reproduce each reliably, then fix it.
3. **[`ex03_pipeline.py`](exercises/ex03_pipeline.py)** — A producer/consumer
   pipeline with queues, graceful shutdown, and backpressure.
4. **[`ex04_pool.py`](exercises/ex04_pool.py)** — Parallelise a real workload
   and find the point where more workers stop helping.

---

## Going deeper

- [`threading`](https://docs.python.org/3/library/threading.html), [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html), [`concurrent.futures`](https://docs.python.org/3/library/concurrent.futures.html)
- [PEP 703 — Making the GIL optional](https://peps.python.org/pep-0703/)
- David Beazley, "Understanding the Python GIL" — the definitive 40-minute talk
- Raymond Hettinger, "Thinking about Concurrency"

---

**Next:** [Module 22 — Asyncio](../22-asyncio/README.md)
