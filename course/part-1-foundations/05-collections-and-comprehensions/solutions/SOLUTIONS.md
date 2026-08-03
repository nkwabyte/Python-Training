# Solutions — Module 05

---

## Exercise 05.1 — Predict, then measure

See [`ex01_complexity_solution.py`](ex01_complexity_solution.py). Representative
output (microseconds per operation, doubling n each column):

| Operation | 1k | 2k | 4k | 8k | 16k | Class |
|---|---|---|---|---|---|---|
| `lst[i]` | 0.029 | 0.028 | 0.029 | 0.027 | 0.027 | O(1) |
| `lst.append` | 0.014 | 0.014 | 0.014 | 0.013 | 0.020 | O(1) amortized |
| `lst.insert(0, x)` | 0.29 | 0.54 | 1.03 | 2.10 | 4.15 | O(n) |
| `lst.pop()` | 0.015 | 0.015 | 0.015 | 0.013 | 0.014 | O(1) |
| `lst.pop(0)` | 0.088 | 0.161 | 0.322 | 0.634 | 1.49 | O(n) |
| `x in list` | 2.03 | 4.23 | 9.67 | 19.6 | 38.7 | O(n) |
| `x in set` | 0.008 | 0.008 | 0.007 | 0.007 | 0.008 | O(1) |
| `x in dict` | 0.009 | 0.009 | 0.009 | 0.009 | 0.009 | O(1) |
| `sorted()` | 21.7 | 49.2 | 130 | 381 | 963 | O(n log n) |
| `lst[:]` | 0.64 | 1.20 | 4.05 | 8.53 | 17.3 | O(n) |

Read the *ratios*, not the absolute numbers: with n doubling each column, a
ratio near 1 is O(1), near 2 is O(n), a little above 2 is O(n log n), and near 4
is O(n²).

### The four measurement traps

These matter more than the results, because they are how benchmarks lie.

**Destructive operations destroy what they measure.** Running `lst.pop()` 20,000
times against a list of 1,000 does not measure a list of 1,000 — it empties it
after fifty repetitions and then measures something else entirely. The fix used
here is a deliberately small `number` relative to `n`, so the structure changes
size by at most a fifth. `timeit` cannot express "reset between repetitions"
without putting the reset inside the timed statement, where it would itself be
measured. Knowing that limitation is most of what separates a benchmark you can
believe from one you cannot.

**Membership must search for a missing element.** `0 in lst` returns
immediately, and you have measured nothing.

**Sorting an already-sorted list is O(n), not O(n log n).** Timsort detects
existing runs and stops. Always shuffle first.

**Take the minimum of repeats, not the mean.** Timing noise is one-sided:
nothing can make code run faster than it can, but another process, a GC pause,
CPU frequency scaling, or a cache miss can all make it slower. The minimum is
the best estimate of the true cost; the mean measures how busy your machine was.
Module 23 returns to this.

### Amortization

Appending 100,000 items triggers about **66 reallocations** — roughly 0.07
percent of appends pay a copy. The list grows geometrically, so the number of
reallocations for n appends is O(log n), and the total copying work is a
geometric series summing to O(n). Divide O(n) total work by n appends and you
get O(1) each.

That is what *amortized* means, and it is stronger than it sounds: it is a
guarantee over **any** sequence of appends, not an average over random inputs.
(CPython's exact growth factor is an implementation detail and has changed
between versions. The geometric *shape* is what matters.)

### The set/list crossover

With ten membership tests, the set wins from roughly **4 to 8 elements** — far
lower than most people guess. And the crossover moves *left* as the number of
probes grows, because the set is built once and the list is scanned every time.

The one thing that ruins it: building the set **inside** the loop. That is
slower than the list at every size, and it is the most common way people
"optimise" this and make it worse. Build the set once, outside. That single
habit is most of what container awareness buys you in practice.

---

## Exercise 05.2 — Comprehensions in both directions

See [`ex02_comprehensions_solution.py`](ex02_comprehensions_solution.py).

Four items in Part A are traps rather than conversions:

**a07 (transpose)** has a one-word answer: `zip(*matrix)`. Ship that, not the
comprehension. The lesson generalises: **before writing a comprehension over
`range(len(...))`, check for a builtin.** The comprehension version is correct
and reimplements something that already exists, faster and without an index bug.

**a10 (grouping)** should *not* become a comprehension. Grouping needs
accumulation into an existing bucket, which a comprehension cannot express
without either re-scanning the input per key (O(n·k)) or a walrus trick nobody
can read. `defaultdict(list)` and a three-line loop is the answer. Note the
solution returns `dict(groups)` — never leak a `defaultdict` across an API
boundary, or a caller's innocent lookup silently inserts a key.

**a14 (invert)** silently loses data when two keys share a value: later wins.
Acceptable only when values are known unique. That a one-liner hides this
decision is exactly why it deserves a comment.

**a15 (running total)** cannot be a plain comprehension, because each result
depends on the previous one and comprehensions carry no state between
iterations. `itertools.accumulate` is the answer. The walrus "solution"
(`[total := total + n for n in nums]`) works and is a bad idea: it mutates an
enclosing variable as a side effect of building a list, so the comprehension has
stopped describing a result and become a loop in disguise — and it leaves
`total` modified afterwards.

### Part B — when a comprehension is wrong

**b01, side effects.** `[print(w) for w in words]` builds a list of `None`s and
throws it away. Worse than the waste, it lies about intent: a comprehension says
"I am producing a value", and this produces nothing.

**b02, too many clauses.** Four clauses plus a conditional expression inside a
`range()`. Nobody can read it, and — the practical objection — nobody can debug
it: you cannot set a breakpoint inside a comprehension or print an intermediate
value. **Rule of thumb: two `for`s or two `if`s is the ceiling.**

**b03, hidden repeated work.** `expensive()` is called *three times per element*,
once in each condition and once in the output expression. On a disk or network
call that is a 3x cost increase hidden inside code that looks efficient. This is
the one place the walrus genuinely earns its keep:

```python
[r.upper() for p in paths if (r := expensive(p)) is not None and len(r) > 3]
```

Removing redundant work is what `:=` was designed for; adding side effects is
not.

---

## Exercise 05.3 — The analytics pipeline

See [`ex03_grouping_solution.py`](ex03_grouping_solution.py). Container choices:

| Question | Tool | Why |
|---|---|---|
| Status counts | `Counter` | Counts, and `most_common()` orders for free |
| Group by day | `defaultdict(list)` | The canonical grouping tool |
| Top paths | `Counter.most_common(k)` | Uses `heapq` internally: O(n log k), not a sort |
| Slowest per path | running-maximum `dict` | One pass, O(1) memory per key |
| Users with errors | set comprehension | Dedupe is the requirement |
| Churn | set difference | O(n) and one expression |

**`slowest_per_path` is worth dwelling on.** The obvious version groups
everything and then takes a max per group — O(n) memory for a result that is
O(distinct paths). Running maxima is O(1) memory per key and works on a stream,
so it is the only version that runs at all on a log file larger than RAM. That
is Module 14's lesson arriving early.

**Two facts about percentiles that come back in Module 35:**

*Why p95 beats the mean as an SLO.* The mean is dominated by the bulk of fast
requests and hides the tail. A service where 95 percent of requests take 20ms
and 5 percent take 8 seconds has a mean around 420ms — a number that describes
no actual request while concealing that one user in twenty is having an unusable
experience. And tails compound: a page making 20 backend calls hits the p95 of
at least one of them most of the time.

*Why you cannot average percentiles.* A percentile is a position in a sorted
distribution, not an additive quantity. Averaging two servers' p95s produces a
number with no meaning — especially when their traffic volumes differ, but even
with equal traffic the combined p95 depends on the *shapes* of both
distributions. To get a real overall p95 you must merge the underlying
observations, which is precisely why Prometheus stores histogram buckets instead
of precomputed quantiles.

---

## Exercise 05.4 — LRU cache

See [`ex04_lru_solution.py`](ex04_lru_solution.py).

**Why both structures are needed.** You need two things at once: find a key in
O(1), and move any key to "most recent" in O(1). A dict gives the first and has
no reorderable order; a linked list gives the second and finds keys in O(n).
Storing *nodes* as the dict's values gives both — jump straight to the node,
unlink and relink in constant time.

**Sentinel head and tail nodes are not decoration.** Without them, unlink and
insert must each handle "first node", "last node", "only node", and "empty
list". Four edge cases, and in most hand-rolled versions at least one is wrong.
With sentinels every real node always has a `prev` and a `next`, and the code
has no branches at all.

**The test that catches a real bug:** `__contains__` must not count as a use.
A membership check that silently promotes an entry to most-recent will keep
dead keys alive forever in a monitoring or debugging code path.

**Measured result:** `OrderedDict` wins by roughly 1.5x, because `move_to_end`
and `popitem` run in C while the hand-rolled version does four Python-level
attribute assignments per reorder. Both facts matter and neither cancels the
other: *a better algorithm beats a faster language, but at equal algorithms the
C implementation wins by a constant factor.* Module 23 formalises this.

**Is a plain dict enough in 3.7+?** Almost. It preserves insertion order and
supports evicting the oldest via `next(iter(d))`, but it has no `move_to_end`.
You can emulate it with `d[k] = d.pop(k)`, which is O(1) and works — so yes,
sufficient. What you lose is the intent being obvious.

**`functools.lru_cache`** uses a dict mapping key to a list-based circular
doubly linked list node (`[prev, next, key, result]`), a lock for thread safety,
and a sentinel root. It is pure Python, about 100 lines in `Lib/functools.py`,
and worth reading: it is the design you just wrote, plus thread safety and a
fast path for the unbounded case.

**When LRU is the wrong policy** — three real cases:

1. **A full scan over data larger than the cache.** Reading a 10 GB table
   through a 1 GB LRU evicts everything before it is reused: hit rate zero, and
   you pay the bookkeeping for nothing. Databases use scan-resistant policies
   (LRU-K, ARC) or mark scan pages use-once.
2. **Strong frequency skew.** If one key is hit 1000 times an hour and a
   thousand others once each, LRU will evict the hot key because it was not
   touched in the last few seconds. LFU or a hybrid (TinyLFU) keeps it.
3. **Data with a natural expiry** — sessions, quotes, weather. TTL is the
   correct policy; LRU will serve stale data indefinitely as long as it is
   popular.
