# Module 22 — Asyncio

**Time budget:** 5 hours lesson, 8 hours exercises
**Prerequisite:** Modules 14 (generators), 21

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

`asyncio` lets one thread handle tens of thousands of concurrent connections,
because a coroutine waiting on the network costs a few kilobytes while a thread
costs megabytes.

The mental model is Module 14's, exactly: **a coroutine is a suspended frame**.
`await` is `yield` with a scheduler attached. If you understood generators, you
already understand 80 percent of this.

---

## 1. The event loop

One thread, one loop, a queue of ready tasks.

```
loop:
    run each READY task until it awaits something
    ask the OS which of the awaited things are now ready   (epoll/kqueue)
    move those tasks back to READY
    repeat
```

There is no preemption. A task runs until **it** yields control by awaiting. That
single fact explains both asyncio's biggest advantage — no locks needed between
awaits, because nothing can interleave — and its biggest failure mode, below.

```python
import asyncio

async def main() -> None:
    await asyncio.sleep(1)
    print("done")

asyncio.run(main())          # creates a loop, runs main, closes the loop
```

---

## 2. Coroutines, awaitables, tasks

```python
async def fetch(url: str) -> str: ...

coro = fetch(url)            # NOTHING has run yet -- exactly like a generator
result = await coro          # runs it, suspending here until it completes
task = asyncio.create_task(coro)     # schedules it to run CONCURRENTLY
result = await task                   # waits for it
```

**Calling a coroutine function runs nothing.** It returns a coroutine object.
This is Module 14's "calling a generator function runs nothing", and forgetting
it produces the most common asyncio bug:

```python
fetch(url)                   # RuntimeWarning: coroutine was never awaited
await fetch(url)             # correct
```

**`await` does not create concurrency.** It waits. Concurrency comes from having
several tasks scheduled:

```python
# SEQUENTIAL: 3 seconds
a = await fetch(url1)
b = await fetch(url2)
c = await fetch(url3)

# CONCURRENT: 1 second
a, b, c = await asyncio.gather(fetch(url1), fetch(url2), fetch(url3))
```

That distinction is the second most common bug: code that is fully `async` and
entirely sequential.

---

## 3. `TaskGroup` over `gather`

```python
async with asyncio.TaskGroup() as tg:          # 3.11+
    t1 = tg.create_task(fetch(url1))
    t2 = tg.create_task(fetch(url2))
results = [t1.result(), t2.result()]
```

`TaskGroup` is **structured concurrency**: no task outlives the block, and if
one fails the others are cancelled and the errors arrive as an `ExceptionGroup`
(Module 16). `gather` does neither by default — a failure leaves the siblings
running, orphaned, with nobody to collect them.

```python
results = await asyncio.gather(*coros, return_exceptions=True)
# without return_exceptions, the FIRST exception propagates and the rest
# keep running, unobserved -- "Task exception was never retrieved" at exit
```

**Use `TaskGroup` for new code.** Use `gather` when you specifically want
results in order and are handling failures deliberately.

---

## 4. The number one asyncio bug: blocking the loop

```python
async def handler() -> Response:
    data = requests.get(url)          # BLOCKS. Nothing else runs. At all.
    time.sleep(1)                      # BLOCKS.
    result = heavy_computation()       # BLOCKS.
```

There is no preemption, so a blocking call in one coroutine freezes **every**
connection the process is serving. A 200 ms blocking call in a service handling
1,000 concurrent requests adds 200 ms to all of them.

```python
async def handler() -> Response:
    async with httpx.AsyncClient() as client:
        data = await client.get(url)              # async library
    await asyncio.sleep(1)                         # async sleep
    result = await asyncio.to_thread(heavy_cpu)    # 3.9+: offload to a thread
```

**Every library in an async path must be async.** `requests`, `psycopg2`, the
`sqlite3` module, `time.sleep`, `open()` — all blocking. Their async
counterparts are `httpx`/`aiohttp`, `asyncpg`, `aiosqlite`, `asyncio.sleep`,
`aiofiles`.

Detect it with the loop's debug mode:

```python
asyncio.run(main(), debug=True)      # warns about callbacks over 100 ms
```

---

## 5. Cancellation and timeouts

```python
async with asyncio.timeout(5.0):        # 3.11+
    await slow_operation()               # raises TimeoutError

result = await asyncio.wait_for(slow_operation(), timeout=5.0)
```

Cancellation works by **raising `CancelledError` inside the coroutine at its
current `await`**. Two consequences:

```python
try:
    await something()
except asyncio.CancelledError:
    await cleanup()          # cleanup is fine
    raise                    # but you MUST re-raise
```

Swallowing `CancelledError` makes a task uncancellable, and `TaskGroup` and
timeouts stop working for it. Note it inherits from `BaseException` (not
`Exception`) since 3.8, precisely so `except Exception` does not eat it —
the same design reasoning as `KeyboardInterrupt` in Module 16.

**Cancellation only happens at an `await`.** A coroutine in a tight
non-awaiting loop cannot be cancelled at all.

---

## 6. Async iteration and context managers

```python
async for record in cursor:                  # __aiter__ / __anext__
    ...

async with session.begin():                  # __aenter__ / __aexit__
    ...

async def stream(url: str) -> AsyncIterator[bytes]:
    async with client.stream("GET", url) as response:
        async for chunk in response.aiter_bytes():
            yield chunk                       # an async generator
```

Everything from Module 09 and Module 14, with `a` prefixes and `await`s.

---

## 7. Bridging sync and async

```python
await asyncio.to_thread(blocking_fn, arg)                 # 3.9+, easiest
await loop.run_in_executor(pool, blocking_fn, arg)        # explicit pool
await loop.run_in_executor(process_pool, cpu_heavy, arg)  # CPU work
```

From sync code into async: `asyncio.run(coro)` — but only once, at the top. You
cannot call it from inside a running loop, and `asyncio.run` inside a request
handler is a common and confusing error.

---

## 8. Choosing: async, threads, or processes

| | asyncio | threads | processes |
|---|---|---|---|
| Concurrency limit | ~100,000 | ~hundreds | ~CPU count |
| Memory per unit | a few KB | ~8 MB stack | a full interpreter |
| CPU parallelism | no | no (pure Python) | **yes** |
| Blocking calls | **poison the loop** | fine | fine |
| Ecosystem | needs async libraries | any library | any library |
| Debugging | harder | hard | hardest |
| Rewrite cost | **whole call stack** | none | none |

**The async colour problem is the real cost.** An `async` function can only be
awaited by another `async` function, so making one function async makes its
entire call chain async. Introducing asyncio into an existing sync codebase is
not a local change.

**Rule of thumb:** hundreds of concurrent I/O operations, or a framework that is
already async (FastAPI) → asyncio. A few dozen blocking calls in otherwise sync
code → threads. CPU work → processes.

---

## Common mistakes in this module

| Mistake | Symptom | Fix |
|---|---|---|
| Forgetting `await` | `RuntimeWarning: never awaited`, nothing happens | `await` it |
| Sequential `await`s | Async code with no concurrency | `gather` / `TaskGroup` |
| A blocking call in a coroutine | **The whole service freezes** | Async library, or `to_thread` |
| `time.sleep` in async | Same | `asyncio.sleep` |
| Swallowing `CancelledError` | Uncancellable tasks, hanging timeouts | Re-raise |
| `gather` without `return_exceptions` | Siblings orphaned on first failure | `TaskGroup` |
| Not keeping a reference to a task | Task garbage collected mid-flight | Keep it, or use `TaskGroup` |
| `asyncio.run` inside a running loop | `RuntimeError` | `await` instead |
| No timeout | A hung connection blocks forever | `asyncio.timeout` |
| Shared mutable state across `await` | Races — yes, even single-threaded | Nothing is atomic *across* an await |

That last one surprises people: asyncio is single-threaded, but a coroutine can
be suspended at any `await`, so a read-modify-write spanning an `await` has
exactly the race from Module 21.

---

## Self-check quiz

1. Describe the event loop in four lines.
2. What does calling a coroutine function do?
3. Why is `await a(); await b()` not concurrent, and what makes it so?
4. Give two things `TaskGroup` does that `gather` does not.
5. Why does one blocking call freeze every connection?
6. How does cancellation work, and why must you re-raise `CancelledError`?
7. Why does `CancelledError` inherit from `BaseException`?
8. When can a coroutine *not* be cancelled?
9. What is the "colour problem" and why does it make adoption expensive?
10. Can single-threaded async code have a race condition? Explain.

---

## Exercises

1. **[`ex01_basics.py`](exercises/ex01_basics.py)** — Twelve predictions about
   ordering, concurrency and timing.
2. **[`ex02_blocking.py`](exercises/ex02_blocking.py)** — Find and fix five
   blocking calls in an async service. Measure the latency impact of each.
3. **[`ex03_scraper.py`](exercises/ex03_scraper.py)** — A concurrent fetcher
   with a semaphore, timeouts, retries, and graceful shutdown.
4. **[`ex04_cancellation.py`](exercises/ex04_cancellation.py)** — Six
   cancellation puzzles, including two that hang.

---

## Going deeper

- [`asyncio`](https://docs.python.org/3/library/asyncio.html) — start with "Coroutines and Tasks"
- [PEP 3156](https://peps.python.org/pep-3156/) (asyncio's design) and [PEP 654](https://peps.python.org/pep-0654/) (ExceptionGroup)
- Nathaniel Smith, "Notes on structured concurrency" — why `TaskGroup` exists
- `trio` and `anyio` — a cleaner take on the same problem; `anyio` runs on both

---

**Next:** [Module 23 — Performance and Profiling](../23-performance-and-profiling/README.md)
