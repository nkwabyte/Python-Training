# Module 23 — Performance and Profiling

**Time budget:** 4 hours lesson, 6 hours exercises
**Prerequisite:** Modules 05 (complexity), 21

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

There is one rule and everything else is technique:

> **Measure first. Your intuition about which line is slow is wrong often
> enough that acting on it is a waste of a day.**

This is not humility, it is empirical. Experienced engineers guess the hot spot
correctly perhaps half the time, and the half they get wrong they optimise
enthusiastically, add complexity, and gain nothing.

---

## 1. The order of operations

Work down this list. Each step is 10 to 100 times more valuable than the one
below it.

| # | Question | Typical gain |
|---|---|---|
| 1 | Do you need to do this at all? | ∞ |
| 2 | Is the algorithm right? (Module 05) | 10–10,000x |
| 3 | Is it doing I/O it could avoid, batch, or cache? | 10–1000x |
| 4 | Is the data structure right? (Module 05) | 10–100x |
| 5 | Can the work be done by a C library (NumPy, pandas)? | 10–100x |
| 6 | Can it be parallel? (Module 21) | up to core count |
| 7 | Micro-optimise Python | 1.1–2x |
| 8 | Rewrite in C / Rust / Cython | 10–100x, at great cost |

**Almost everybody starts at 7.** The N+1 query at step 3 costs a thousand times
more than every local variable lookup in the file, and fixing it is a two-line
change.

---

## 2. Measuring correctly

```python
import timeit
timeit.repeat("f(x)", setup="from __main__ import f, x", number=1000, repeat=5)
```

Four rules, each of which is the difference between a benchmark you can believe
and one you cannot:

**Take the minimum, not the mean.** Noise is one-sided: nothing makes code
faster than it can run, but a GC pause, another process, CPU frequency scaling
or a cache miss can all make it slower. The minimum estimates the true cost; the
mean measures how busy your laptop was.

**Do not let setup leak into the measurement.** `timeit`'s `setup` is not timed —
put everything you are not measuring there.

**Beware constant folding.** `timeit("1 + 2")` measures nothing; the compiler
folded it (Module 01).

**Measure the thing you actually do, at the rate you actually do it.** A 50x
ratio on a 7-microsecond operation is not a performance problem (Module 02).

For anything wall-clock, `time.perf_counter()`. Never `time.time()` (Module 19).

---

## 3. `cProfile`: where the time goes

```bash
python -m cProfile -o out.prof app.py
python -m pstats out.prof
```

```python
import cProfile, pstats
with cProfile.Profile() as prof:
    main()
pstats.Stats(prof).sort_stats("cumulative").print_stats(20)
```

**Two columns, two meanings, and confusing them wastes hours:**

- **`tottime`** — time in this function, *excluding* callees. Points at the leaf
  actually burning CPU.
- **`cumtime`** — time in this function *and everything it called*. Points at
  the branch of the program responsible.

Sort by `cumulative` to find *what area* is slow; sort by `tottime` to find
*which function* to change.

**`cProfile` adds per-call overhead**, so it distorts programs dominated by many
tiny calls. For a production process, use a **sampling** profiler:

```bash
py-spy top --pid 1234              # live, no restart, negligible overhead
py-spy record -o flame.svg --pid 1234
py-spy dump --pid 1234             # stack traces of every thread -- for hangs
```

`py-spy dump` on a hung process is the single most useful debugging tool in this
module.

**Flame graphs** read like this: width is time, stacking is call depth. A wide
plateau is where the time is. A tall narrow spike is deep recursion and usually
not your problem.

---

## 4. Memory

```python
import tracemalloc
tracemalloc.start()
snapshot1 = tracemalloc.take_snapshot()
run()
snapshot2 = tracemalloc.take_snapshot()
for stat in snapshot2.compare_to(snapshot1, "lineno")[:10]:
    print(stat)
```

`compare_to` between two snapshots is how you find a leak: it shows which lines
allocated memory that was not released.

The usual causes, all met before: an unbounded cache (Module 15), a listener
registry holding strong references (Module 02), a stored exception dragging in
every frame (Module 02), materialising a stream that should be lazy (Module 14),
and `lru_cache` on a method pinning every instance (Module 15).

Reducing memory: `__slots__` (Module 08), generators (Module 14), `array` or
NumPy for numbers, interning repeated strings, and processing in chunks.

---

## 5. Where Python's time actually goes

Rough costs on a modern CPU. **The ratios are the lesson; the absolute numbers
vary by hardware and by version** — 3.11's specialising interpreter changed
several of these substantially, and "zero-cost" exception handling made an
untaken `try` genuinely free.

| Operation | Approx. |
|---|---|
| Local variable read | ~10 ns |
| Global variable read | ~15 ns |
| Attribute access | ~20 ns |
| Function call | **~60 ns** |
| Method call | ~70 ns |
| Creating an object | ~80 ns |
| Dict lookup | ~25 ns |
| List append (amortized) | ~30 ns |
| `try` with no exception | ~0 ns (free since 3.11) |
| Raising and catching | ~50-200 ns |
| A NumPy op per element | ~1 ns |

**A Python function call is the expensive primitive.** That is why a
comprehension beats `map(lambda ...)` (Module 01), why hot loops sometimes
inline, and why NumPy wins — one call processing a million elements instead of a
million calls.

The techniques that actually help, in a loop a profiler has flagged:

```python
local_len = len                       # bind globals/builtins to locals
result = [x * 2 for x in data]        # comprehension over an explicit loop
"".join(parts)                        # never += in a loop (Module 03)
seen = set(other)                     # membership (Module 05)
if x in seen: ...
```

And the one that matters most: **do less work**. Hoist invariants out of loops,
avoid recomputing, and cache what is pure (Module 15).

---

## 6. Vectorising

```python
total = 0.0
for x in values:                      # 1,000,000 Python function calls
    total += math.sqrt(x)

total = np.sqrt(arr).sum()            # 2 calls into C
```

Typically 50 to 200 times faster, for two reasons: no per-element interpreter
overhead, and contiguous typed memory instead of a million pointers to boxed
floats (Module 08).

The rule for NumPy and pandas: **if you are writing a `for` loop over rows, you
are using it wrong.** `df.iterrows()` is the single most common pandas
performance bug (Module 29).

---

## 7. Caching

| Where | Tool | Wins when |
|---|---|---|
| Function results | `functools.cache` (Module 15) | Pure, repeated arguments |
| Computed attributes | `cached_property` | Expensive, per instance |
| Across processes | Redis / memcached | Shared, survives restarts |
| HTTP | Cache-Control, ETag | Reduces requests entirely |
| Database | Query cache, materialised view | Repeated expensive queries |

Caching is the highest-leverage optimisation and the one with the most hidden
cost: staleness, invalidation, memory growth, and a cold-start cliff. Module 33
covers doing it properly.

---

## 8. When to stop, and when to reach for C

**Stop when the number meets the requirement.** "Fast enough" is defined by a
p95 target, a batch window, or a cost budget — not by whether it could be
faster. Every further optimisation costs complexity, and complexity is paid
forever by everyone who reads the code.

**Before reaching for C**, exhaust steps 1 to 6. Then, in order of cost:

| Option | Effort | Notes |
|---|---|---|
| NumPy / pandas / Polars | low | Usually enough |
| `numba` `@jit` | low | One decorator; numeric loops only |
| Cython | medium | Python-like syntax, C speed, a build step |
| Rust + PyO3 | high | Best performance and safety; a whole toolchain |
| C extension | high | Maximum control, maximum footgun |

Every one of these adds a build step, a platform matrix, and a barrier to
contribution. That cost is real and permanent.

---

## Common mistakes in this module

| Mistake | Symptom | Fix |
|---|---|---|
| Optimising without profiling | Days spent, no gain | Profile first |
| Micro-optimising an O(n²) algorithm | 2x on something that needed 1000x | Fix the algorithm |
| Benchmarking with the mean | Noisy, unreproducible numbers | Take the minimum |
| `time.time()` for durations | Negative durations | `perf_counter` |
| Profiling a toy input | The hot spot differs at scale | Profile realistic data |
| Confusing `tottime` and `cumtime` | Optimising the wrong function | Know which question each answers |
| `cProfile` in production | Distorted results, real slowdown | `py-spy` |
| `iterrows()` | 100x slower than vectorised | Vectorise |
| Caching an impure function | Wrong results | Module 15 |
| Adding a C extension first | Build complexity for a fixable algorithm | Steps 1-6 |
| Never stopping | Unmaintainable code, no requirement met | Define "fast enough" |

---

## Self-check quiz

1. What is the one rule, and why is it empirical rather than modest?
2. Give the order of operations, and which step people wrongly start at.
3. Why take the minimum of repeated timings rather than the mean?
4. What is the difference between `tottime` and `cumtime`, and which finds what?
5. When is `cProfile` the wrong tool, and what replaces it?
6. How do you read a flame graph?
7. Why is a Python function call the expensive primitive?
8. Why is NumPy 50-200x faster, and what are the two reasons?
9. Name four causes of a memory leak in Python, from earlier modules.
10. How do you decide to stop optimising?

---

## Exercises

1. **[`ex01_predict.py`](exercises/ex01_predict.py)** — Rank ten operations by
   cost, then measure. Score yourself.
2. **[`ex02_profile.py`](exercises/ex02_profile.py)** — A slow program with four
   bottlenecks at different levels of the hierarchy. Find them in order.
3. **[`ex03_memory.py`](exercises/ex03_memory.py)** — Find three leaks with
   `tracemalloc`, then halve the memory of a working program.
4. **[`ex04_vectorise.py`](exercises/ex04_vectorise.py)** — Take a numeric loop
   through six versions, from naive Python to NumPy, measuring each.

---

## Going deeper

- [`cProfile`](https://docs.python.org/3/library/profile.html), [`timeit`](https://docs.python.org/3/library/timeit.html), [`tracemalloc`](https://docs.python.org/3/library/tracemalloc.html)
- [py-spy](https://github.com/benfred/py-spy) and [scalene](https://github.com/plasma-umass/scalene) — install both
- Brendan Gregg on flame graphs — the original, and still the clearest
- [Python Speed](https://pythonspeed.com/) — Itamar Turner-Trauring, especially on memory

---

**Next:** [Module 24 — CPython Internals](../24-cpython-internals/README.md)
