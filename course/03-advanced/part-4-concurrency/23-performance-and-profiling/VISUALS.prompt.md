# NotebookLM Visual Prompts — Module 23: Performance and Profiling

---

## Sources to add

| Source | Type |
|---|---|
| `23-performance-and-profiling/README.md` | Upload |
| `05-collections-and-comprehensions/README.md` (complexity) | Upload |
| https://docs.python.org/3/library/profile.html | Website |
| https://github.com/benfred/py-spy | Website |
| https://pythonspeed.com/ | Website |

---

## 1. Cinematic Video Overview

**Format:** Explanation
**Visual style:** Custom, with this description:

```
Clean technical schematic on a dark background. Time drawn as horizontal bars
whose width is duration, so a 1000x difference is physically visible rather
than a number. Flame graphs drawn as actual stacked flame graphs. Memory drawn
as a filling meter. Monospace type for code and profiler output. No characters.
```

**Steering prompt (paste this whole block):**

```
Audience: a programmer who has optimised code by rewriting loops they believed
were slow, without measuring, and who is not sure whether it helped.

Thesis: measure first, and work top-down through a hierarchy where each level
is worth 10 to 100 times the one below it. Almost everyone starts at the
bottom.

1. THE GUESS. Open with a 40-line function and ask the viewer to pick the
   slowest line. Show three plausible candidates highlighted. Then reveal the
   profile: the time is in a database call inside a loop -- an N+1 query -- and
   the three candidates together account for under one percent. Put the bars
   side by side so the 1000x is a physical width, not a claim. This is the
   whole module in ninety seconds and it must come first.

2. THE HIERARCHY. Draw eight rungs from "do you need to do this at all" down to
   "rewrite in C", with a typical gain beside each drawn to scale. Then animate
   where people actually start -- at rung 7 -- and show the gain they get
   compared with the rung 2 fix they walked past. Emphasise that the top rungs
   are usually SIMPLER code, not more complex.

3. MEASURING HONESTLY. Show fifty timing runs plotted as points. Show the mean
   sitting well above the cluster because of three outliers, and the minimum
   sitting at the bottom edge of the cluster. Explain that noise is ONE-SIDED:
   nothing can make code faster than it is, but a GC pause, another process, or
   CPU frequency scaling can all make it slower. Therefore the minimum is the
   estimate and the mean is a measure of how busy the machine was.

4. TOTTIME VERSUS CUMTIME. Draw a call tree with time flowing through it. Show
   cumtime as the total flowing through a branch, and tottime as the amount
   burned at each node itself. Then answer two different questions with the
   same profile: "which AREA is slow" (sort by cumulative -- the answer is a
   high-level function) and "which FUNCTION should I change" (sort by tottime --
   the answer is a leaf). Show someone optimising the cumtime answer and
   achieving nothing because it was only calling something else.

5. FLAME GRAPHS. Build one up: width is time, vertical is call depth. Show a
   wide plateau and a tall narrow spike, and say which one to care about. Then
   show a real shape -- a broad flat region under a single call -- and the
   viewer identifying the target without reading a single number.

6. THE COST TABLE, MADE PHYSICAL. Draw bars for a local read, an attribute
   access, a function call, and a raised exception. Make the function call
   visibly six times the local read. Then explain the consequences that follow
   from that one fact: why comprehensions beat map+lambda, why hot loops
   sometimes bind builtins to locals, and above all why NumPy wins -- ONE call
   processing a million elements instead of a million calls. Show a million
   little call-bars collapsing into two.

7. MEMORY. Show tracemalloc's two snapshots and the diff between them
   identifying the growing line. Then walk the four leaks the course has
   already met -- an unbounded cache, a listener registry, a stored traceback,
   a materialised stream -- and show the meter climbing for each.

8. WHEN TO STOP. Close with a curve: effort on the x axis, performance on the
   y, flattening sharply. Draw a horizontal line labelled "the requirement" --
   a p95 target or a batch window -- and mark where it is crossed. State that
   everything to the right costs complexity that is paid forever by every
   future reader, and that "it could be faster" is not a reason.
```

---

## 2. Mind Map

**Prompt:**

```
Build a mind map titled "Making Python Faster".

Branch 1 "The rule": measure first, why intuition fails, and profile realistic
data at realistic scale.

Branch 2 "The hierarchy": the eight rungs with typical gains, and the
observation that the top rungs usually SIMPLIFY the code.

Branch 3 "Timing": timeit, minimum not mean, setup not timed, constant folding,
perf_counter, and measuring at the real call rate.

Branch 4 "Profiling": cProfile, tottime vs cumtime and the question each
answers, pstats sorting, sampling profilers, py-spy top/record/dump, and flame
graph reading.

Branch 5 "Memory": tracemalloc snapshots and compare_to, the five classic
leaks, and the five ways to reduce memory.

Branch 6 "Where time goes": the cost table, the function call as the expensive
primitive, and the three consequences that follow from it.

Branch 7 "Vectorising": why NumPy wins (no interpreter overhead, contiguous
typed memory), and iterrows as the canonical mistake.

Branch 8 "Caching": the five layers, and the four hidden costs.

Branch 9 "Going native": NumPy, numba, Cython, Rust/PyO3, C -- ordered by cost,
with the permanent price of a build step.

Branch 10 "Stopping": defining fast enough, and complexity as a permanent tax.
```

---

## 3. Study Guide, Quiz, and Flashcards

**Study Guide prompt:**

```
Produce a study guide for someone whose service is too slow and who has one day
to fix it.

Include an ordered triage procedure: what to measure first, which tool at each
stage, and what a result at each stage tells you to do next.

Include a profiler-output reading guide: annotated cProfile output and an
annotated flame graph, with the specific question each answers.

Include a bottleneck catalogue: for each of about twelve symptoms (high CPU
with low throughput, high latency with low CPU, memory growing over hours,
slow only on large inputs, slow only in production, slow on the first request
after a deploy, one endpoint slow and the rest fine), the likely cause and the
tool that confirms it.

Include a micro-optimisation reference stating clearly that these are the LAST
resort, with measured gains for each so the reader can see how small they are
relative to the top rungs.

End with five slow programs described by symptom, each with the diagnosis, the
fix, and the measured improvement.
```

**Quiz prompt:**

```
Generate 14 questions.

At least five give a symptom and a profile excerpt and ask what to fix. Include
one where the correct answer is "the algorithm", one where it is "an N+1
query", one where it is "nothing -- it already meets the requirement", and one
where the profile is misleading because the input was unrealistically small.

At least three on measurement method: mean versus minimum, a benchmark that
measures a constant-folded expression, and a benchmark whose setup is inside
the timed statement.

Include: distinguishing tottime from cumtime on the same profile, choosing
between cProfile and py-spy for a production hang, and identifying which of
four listed leaks explains memory that grows only under load.

For each answer, name the rung of the hierarchy the fix belongs to.
```

**Flashcards prompt:**

```
20 flashcards. Front: a tool, term or question. Back: what it does and when to
reach for it.

Include: timeit, minimum vs mean, perf_counter, cProfile, pstats, tottime,
cumtime, py-spy top, py-spy record, py-spy dump, flame graph, tracemalloc,
compare_to, __slots__, generator, vectorisation, iterrows, lru_cache,
amortized, N+1 query, numba, Cython, "fast enough".
```

---

## The specific visuals to insist on

1. **The guessed line versus the profiled line**, with bars to scale showing
   1000x. This must be the opening image.
2. **The eight-rung hierarchy with gains to scale**, and an arrow showing where
   people actually start.
3. **Fifty timing points with the mean pulled up by outliers** and the minimum
   at the cluster's edge.
4. **A call tree with cumtime flowing through and tottime burned at each node.**
5. **A flame graph with a wide plateau and a tall spike**, and which to care
   about.
6. **A function-call bar six times a local-read bar**, then a million call-bars
   collapsing into two NumPy calls.
7. **Two tracemalloc snapshots and the diff** pointing at the growing line.
8. **The effort/performance curve crossing a requirement line.**

---

## Analogies that work

- **A doctor ordering tests before prescribing.** Nobody would accept
  "I reckon it's your liver" without a scan, and the same standard should apply
  to a hot loop.
- **Traffic on a road network.** The jam is at one junction; widening every
  other road changes nothing. `cumtime` tells you which route is congested;
  `tottime` tells you which junction.
- **A conveyor belt with one slow station.** Speeding up any other station moves
  no more product. This is why fixing anything other than the bottleneck yields
  zero, not "a bit".

## Analogies to refuse

- **"Python is slow."** Too coarse to act on. Python's *interpreter overhead per
  bytecode* is high; that is only the bottleneck for pure-Python CPU work, which
  is a minority of real programs.
- **"Premature optimisation is the root of all evil"** quoted without its second
  half. Knuth's point was that the critical 3 percent should absolutely be
  optimised — after it has been identified by measurement.
- **Describing micro-optimisations as "tricks" or "hacks".** They are small,
  measurable, last-resort changes, and framing them as clever encourages exactly
  the behaviour this module is trying to prevent.

---

## Accuracy guardrails

```
Accuracy requirements:
- Take the MINIMUM of repeated timings, not the mean. Noise is one-sided.
- tottime EXCLUDES sub-calls; cumtime INCLUDES them. State both directions.
- cProfile is a deterministic profiler and adds per-call overhead, which
  distorts call-heavy code. py-spy is a sampling profiler with low overhead and
  can attach to a running process.
- The cost figures for operations are ORDER-OF-MAGNITUDE, hardware- and
  version-dependent. Present the ratios, not the absolute numbers, as the
  lesson.
- NumPy's advantage has TWO causes: no per-element interpreter overhead, and
  contiguous typed memory rather than pointers to boxed objects. Give both.
- CPython 3.11+ made meaningful interpreter improvements (the specialising
  adaptive interpreter). Do not present old benchmark folklore as current.
- Memory reported by tracemalloc is Python-level allocation; the process RSS
  will differ because of allocator behaviour and because freed memory is not
  always returned to the OS.
- Caching introduces staleness, invalidation and unbounded growth. Do not
  present it as free.
- A build step for Cython/Rust/C is a permanent cost: a platform matrix,
  wheels, and a barrier to contribution. Say so.
```

---

## After watching, you should be able to

- [ ] State the one rule and why it is empirical.
- [ ] Recite the hierarchy and say which rung a proposed fix belongs to.
- [ ] Explain why the minimum is the right statistic.
- [ ] Say which profiler column answers "which area" and which answers "which
      function".
- [ ] Read a flame graph and point at the target in five seconds.
- [ ] Explain NumPy's advantage with both causes.
- [ ] Name four leak sources from earlier modules.
- [ ] Say how you would decide to stop.
