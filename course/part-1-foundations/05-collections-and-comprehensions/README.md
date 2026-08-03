# Module 05 — Collections in Depth and Comprehensions

**Time budget:** 4 hours lesson, 7 hours exercises
**Prerequisite:** Modules 02, 03, 04

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

Choosing the right container is the highest-leverage decision in most Python
code, and it is made in the first thirty seconds of writing a function. This
module gives you the complexity table, the internal shapes that produce it, and
the comprehension syntax that makes using them idiomatic.

---

## 1. `list`: a dynamic array of pointers

A `list` is a contiguous array of **pointers to objects**, not the objects
themselves. That single fact explains its performance profile.

```
lst = [a, b, c]

  lst ──> [ ● , ● , ● , _ , _ , _ ]      over-allocated
            │   │   │
            v   v   v
           obj obj obj                    scattered anywhere in memory
```

| Operation | Complexity | Note |
|---|---|---|
| `lst[i]` | O(1) | pointer arithmetic |
| `lst[i] = x` | O(1) | |
| `append` | O(1) amortized | occasional resize copies everything |
| `pop()` | O(1) | from the end |
| `pop(0)` / `insert(0, x)` | **O(n)** | everything shifts |
| `x in lst` | **O(n)** | linear scan with `==` |
| `del lst[i]` | O(n) | |
| `len` | O(1) | stored |
| `sort` | O(n log n) | Timsort, stable |
| `lst[a:b]` | O(b-a) | builds a new list |

**Amortized O(1) append** means: the list over-allocates, so most appends are
free; occasionally it grows (roughly 1.125x plus a constant in CPython) and
copies. Averaged over many appends, constant. Any *single* append may be O(n).

The pointer indirection is why a list of a million ints costs ~40 MB and a NumPy
array of the same costs 8 MB, and why numeric loops are slow (Modules 23, 29).

---

## 2. `dict`: a hash table with compact ordering

Since 3.6, CPython's dict has two parts: a dense array of entries in insertion
order, and a sparse index array of positions into it.

```
indices : [ _ , 1 , _ , 0 , _ , 2 , _ , _ ]    sparse, sized to load factor
entries : [ (hash, key, value),                dense, INSERTION ORDER
            (hash, key, value),
            (hash, key, value) ]
```

That layout gives ordering for free and saves memory. Insertion order became a
**language guarantee in 3.7** (it was a CPython implementation detail in 3.6 —
worth knowing when reading old code).

| Operation | Complexity |
|---|---|
| `d[k]`, `d[k] = v`, `del d[k]`, `k in d` | O(1) average, O(n) worst |
| iteration | O(n), insertion order |
| `len` | O(1) |

The lookup: hash the key, mask it to an index, probe. On collision, probe again.
On a match of hashes, confirm with `==`. This is why **`__hash__` and `__eq__`
must agree** (Module 09), and why a mutable key would be unfindable (Module 03).

### The methods worth knowing

```python
d.get(k, default)               # no KeyError
d.setdefault(k, [])             # get, inserting the default if absent
d.pop(k, default)
d.popitem()                     # removes and returns the LAST item (LIFO)
d | other                       # merge, 3.9+ (right wins)
d |= other                      # in-place merge
{**a, **b}                      # merge, older syntax
d.keys() / .values() / .items() # VIEWS: live, not copies
dict.fromkeys(seq)              # dedupe preserving order (Module 03)
```

Views are live and cheap:

```python
keys = d.keys()
d["new"] = 1
print("new" in keys)      # True -- the view reflects the change
```

Key views also support set operations: `d1.keys() & d2.keys()` gives the common
keys. `d.items() - other.items()` gives the differing pairs. Underused and
excellent.

**`setdefault` versus `defaultdict`:**

```python
groups = {}
for item in items:
    groups.setdefault(item.kind, []).append(item)     # fine

from collections import defaultdict
groups = defaultdict(list)
for item in items:
    groups[item.kind].append(item)                     # cleaner
```

The `defaultdict` catch: **reading a missing key inserts it.** `if x in dd`
is safe; `dd[x]` is not. Convert with `dict(dd)` before returning it to code
that does not expect that behaviour.

---

## 3. `set`: a hash table without values

```python
a | b       # union
a & b       # intersection
a - b       # difference
a ^ b       # symmetric difference (in one or the other, not both)
a <= b      # subset
a.isdisjoint(b)
```

O(1) average membership, add, and remove. Unordered. Elements must be hashable.
`frozenset` is the immutable, hashable version — usable as a dict key or a set
member.

The two workhorse uses:

```python
seen = set()                            # dedupe / membership tracking
common = set(a) & set(b)                # relational algebra without loops
```

Set operations replace nested loops with a single expression *and* change the
complexity from O(n·m) to O(n+m). Any time you write a nested loop comparing two
collections, ask whether it is a set operation.

---

## 4. `tuple`

Immutable, hashable (if contents are), and compact. Two distinct uses:

```python
point = (3, 4)              # a RECORD: position means something
coords = (1, 2, 3, 4, 5)    # a sequence that happens not to change
```

For records, `NamedTuple` or a `dataclass` (Module 11) is almost always better,
because `p.x` beats `p[0]`.

Unpacking is where tuples earn their keep:

```python
a, b = b, a                      # swap, no temporary
first, *rest = [1, 2, 3, 4]      # first=1, rest=[2,3,4]
*init, last = [1, 2, 3, 4]       # init=[1,2,3], last=4
a, (b, c) = 1, (2, 3)            # nested
for i, (name, score) in enumerate(pairs): ...
def f(): return 1, 2             # returns a tuple; callers unpack it
```

---

## 5. Comprehensions

```python
[f(x) for x in xs if pred(x)]           # list
{f(x) for x in xs}                      # set
{k: v for k, v in pairs}                # dict
(f(x) for x in xs)                      # GENERATOR -- lazy, not a tuple
```

Read them outside-in: *what to produce*, then *what to loop over*, then *what to
keep*.

```python
[y for x in matrix for y in x]           # flatten: loops in the same order
                                          # you would write them nested
[[y for y in row] for row in matrix]     # nested comprehension: inner produces
                                          # a list per row
```

The multi-`for` order trips everyone up once. It reads left to right in the same
order as the equivalent nested `for` statements.

### Conditions

```python
[x for x in xs if x > 0]                 # FILTER: after the for
[x if x > 0 else 0 for x in xs]          # TRANSFORM: a conditional expression
                                          # before the for
[x for x in xs if x > 0 if x < 10]       # two filters, ANDed
```

### When not to use one

- More than two `for` clauses, or a `for` plus two conditions: use a loop.
- Any side effect. `[print(x) for x in xs]` builds a list of `None` and throws
  it away. Write a `for` loop.
- When the expression no longer fits on a line and reads worse than three lines
  of loop.

A comprehension should read as a *description of the result*. When it starts
reading as a *procedure*, it should be a loop.

### Generator expressions: the lazy version

```python
sum(x**2 for x in range(1_000_000))     # never builds the list
any(line.startswith("ERROR") for line in fh)   # stops at the first hit
max((score(x), x) for x in candidates)
```

Parentheses are optional when it is the only argument to a call. Use a generator
expression when you are consuming the values once — it uses O(1) memory instead
of O(n) and can short-circuit. Module 14 makes this a design tool.

---

## 6. Sorting

```python
sorted(xs)                                   # new list
xs.sort()                                    # in place, returns None
sorted(xs, key=len)                          # by a computed value
sorted(xs, key=lambda p: (p.dept, -p.score)) # multi-key; - reverses a number
sorted(xs, reverse=True)
sorted(xs, key=str.casefold)                 # case-insensitive text

from operator import attrgetter, itemgetter
sorted(people, key=attrgetter("age"))        # faster and clearer than a lambda
sorted(rows, key=itemgetter(1, 0))
```

Facts to keep:

- **Timsort, O(n log n), and stable.** Stability means equal elements keep their
  relative order, which is what makes multi-pass sorting work:

  ```python
  rows.sort(key=itemgetter("name"))     # secondary key first
  rows.sort(key=itemgetter("dept"))     # primary key last
  ```

- The `key` function is called **once per element**, not on every comparison.
  That is why `key=` beats the removed `cmp=` and why an expensive key is fine.
- For reverse-sorting on a non-numeric key, use `reverse=True` rather than
  negating — you cannot negate a string.
- For top-k, `heapq.nlargest(k, xs)` is O(n log k) and streams its input.

---

## 7. `collections`

```python
from collections import Counter, defaultdict, deque, namedtuple, ChainMap
```

**`Counter`** — counting, with the counting methods you want:

```python
c = Counter(words)
c.most_common(3)                # [(word, n), ...]
c["missing"]                    # 0, not a KeyError
c1 + c2 / c1 - c2 / c1 & c2     # add, subtract (drops <=0), min
sum(c.values())                 # total
```

**`defaultdict`** — a factory for missing keys. `defaultdict(list)`,
`defaultdict(int)`, `defaultdict(set)`, or `defaultdict(lambda: {"n": 0})`.

**`deque`** — O(1) at both ends, which `list` is not:

```python
d = deque(maxlen=100)           # a bounded ring buffer: old items fall off
d.appendleft(x); d.popleft()    # O(1)  -- list.pop(0) is O(n)
d.rotate(1)
```

Ideal for queues, sliding windows, BFS frontiers, and "keep the last N" logs.

**`ChainMap`** — layered lookup without merging:

```python
config = ChainMap(cli_args, env_vars, file_config, defaults)
config["timeout"]               # first layer that has it wins
```

Cheaper than merging dicts and it preserves which layer a value came from.

---

## 8. Choosing a container

| Need | Use |
|---|---|
| Ordered, changes | `list` |
| Fixed record, hashable | `tuple` / `NamedTuple` / frozen dataclass |
| Lookup by key | `dict` |
| Membership, dedupe, set algebra | `set` |
| Queue, sliding window, last-N | `deque` |
| Counting | `Counter` |
| Grouping | `defaultdict(list)` |
| Priority / top-k | `heapq` |
| Layered config | `ChainMap` |
| Sorted, with fast inserts | `bisect` on a list, or `sortedcontainers` |
| Large numeric data | `array`, or NumPy (Module 29) |

The two questions that answer this almost every time:

1. **How will I look things up?** By position → list. By key → dict. By presence
   → set.
2. **Where do I add and remove?** Both ends → deque. End only → list.

---

## Common mistakes in this module

| Mistake | Symptom | Fix |
|---|---|---|
| `x in list` inside a loop | Quadratic runtime | Build a `set` first |
| `list.pop(0)` as a queue | Quadratic runtime | `collections.deque` |
| `x = lst.sort()` | `x` is `None` | `sorted()` returns; `.sort()` mutates |
| Reading `defaultdict[k]` to test | Key gets inserted | `k in dd`, or `dict(dd)` |
| `[print(x) for x in xs]` | Builds and discards a list | Use a `for` loop |
| Consuming a generator twice | Second pass sees nothing | Materialise with `list()` |
| `sorted(xs, key=lambda x: -x.name)` | `TypeError` on a string | `reverse=True` |
| `{}` for an empty set | That is an empty dict | `set()` |
| Mutable default of `[]` | Shared state | `None` sentinel |
| `sum(lists, [])` to flatten | O(n²) | `itertools.chain.from_iterable` |
| Building an index inside a loop | Rebuilt every iteration | Build it once outside |

---

## Self-check quiz

1. Why is `list.append` O(1) amortized rather than O(1)?
2. Why is `list.pop(0)` O(n), and what should you use instead?
3. Describe the two arrays in a modern CPython dict and what each buys.
4. In which version did dict insertion order become a language guarantee?
5. What does `d.keys() & other.keys()` return, and why is it useful?
6. What is the difference between a filter condition and a conditional
   expression in a comprehension? Write one of each.
7. What does "Timsort is stable" mean, and how do you exploit it for multi-key
   sorting?
8. How many times is a `key=` function called per element?
9. When is a generator expression better than a list comprehension, and when is
   it worse?
10. Name the container for: a sliding window of the last 100 items; counting
    word frequencies; layered configuration; the 10 largest of a million.

---

## Exercises

1. **[`ex01_complexity.py`](exercises/ex01_complexity.py)** — Predict, then
   measure, the complexity of twelve operations. Plot the curves.
2. **[`ex02_comprehensions.py`](exercises/ex02_comprehensions.py)** — Fifteen
   loops to convert, and three comprehensions to convert *back* to loops
   because they should never have been comprehensions.
3. **[`ex03_grouping.py`](exercises/ex03_grouping.py)** — Build a small
   analytics pipeline over a realistic dataset using `Counter`, `defaultdict`,
   `sorted` with multi-keys, and set algebra.
4. **[`ex04_lru.py`](exercises/ex04_lru.py)** — Implement an LRU cache with
   O(1) get and put, using a `dict` plus a doubly linked list, then again with
   `OrderedDict`, and compare.

---

## Going deeper

- [TimeComplexity wiki](https://wiki.python.org/moin/TimeComplexity) — the table, authoritative
- [`collections`](https://docs.python.org/3/library/collections.html) and [`heapq`](https://docs.python.org/3/library/heapq.html)
- [Sorting HOW TO](https://docs.python.org/3/howto/sorting.html)
- Raymond Hettinger, "Modern Dictionaries" — the compact dict design explained by its author

---

**Next:** [Module 06 — Modules, Packages, and Project Layout](../06-modules-packages-projects/README.md)
