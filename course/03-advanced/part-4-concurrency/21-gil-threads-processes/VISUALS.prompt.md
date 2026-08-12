# NotebookLM Visual Prompts — Module 21: The GIL, Threads, and Processes

---

## Sources to add

| Source | Type |
|---|---|
| `21-gil-threads-processes/README.md` | Upload |
| `02-objects-names-data-model/README.md` (refcounting) | Upload |
| https://docs.python.org/3/library/concurrent.futures.html | Website |
| https://peps.python.org/pep-0703/ | Website |
| https://docs.python.org/3/library/multiprocessing.html | Website |

---

## 1. Cinematic Video Overview

**Format:** Explanation
**Visual style:** Custom, with this description:

```
Clean technical schematic on a dark background. Threads drawn as horizontal
lanes on a timeline. The GIL drawn as a single physical TOKEN that a lane must
be holding to execute, passed between lanes and visibly dropped during I/O.
Processes drawn as separate walled regions, each with its own token. Monospace
type for all code. No characters, no mascots.
```

**Steering prompt (paste this whole block):**

```
Audience: a programmer who has heard "Python can't do threads because of the
GIL", believes it, and has therefore either avoided concurrency entirely or
reached for multiprocessing where threads would have been correct.

Thesis: the GIL prevents exactly one thing -- two threads executing Python
BYTECODE simultaneously. It is released during I/O and inside many C
extensions. Knowing the precise boundary is what lets you choose correctly
between threads, processes and async.

1. THE TOKEN. Draw four thread lanes and one token. A lane can only execute
   while holding it. Animate a pure-Python loop across four threads: the token
   passes round every 5 milliseconds, each lane runs a fraction of the time,
   and total throughput is NO BETTER than one thread -- in fact slightly worse,
   because passing the token costs something. Put a wall-clock bar beside it
   showing serial versus threaded, and show them equal.

2. THE TOKEN BEING DROPPED. Now the same four lanes doing an HTTP request. Show
   each lane grabbing the token, issuing the request, and DROPPING THE TOKEN
   while it waits. Show all four waiting simultaneously with the token idle.
   Then the wall-clock bar: four requests in the time of one. This is the frame
   that corrects the misconception, and it should be the most memorable image
   in the video.

3. THE THIRD CASE. A NumPy operation on a large array. Show the lane entering C
   code and RELEASING the token for the duration, so several lanes compute in
   parallel while all inside C. State the rule that follows: threads are right
   for I/O and for C extensions that release the GIL, and wrong only for pure
   Python CPU work.

4. WHY IT EXISTS. Reuse Module 02's refcount picture. Show two threads
   incrementing the same object's refcount simultaneously with no lock, and one
   increment being lost -- leading to a premature free and a crash. Then show
   the GIL making that impossible with a single lock instead of a lock per
   object. Say plainly: it is a trade that makes single-threaded code fast and C
   extensions simple, and it has been attempted to remove since 1999.

5. THE RACE. Animate `counter += 1` decomposing into LOAD, ADD, STORE. Show two
   lanes interleaving between the LOAD and the STORE, both reading 41, both
   writing 42, and one increment vanishing. Then run it 100,000 times and show
   the final count short by a few thousand. Then add the lock and show it
   correct. Emphasise that the GIL does NOT save you here -- a switch can occur
   between any two bytecodes.

6. PROCESSES. Draw two walled regions, each with its own token and its own
   memory. Show true parallel execution on the wall-clock bar. Then show the
   cost: an object being PICKLED to cross the wall, and three things bouncing
   off it -- a lambda, an open file handle, a database connection. Then show
   spawn re-importing the module in the child, and without a __main__ guard,
   the child spawning its own children: a process bomb, drawn as it happens.

7. THE DECISION TABLE, EARNED. Having shown all three mechanisms, present the
   workload-to-tool table as a conclusion rather than a premise. Then show the
   most common mistake concretely: multiprocessing applied to an I/O workload,
   with the pickling and process startup costing MORE than the parallelism
   saves, and the bar coming out slower than threads.

8. FREE-THREADED PYTHON. Close by showing the 3.13 no-GIL build: four lanes,
   four tokens, real parallelism for pure Python. Then the honest caveats --
   single-threaded code currently slower, C extensions needing updates, not the
   default. And the point that matters: the DECISION FRAMEWORK does not change,
   because it is about the nature of the work, not the interpreter.

Do not cover: asyncio in detail (Module 22) or profiling (Module 23).
```

---

## 2. Mind Map

**Prompt:**

```
Build a mind map titled "Concurrency in Python".

Branch 1 "The GIL": what it locks, the three situations it is released, why it
exists (refcounting), the switch interval, and PEP 703.

Branch 2 "Choosing": a workload-to-tool table -- network I/O, disk I/O, pure
Python CPU, NumPy/C-extension CPU, thousands of connections, a few dozen
blocking calls -- each with the reason.

Branch 3 "Threads": Thread, start/join, the primitives (Lock, RLock, Event,
Condition, Semaphore, Barrier, local, Queue), and what each is for.

Branch 4 "Races": why += is not atomic, what IS atomic and why that is an
implementation detail, deadlock and the two rules that prevent it, and
"don't share state" as the real answer.

Branch 5 "Processes": separate memory and GILs, pickling as the boundary, what
cannot cross it, fork vs spawn, the __main__ guard, and shared_memory.

Branch 6 "concurrent.futures": ThreadPoolExecutor vs ProcessPoolExecutor, map
vs as_completed, exceptions stored in futures, and choosing max_workers.

Branch 7 "Costs": thread stack size, process startup, pickling, context
switching, and lock contention.
```

---

## 3. Study Guide, Quiz, and Flashcards

**Study Guide prompt:**

```
Produce a study guide for someone about to make a slow program faster with
concurrency.

Include a decision procedure: a short series of questions (is it waiting or
computing? if computing, is the work in Python or in a C extension? how many
concurrent operations? is the data large?) leading to threads, processes, or
async, with the reasoning at each branch.

Include a race-condition catalogue: check-then-act, read-modify-write, lazy
initialisation, iteration during mutation, and compound operations on shared
containers. For each: the code that looks fine, why it is not, and the fix.

Include a deadlock section: the four conditions required, the two practical
rules that break them, and how to diagnose one in a running process.

Include a multiprocessing gotcha list: what cannot be pickled, fork vs spawn
differences, the __main__ guard, module-level side effects re-running, and
sharing large arrays.

End with five slow programs described by their workload, each with the correct
tool and the expected speedup.
```

**Quiz prompt:**

```
Generate 16 questions.

At least six give a workload and ask which tool and what speedup to expect.
Include one where the answer is "none of them -- fix the algorithm first".

At least four are race conditions: given code, does it have one, under what
interleaving, and how often would it show up in testing.

Include: threads on a pure-Python loop, threads on a NumPy operation,
multiprocessing on an I/O workload, a ThreadPoolExecutor whose results are
never consumed, a spawn-based pool with no __main__ guard, and two threads
acquiring two locks in opposite orders.

For each answer, say what the GIL is or is not doing.
```

**Flashcards prompt:**

```
20 flashcards. Front: a term or scenario. Back: the precise answer.

Include: GIL, switch interval, when the GIL is released, why the GIL exists,
atomic operation, race condition, read-modify-write, Lock vs RLock, Event,
Condition, Semaphore, queue.Queue, deadlock, lock ordering, fork vs spawn,
pickling boundary, __main__ guard, shared_memory, ThreadPoolExecutor,
ProcessPoolExecutor, as_completed, future.result(), PEP 703.
```

---

## The specific visuals to insist on

1. **One token, four lanes, no speedup** for pure-Python CPU work.
2. **The token dropped during I/O**, four requests overlapping, four times the
   throughput. The single most important frame.
3. **A lane inside C code with the token released**, several computing at once.
4. **Two threads losing a refcount increment**, then the GIL preventing it.
5. **`counter += 1` decomposed**, with two lanes interleaving and an increment
   vanishing.
6. **An object pickled across a process wall**, and a lambda, a file handle and a
   DB connection bouncing off.
7. **The process bomb** from a missing `__main__` guard under spawn.
8. **Multiprocessing losing to threads on an I/O workload**, with the pickling
   and startup costs itemised.

---

## Analogies that work

- **A single microphone in a meeting room.** Only the person holding it can
  speak (execute bytecode). Everyone can *listen, think and wait for a phone
  call* without it — which is why waiting parallelises and talking does not.
- **A shared whiteboard** for the race: two people read "41", both write "42",
  and one update is lost. The board was never locked between reading and
  writing.
- **Posting a parcel to another building** for processes: it works, but
  everything must fit in a box, and some things (a running tap, a lit fire) do
  not.

## Analogies to refuse

- **"The GIL means Python is single-threaded."** It is not; it runs many
  threads, and they genuinely overlap during I/O. This phrasing is the
  misconception the module exists to correct.
- **"Use multiprocessing when you need speed."** Speed depends on the workload.
  For I/O, multiprocessing is *slower* than threads.
- **"The GIL makes your code thread-safe."** It does not. It makes individual
  bytecodes atomic; nearly every interesting operation is several bytecodes.

---

## Accuracy guardrails

```
Accuracy requirements:
- The GIL prevents concurrent execution of PYTHON BYTECODE. It is released
  during blocking I/O and by C extensions that choose to release it. State the
  boundary precisely every time.
- The GIL is a CPython implementation detail. Jython and IronPython have none;
  PyPy has one; the 3.13 free-threaded build makes it optional.
- The default switch interval is 5 ms and is configurable. It is not a
  guarantee about scheduling.
- `counter += 1` is NOT atomic; it is LOAD, ADD, STORE. list.append and
  dict assignment ARE effectively atomic under CPython, but that is a GIL side
  effect and not a language guarantee.
- multiprocessing pickles arguments and results. Lambdas, closures, open files,
  sockets, locks and DB connections cannot cross.
- spawn re-imports the module in the child; fork does not. spawn is the default
  on macOS and Windows, and is becoming the default on Linux. The __main__
  guard is mandatory under spawn.
- Exceptions in a concurrent.futures worker are stored in the Future and
  re-raised on .result(). Never calling .result() discards them silently.
- Threads have real memory cost (a stack per thread, commonly ~8 MB of virtual
  address space) -- which is why asyncio wins at thousands of connections.
- Do not claim free-threaded Python is production-default. It is an optional
  build with real caveats as of 3.13.
```

---

## After watching, you should be able to

- [ ] State exactly what the GIL prevents, in one sentence, without
      overstating.
- [ ] Name three situations where it is released.
- [ ] Choose between threads, processes and async for five given workloads.
- [ ] Explain why `counter += 1` races despite the GIL.
- [ ] Say what can and cannot cross a process boundary.
- [ ] Explain why a missing `__main__` guard under spawn is catastrophic.
- [ ] Say what happens to an exception in a pool worker whose result is never
      read.
- [ ] Give the two rules that prevent almost all deadlocks.
