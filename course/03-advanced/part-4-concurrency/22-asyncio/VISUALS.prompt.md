# NotebookLM Visual Prompts — Module 22: Asyncio

---

## Sources to add

| Source | Type |
|---|---|
| `22-asyncio/README.md` | Upload |
| `14-iterators-and-generators/README.md` (suspended frames) | Upload |
| `21-gil-threads-processes/README.md` | Upload |
| https://docs.python.org/3/library/asyncio-task.html | Website |
| https://peps.python.org/pep-0654/ | Website |

---

## 1. Cinematic Video Overview

**Format:** Explanation
**Visual style:** Custom, with this description:

```
Clean technical schematic on a dark background. The event loop drawn as a
single worker at a desk with a QUEUE of task cards beside it. A task waiting on
I/O drawn as a card moved to a separate PARKED area, not occupying the desk.
Suspended coroutine frames drawn exactly as in Module 14 -- greyed but intact,
with a marker resting on the await line. Monospace type for code. No characters
beyond the single abstract worker, no mascots.
```

**Steering prompt (paste this whole block):**

```
Audience: a programmer who has written async/await in another language or
copied it in Python, and does not know what the event loop is doing. They have
probably written a fully-async function that runs entirely sequentially.

Thesis: a coroutine is a suspended frame -- the same object from Module 14 --
with a scheduler deciding when to resume it. One worker, many parked tasks. All
of asyncio's power and all of its failure modes come from there being NO
PREEMPTION.

1. THE BRIDGE FROM GENERATORS. Open by replaying Module 14's suspended frame:
   locals intact, marker on the yield line. Then relabel `yield` as `await` and
   add a scheduler beside it. Say directly: you already know this. An awaiting
   coroutine is a paused frame; asyncio is the thing that decides which paused
   frame to resume next.

2. THE LOOP. One worker at a desk, a queue of ready cards, and a parked area.
   Animate the cycle: take a card, run it until it awaits, MOVE IT TO PARKED,
   take the next card. Then the loop asks the OS which parked things are ready
   and moves those cards back to the queue. Run it with five tasks so the
   viewer sees the desk never idle while any card is runnable.

3. AWAIT DOES NOT CREATE CONCURRENCY. The single most valuable correction in
   the module. Show three sequential awaits: card 1 parks, and the DESK SITS
   IDLE because no other card exists yet -- three seconds. Then show
   gather/TaskGroup creating three cards up front: card 1 parks, the worker
   immediately picks up card 2, then card 3, all three park, and all three
   complete together -- one second. Put both wall clocks on screen.
   State it plainly: await means WAIT. Concurrency comes from having other
   tasks scheduled.

4. THE BLOCKING CALL. Give this the most time; it is the failure that takes
   services down. Show 1,000 parked cards and one card on the desk making a
   blocking requests.get(). Freeze the entire scene -- the worker cannot move,
   the parked cards cannot be resumed, the queue cannot advance. Add a latency
   meter for all 1,000 connections climbing together by the duration of that one
   call. Then swap in an async client and show the card parking properly while
   everything else proceeds. Then show asyncio.to_thread as the escape hatch for
   code you cannot make async, with the blocking work moved off the desk
   entirely.

5. STRUCTURED CONCURRENCY. Show gather with three tasks where one fails: the
   exception propagates to the caller while the other two KEEP RUNNING,
   orphaned, with nobody to collect them -- and later, at interpreter exit,
   "Task exception was never retrieved". Then show TaskGroup: one failure
   cancels the siblings, nothing outlives the block, and the errors arrive
   together as an ExceptionGroup. Draw the TaskGroup as a physical boundary no
   card can cross.

6. CANCELLATION. Show CancelledError being raised INSIDE a coroutine at its
   current await -- not at an arbitrary point, at the await. Then two failure
   modes: a coroutine that catches it and does not re-raise, becoming
   uncancellable while a timeout waits forever; and a coroutine in a tight loop
   with no await at all, which cannot be cancelled because there is no point at
   which to deliver the exception.

7. THE RACE THAT SURPRISES EVERYONE. Single-threaded, no GIL involved. Show a
   read-modify-write spanning an await: task A reads the value, awaits, task B
   reads the same value and writes, task A resumes and writes a stale value.
   Reuse Module 21's lost-update animation exactly. The lesson: nothing is
   atomic ACROSS an await, and single-threaded does not mean race-free.

8. CHOOSING. Close with the three-way comparison from Module 21, now including
   async: memory per unit, concurrency ceiling, CPU parallelism, and the colour
   problem -- one function becoming async forcing its whole call chain to
   follow. Show that spreading as a stain up a call graph, because it is the
   real cost of adoption and nobody mentions it.
```

---

## 2. Mind Map

**Prompt:**

```
Build a mind map titled "Asyncio".

Branch 1 "The loop": ready queue, parked tasks, no preemption, one thread,
asyncio.run, and the OS readiness call (epoll/kqueue).

Branch 2 "Coroutines": calling one runs nothing, await waits, create_task
schedules, the relationship to generators, and async generators.

Branch 3 "Concurrency": gather, TaskGroup, structured concurrency, what happens
to siblings on failure, return_exceptions, and keeping references to tasks.

Branch 4 "Blocking": what blocks (requests, time.sleep, open, psycopg2, CPU
work), what that does to every other connection, the async replacements, and
to_thread / run_in_executor.

Branch 5 "Cancellation and timeouts": CancelledError as BaseException, delivery
at the await point, re-raising, asyncio.timeout, wait_for, and shielding.

Branch 6 "Async protocols": async for, async with, __aiter__/__anext__,
__aenter__/__aexit__, async generators.

Branch 7 "Choosing": async vs threads vs processes across memory, ceiling, CPU,
ecosystem and rewrite cost -- including the colour problem.

Branch 8 "Races in single-threaded code": nothing is atomic across an await,
asyncio.Lock, and when you still need one.
```

---

## 3. Study Guide, Quiz, and Flashcards

**Study Guide prompt:**

```
Produce a study guide for someone debugging a slow or hanging async service.

Include a "why is my async code slow" diagnosis table: sequential awaits, a
blocking call, no concurrency limit causing resource exhaustion, an
unawaited coroutine, CPU work on the loop, and a missing connection pool. For
each: the symptom, how to confirm it, and the fix.

Include a blocking-call inventory: for fifteen common libraries and functions
(requests, httpx sync, time.sleep, open, psycopg2, sqlite3, boto3, subprocess,
hashlib on large input, json.dumps on large input, PIL operations), whether it
blocks and what to use instead.

Include a cancellation guide: what raises CancelledError, where it is
delivered, what must re-raise it, when to use shield, and how to write cleanup
that runs on cancellation.

Include a decision guide for async vs threads vs processes with the colour
problem stated as an explicit cost.

End with five async functions that look correct and are not, each with the bug
and the fix.
```

**Quiz prompt:**

```
Generate 16 questions.

At least five must be timing questions: given async code, how long does it take
and why. Include sequential awaits, gather, a TaskGroup with a failure, a
blocking sleep among async sleeps, and a semaphore-limited batch.

At least three on cancellation: a coroutine swallowing CancelledError, a tight
loop with no await, and a cleanup that must run.

Include: a coroutine called without await, gather where one task raises,
a task created without keeping a reference, asyncio.run called inside a running
loop, and a read-modify-write across an await.

For each answer, describe what the event loop is doing at each step -- which
task is on the desk and which are parked.
```

**Flashcards prompt:**

```
20 flashcards. Front: a term or fragment. Back: meaning and the trap.

Include: event loop, coroutine object, await, create_task, gather, TaskGroup,
structured concurrency, ExceptionGroup, CancelledError, asyncio.timeout,
wait_for, shield, to_thread, run_in_executor, async for, async with, async
generator, blocking the loop, asyncio.Lock, the colour problem, debug mode.
```

---

## The specific visuals to insist on

1. **The Module 14 suspended frame, relabelled** from `yield` to `await` with a
   scheduler attached.
2. **The desk, the ready queue, and the parked area**, cycling.
3. **Three sequential awaits with an idle desk (3s), versus gather (1s)**, both
   wall clocks visible. The most valuable correction in the module.
4. **1,000 parked cards frozen by one blocking call**, with a latency meter
   climbing for all of them.
5. **`gather` orphaning siblings on failure**, versus `TaskGroup` as a boundary
   nothing escapes.
6. **`CancelledError` delivered at the await point**, and a tight loop that
   cannot receive it.
7. **A read-modify-write across an await losing an update**, single-threaded.
8. **The async colour spreading up a call graph.**

---

## Analogies that work

- **A single receptionist with a waiting room.** They serve one visitor at a
  time, but a visitor sent off to fill in a form goes to the waiting area rather
  than occupying the desk. The desk is never idle while anyone is ready — and
  one visitor who insists on doing their paperwork *at the desk* blocks
  everybody.
- **Cooperative, not preemptive.** Everyone must volunteer to step aside. One
  person who never volunteers stops the whole room. This is exactly why a
  blocking call is fatal here and merely slow with threads.
- **A relay handoff at fixed points** for cancellation: you can only be tapped
  out at a handoff (an `await`), never mid-stride.

## Analogies to refuse

- **"Async makes code run in parallel."** It does not. One thread, one task
  executing at a time. It overlaps *waiting*, which is a different thing and is
  the whole point.
- **"Async is faster than threads."** It scales further on concurrent
  connections and uses less memory. For a few dozen operations, threads are
  usually simpler and no slower.
- **"Single-threaded means no race conditions."** Anything spanning an `await`
  can interleave. This misconception ships real bugs.

---

## Accuracy guardrails

```
Accuracy requirements:
- asyncio is single-threaded and cooperative. There is NO preemption; a task
  runs until it awaits.
- Calling a coroutine function returns a coroutine object and executes nothing.
- `await` does not create concurrency. gather, TaskGroup or create_task do.
- A blocking call in a coroutine stops the ENTIRE loop, not just that task.
  Say this without softening it.
- CancelledError inherits from BaseException since 3.8, so `except Exception`
  does not catch it. Handlers that catch it must re-raise.
- Cancellation is delivered at an await point. A coroutine with no awaits
  cannot be cancelled.
- asyncio.TaskGroup and asyncio.timeout require 3.11+. asyncio.to_thread
  requires 3.9+.
- gather() without return_exceptions=True propagates the first exception while
  leaving the other tasks running and unobserved.
- A task created with create_task must be referenced somewhere, or it can be
  garbage collected before completing. TaskGroup handles this.
- Single-threaded does NOT mean race-free. Nothing is atomic across an await.
- Do not claim asyncio is universally faster than threads. State the axes:
  memory per connection and concurrency ceiling.
```

---

## After watching, you should be able to

- [ ] Describe the event loop's cycle in four steps.
- [ ] Say what calling a coroutine function does.
- [ ] Explain why three `await`s in a row are not concurrent, and fix it.
- [ ] Say what one blocking call does to 1,000 open connections.
- [ ] Name two things `TaskGroup` gives you that `gather` does not.
- [ ] Explain where `CancelledError` is delivered and why you must re-raise.
- [ ] Construct a race condition in single-threaded async code.
- [ ] State the colour problem and why it makes adoption a whole-stack decision.
