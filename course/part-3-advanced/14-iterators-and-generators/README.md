# Module 14 — Iterators, Generators, and Lazy Pipelines

**Time budget:** 5 hours lesson, 8 hours exercises
**Prerequisite:** Part 2 complete

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

This is the module that changes how you write Python.

A generator lets you write a function that produces a sequence **without ever
holding the sequence in memory**. Chain a few together and you have a pipeline
that processes a 50 GB file in constant memory, reads only what it needs, and
stops the moment the caller stops asking.

Concretely: this module is the difference between

```python
lines = open("50gb.log").readlines()      # MemoryError
```

and

```python
errors = (l for l in open("50gb.log") if "ERROR" in l)   # 200 bytes of memory
first_ten = list(islice(errors, 10))                      # reads ~10 lines
```

---

## 1. The iterator protocol

Two methods, and everything else in this module is built on them.

```python
iter(obj)      # -> obj.__iter__()  : returns an ITERATOR
next(it)       # -> it.__next__()   : the next value, or raises StopIteration
```

A `for` loop is sugar for exactly this:

```python
for x in things: process(x)

# is precisely:
it = iter(things)
while True:
    try:
        x = next(it)
    except StopIteration:
        break
    process(x)
```

| | Iterable | Iterator |
|---|---|---|
| Defines | `__iter__` | `__iter__` **and** `__next__` |
| `__iter__` returns | a **fresh** iterator | `self` |
| Reusable | yes | **no** |
| Examples | `list`, `dict`, `str`, `range` | generators, file objects, `iter([])` |

**Every iterator is an iterable; not every iterable is an iterator.** The
distinction shows up as the one-shot bug (Module 09), and it is worth being able
to state precisely:

```python
data = (x for x in range(3))
list(data)      # [0, 1, 2]
list(data)      # []          <- exhausted, silently
```

No error. That silence is the whole hazard.

---

## 2. Generator functions

Any function containing `yield` is a generator function. Calling it **runs
nothing** — it returns a generator object.

```python
def countdown(n: int):
    print("starting")            # does NOT run on the call
    while n > 0:
        yield n
        n -= 1
    print("done")

gen = countdown(3)               # nothing printed
next(gen)                         # 'starting', then 3
next(gen)                         # 2
```

`yield` **suspends** the function: locals, instruction pointer, and the whole
frame are preserved. `next()` resumes exactly where it stopped. That suspended
frame is the mental image to carry — it is also how `await` works (Module 22).

### Generators are the easiest way to write `__iter__`

Compare this with Module 09's iterator class:

```python
class Countdown:
    def __init__(self, start: int) -> None:
        self.start = start

    def __iter__(self):
        current = self.start      # a LOCAL, so each call gets fresh state
        while current > 0:
            yield current
            current -= 1
```

Two `for` loops both work, because each call to `__iter__` creates a new
generator with its own locals. That is the fix for the one-shot bug, and it is
free.

### `yield from`

```python
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)      # delegate, recursively
        else:
            yield item
```

`yield from x` is not just `for i in x: yield i` — it also forwards `send`,
`throw` and `close`, and propagates the sub-generator's return value. For plain
iteration the loop is equivalent; for coroutines it is not.

### Generator expressions

```python
squares = (x * x for x in range(1_000_000))     # lazy, ~200 bytes
squares = [x * x for x in range(1_000_000)]     # eager, ~40 MB

sum(x * x for x in data)                         # parens optional as sole arg
any(line.startswith("ERROR") for line in fh)     # short-circuits
```

**Use a generator expression when the values are consumed once.** Use a list
when you need to index, re-iterate, or take `len()`.

---

## 3. Pipelines

The technique that makes this module worth its time. Each stage is lazy; the
data flows through one item at a time.

```python
def read_lines(path):
    with open(path, encoding="utf-8") as fh:
        yield from fh

def parse(lines):
    for line in lines:
        parts = line.rstrip("\n").split("\t")
        if len(parts) == 4:
            yield {"ts": parts[0], "level": parts[1],
                   "user": parts[2], "msg": parts[3]}

def only(records, level):
    for r in records:
        if r["level"] == level:
            yield r

def summarise(records, limit):
    for r in islice(records, limit):
        yield f"{r['ts']} {r['user']}: {r['msg']}"

# nothing has run yet
pipeline = summarise(only(parse(read_lines("50gb.log")), "ERROR"), 10)

for line in pipeline:      # NOW it runs, one line at a time
    print(line)
```

Memory: one line. Work done: it stops after finding ten errors, even if the file
is 50 GB and the tenth error is on line 900.

**Three properties that fall out:**

1. **Constant memory**, regardless of input size.
2. **Early termination** — `break` at any point stops all upstream work.
3. **Composability** — any stage can be inserted, removed, or reordered without
   touching the others.

### The `with` trap in a generator

```python
def read_lines(path):
    with open(path) as fh:
        yield from fh          # the file stays open while the generator lives
```

If the consumer abandons the generator, the `with` block exits when the
generator is garbage collected — which is *usually* immediate under CPython
refcounting and *not guaranteed* (Module 02). For long-lived programs, close it
explicitly or use `contextlib.closing`. This is a real source of "too many open
files" in production.

---

## 4. `itertools`

The composable toolkit. Everything here is lazy.

```python
from itertools import (
    chain, islice, tee, cycle, repeat, count,
    groupby, takewhile, dropwhile, filterfalse, compress,
    accumulate, pairwise, product, permutations, combinations, zip_longest,
)

chain(a, b, c)                  # concatenate iterables
chain.from_iterable(nested)     # flatten one level -- the O(n) way
islice(it, 10)                  # a slice of an iterator
islice(it, 5, 15)
takewhile(lambda x: x < 100, it)   # stop at the first failure
dropwhile(lambda x: x < 100, it)   # skip until the first success
accumulate(nums)                    # running totals
pairwise("abcd")                    # ('a','b'), ('b','c'), ('c','d')  3.10+
groupby(sorted(rows, key=f), key=f) # group CONSECUTIVE equal keys
zip_longest(a, b, fillvalue=0)
count(1)                            # 1, 2, 3, ... infinite
```

**`groupby` requires sorted input.** It groups *consecutive* equal keys, like
Unix `uniq`. Unsorted input silently produces many small groups instead of one
per key — a quiet wrong answer, not an error. If you cannot sort (it is an
infinite stream, or sorting is too expensive), use `defaultdict(list)` instead.

**`tee` is not free.** `tee(it, 2)` buffers everything one branch has consumed
and the other has not. If one branch runs ahead, the buffer grows to that gap.
Two independent passes over a list are usually cheaper.

**Flattening:**

```python
sum(lists, [])                          # O(n^2). Never.
list(chain.from_iterable(lists))        # O(n). Always.
```

---

## 5. Generators as coroutines

`yield` is an expression, so a generator can *receive* values.

```python
def averager():
    total, count = 0.0, 0
    average = None
    while True:
        value = yield average        # RECEIVES from send(), yields the average
        total += value
        count += 1
        average = total / count

avg = averager()
next(avg)              # "prime" it: run to the first yield
avg.send(10)           # 10.0
avg.send(20)           # 15.0
```

Three methods drive a generator from outside:

```python
gen.send(value)        # resume, with `value` as the result of the yield
gen.throw(SomeError)   # raise inside the generator at the yield point
gen.close()            # raise GeneratorExit at the yield point
```

This is where `async`/`await` came from historically — before native
coroutines, `asyncio` was built on `yield from` over generators. You will rarely
write `send()` today, but understanding it makes Module 22 straightforward
rather than mysterious.

`contextlib.contextmanager` is the one place you use this daily:

```python
@contextmanager
def managed():
    setup()
    try:
        yield resource        # the with-block runs HERE, at the suspension
    finally:
        teardown()
```

The generator suspends at `yield`, the `with` body runs, and then the generator
is resumed to run its `finally`. `__exit__` is implemented by calling `send` or
`throw` on it — a direct application of everything above.

---

## 6. When *not* to be lazy

Laziness is not free, and it is not always right.

| Situation | Use |
|---|---|
| Need `len()` | a list |
| Need to iterate twice | a list |
| Need indexing or slicing | a list |
| Small data (under ~1000 items) | a list — clearer, and faster |
| Result feeds a C library (NumPy, pandas) | a list or array |
| Data larger than memory | a generator |
| Infinite or unbounded stream | a generator |
| Early termination likely | a generator |
| Expensive per-item work, may not need all | a generator |

**The debugging cost is real.** A generator pipeline shows you nothing until it
runs, a traceback points at the *consumption* site rather than the definition,
and you cannot inspect intermediate state in a debugger without consuming it.
`list()` a stage temporarily when debugging.

**The exhaustion bug is the one that bites.** Passing a generator to a function
that iterates it twice produces an empty second pass and no error at all
(Module 05's exercise). If a function must iterate twice, it should take a
`Sequence`, not an `Iterable`, and say so in its signature.

---

## Common mistakes in this module

| Mistake | Symptom | Fix |
|---|---|---|
| Iterating a generator twice | Second pass is empty, silently | `list()` it, or regenerate |
| `groupby` on unsorted input | Many tiny groups; wrong answer | Sort by the same key first |
| `sum(lists, [])` | O(n²) | `chain.from_iterable` |
| `len()` on a generator | `TypeError` | `sum(1 for _ in it)`, consuming it |
| `return value` in a generator | Not yielded; lands in `StopIteration.value` | `yield` it |
| Forgetting to prime a coroutine | `TypeError: can't send non-None` | `next(gen)` first |
| `with` inside an abandoned generator | File handles leak | `close()`, or `contextlib.closing` |
| `tee` with one branch far ahead | Unbounded buffering | Two passes over a list |
| Building a list to pass to `any`/`sum` | Wasted memory | Pass a generator expression |
| Generator in a hot inner loop | Slower than a list | Measure (Module 23) |

---

## Self-check quiz

1. Write the `while` loop a `for` loop desugars into.
2. What is the difference between an iterable and an iterator?
3. What happens when you call a generator function? What runs?
4. Why does `list(gen)` twice give `[...]` then `[]`, with no error?
5. What does `yield from` do that a `for`/`yield` loop does not?
6. Give three properties a lazy pipeline has that an eager one does not.
7. Why does `groupby` need sorted input, and what happens if it does not get it?
8. When is `tee` a bad idea?
9. What does `send()` do, and why must a coroutine be primed?
10. Name four situations where a list is the right answer.

---

## Exercises

1. **[`ex01_protocol.py`](exercises/ex01_protocol.py)** — Implement the
   protocol by hand, then with `yield`, and prove the reusability difference.
2. **[`ex02_pipeline.py`](exercises/ex02_pipeline.py)** — Build a log-analysis
   pipeline over a generated 200 MB file. Measure memory against the eager
   version.
3. **[`ex03_itertools.py`](exercises/ex03_itertools.py)** — Twenty problems,
   each with a one-line `itertools` answer. Then implement six of them yourself.
4. **[`ex04_coroutines.py`](exercises/ex04_coroutines.py)** — Build a running
   statistics coroutine, a broadcast fan-out, and a `@contextmanager` from
   scratch.

---

## Going deeper

- [`itertools`](https://docs.python.org/3/library/itertools.html) — read the whole page, then the recipes section twice
- [PEP 255](https://peps.python.org/pep-0255/) (generators), [PEP 380](https://peps.python.org/pep-0380/) (`yield from`)
- [`more-itertools`](https://more-itertools.readthedocs.io/) — the recipes, packaged and tested
- David Beazley, "Generators: The Final Frontier" — three hours, and worth every minute

---

**Next:** [Module 15 — Decorators, Closures, and functools](../15-decorators-closures-functools/README.md)
