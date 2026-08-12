# Solutions — Module 14

---

## Exercise 14.1 — The protocol

The hand-written version needs **two** classes, and that is the lesson.
`Fibonacci` is the iterable (a factory); `FibonacciIterator` is the cursor
(holds the position). `Fibonacci.__iter__` returns a *new* cursor each call,
which is why two loops work.

`BrokenFibonacci`, whose `__iter__` returns `self`, produces the silent
one-shot bug: the second loop yields nothing and raises nothing.

The generator version is three lines and cannot have that bug, because each
call to `__iter__` creates a new generator with its own locals. **Write
`__iter__` as a generator unless you have a specific reason not to.**

**Why `iter()` on a `Countdown` prints nothing:** calling a generator function
creates a generator object and executes none of the body. The first `next()` is
what runs to the first `yield`. Section 2 of the video is exactly this.

**`average_and_max` — three fixes, three situations:**

```python
def f(numbers):                     # (a) materialise
    numbers = list(numbers)         # simplest; O(n) memory; correct
    ...

def f(numbers):                     # (b) one pass
    total = count = 0; largest = None
    for n in numbers:               # works on infinite streams; O(1) memory
        ...

def f(numbers: Sequence[float]):    # (c) change the contract
    ...                             # the type checker rejects a generator
```

(a) when the input is small and clarity matters. (b) when it may be large or is
a stream. (c) when two passes are genuinely required and you want the *caller*
to decide how to materialise. Silently accepting an `Iterable` and iterating it
twice is the bug; all three fixes work by removing that.

---

## Exercise 14.2 — The pipeline

Typical results over a 50 MB file, taking the first 10 errors:

| | Peak memory | Time |
|---|---|---|
| Eager | ~250 MB (≈5x file size) | ~1.4 s |
| Lazy | ~0.1 MB | ~0.01 s |

The eager version peaks at several times the file size, because the text, the
line list, and the parsed dicts all exist simultaneously — and a dict per record
costs far more than the bytes it holds (Module 03).

**The interesting comparison is the second one.** At `limit=10` the lazy version
is ~100x faster, because it stops after finding ten errors. At
`limit=1_000_000` (more than exist) both must read the whole file, and the lazy
version is only slightly faster — sometimes *slower*, because per-item generator
overhead is real. **Laziness buys memory and early termination, not raw speed.**

**Counting malformed lines from inside a generator** — three options, each with
a real trade-off:

1. **A mutable counter passed in** (`stats: dict`). Simple, and couples the
   caller to the stage.
2. **`return` the count**, retrieved from `StopIteration.value` via
   `yield from`. Correct and obscure; almost nobody reads it that way.
3. **Yield a tagged union** — `("record", r)` or `("error", line)` — and let the
   consumer route. Most composable, most verbose, and it is what real ETL
   frameworks do.

Recommended: option 1 for a script, option 3 for a pipeline anyone else will
extend.

**`count_by_user` cannot terminate early** — it must see every line. Laziness
still helps: peak memory is one line plus the result dict (a few hundred
entries), rather than the whole file. **Laziness helps whenever the *input* is
larger than the *output*, even with no early exit.**

**`busiest_hour` and why `groupby` is wrong here:** it needs the input sorted by
hour, which means materialising and sorting the entire file — turning an O(n)
constant-memory problem into O(n log n) with O(n) memory. `Counter` does it in
one pass. `groupby` is for input that is *already* sorted.

---

## Exercise 14.3 — Twenty problems

See [`ex03_itertools_solution.py`](ex03_itertools_solution.py). Six worth
calling out:

**p03 `chunks`** uses the two-argument `iter(callable, sentinel)` form, which
calls the callable until it returns the sentinel. Combined with `islice` over a
shared iterator, that chunks lazily with no index arithmetic. (3.12+ has
`itertools.batched`.)

**p06/p07 — `takewhile` and `dropwhile` are not filters.** `takewhile` *stops*
at the first failure: `[1,2,-1,3]` gives `[1,2]`, where `filter` gives
`[1,2,3]`. `dropwhile` stops *testing* after the first success, which is why
later `#` lines survive in p07.

**p08 — ship the `defaultdict` version.** `groupby` needs a sort (O(n log n)
plus materialisation), only groups consecutive keys, and produces sub-iterators
invalidated by advancing — so `list(g)` inside the loop is mandatory and easy to
forget. `defaultdict` is O(n), needs no sort, works on unsortable keys, and
cannot be silently wrong. `groupby` earns its place only when the input is
*already* sorted and you want to stream.

**p14 — three different questions, three answers.** Consecutive dedupe is
`groupby`; remove-all-duplicates-keeping-order is `dict.fromkeys`;
remove-all-duplicates-order-irrelevant is `set`.

**p16 — the shared-iterator trick.** `islice` *advances* the underlying
iterator, so after materialising the head, the same object is positioned exactly
at item n. Returning it gives a lazy tail with no buffering. Using `tee` instead
would buffer the entire head — correct and needlessly expensive.

**p18/p19 — `deque(maxlen=1)` gets the last item in constant memory**, and
counting an iterator necessarily *consumes* it. That is why `len()` is undefined
for iterators: a silently-consuming `len()` would be far worse than a
`TypeError`.

**Part B's `my_groupby` is the hard one**, and the difficulty is instructive:
the caller may advance to the next group without consuming the current one, so
the outer generator must be able to skip the remainder itself. That requires
shared mutable state between the two generators. This is exactly why the real
`itertools.groupby` documents that a group is invalid once you advance past it —
not an API wart, but the only way to avoid buffering an arbitrarily large group.

---

## Exercise 14.4 — Coroutines

**Welford's algorithm** for the running standard deviation is the point of the
first task: computing it from a stored list defeats the purpose, which is
constant memory over an unbounded stream. The recurrence keeps a running mean
and a running sum of squared deviations, and it is also numerically more stable
than the naive "sum of squares minus square of sum" formula, which loses
precision catastrophically for large values with small variance.

**The `@prime` decorator** removes a genuinely confusing error message
(`TypeError: can't send non-None value to a just-started generator`) and is a
natural preview of Module 15.

**`broadcast` needs a snapshot** of its targets before sending, for the same
reason Module 04's event bus did — a target that unsubscribes itself during a
send would otherwise corrupt the iteration.

**`my_contextmanager` is the most valuable task in the module**, because it
shows that `with` is *entirely* built on the generator protocol:

```python
__enter__  =  next(gen)                       -> the yielded value
__exit__   =  gen.throw(exc) if the block raised
              next(gen)      if it did not
              StopIteration means the generator finished normally
```

**Why `throw()` rather than `next()` on the exception path:** the generator is
suspended *at the `yield`*, inside its `try`. `throw()` raises the exception **at
that point**, so the generator's own `except` and `finally` clauses see it and
run in the right order. Calling `next()` instead would resume normally, run the
`finally` for the wrong reason, and the generator would never learn that the
block failed — so a context manager that logs failures, rolls back a
transaction, or suppresses a specific exception could not work at all.

And if the generator *catches* the thrown exception and returns without
re-raising, `__exit__` must return `True` — that is how `contextlib.suppress`
works, and it is the one legitimate use of exception suppression from Module 09.
