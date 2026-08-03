# Solutions — Module 02

---

## Exercise 02.1 — The identity lab

| # | Output | Mechanism |
|---|---|---|
| q01 | `[1, 2, 3, 4]` | `b = a` binds a second name to one object; `append` mutates it |
| q02 | `[1, 2, 3]` | `b = [...]` rebinds `b` only; `a` still points at the original |
| q03 | `[1, 2, 3] True` | `+=` on a list calls `__iadd__`, which mutates in place |
| q04 | `[1, 2] False` | `b + [3]` builds a new list; the assignment rebinds `b` |
| q05 | `(1, 2) (1, 2, 3) False` | tuple has no `__iadd__`, so `+=` degrades to `u = u + (3,)` |
| q06 | `[[1,0,0],[1,0,0],[1,0,0]]` | `* 3` repeats the *reference*; one inner list, three arrows |
| q07 | `['a'] ['a','b'] ['a','b','c']` | the default list is created once, at `def` time |
| q08 | `[[1,2,99],[3,4]] [[1,2],[3,4]]` | shallow copy shares inner lists; deep copy does not |
| q09 | `True False` | small-int caching covers -5..256; 1000 gets fresh objects |
| q10 | `([1,2,3], 'x')` then `TypeError` | the tuple's *references* are fixed; the list they point at is not |
| q11 | `[1, 3, 5]` | mutating while iterating: the index advances as the list shrinks |
| q12 | `[1, 2, 3] None [1, 2, 3]` | `.sort()` mutates and returns `None`; `sorted()` returns a new list |

Three worth dwelling on.

**q03 vs q04.** These two lines are equivalent in most languages and are not in
Python. `+=` is not sugar for `x = x + y`; it is `x = x.__iadd__(y)` when the
type defines `__iadd__`, falling back to `x = x.__add__(y)` when it does not.
Mutable containers define it (in-place, shared effects); immutable ones do not
(new object, rebinding). The consequence: `+=` inside a function *can* affect
the caller, for a list, and *cannot*, for a tuple or int. That is why q05 exists.

**q11.** This one does not raise. It silently produces a wrong answer, which is
strictly worse. The iterator holds an index; `remove` shifts elements left; the
index moves right. Element 4 slides into the position the iterator already
passed. The dict version *does* raise `RuntimeError`, which is why dicts are
easier to debug here than lists. **Never mutate a sequence you are iterating.**
Build a new one, or iterate a snapshot: `for n in list(nums):`.

**q12.** Python's convention: **a method that mutates in place returns `None`.**
`list.sort`, `list.reverse`, `list.append`, `dict.update`, `random.shuffle`,
`set.add`. This is deliberate — it makes `x = lst.sort()` fail loudly instead of
silently binding `None`. The paired non-mutating versions return new objects:
`sorted()`, `reversed()`. When you find yourself writing `x = something.verb()`
and getting `None`, this is why.

### Scoring

- **11-12**: solid. Move on.
- **9-10**: fine. Note which ones you missed and why.
- **6-8**: re-read sections 2 through 6 with a REPL open before Module 03. This
  material is load-bearing for everything after it.
- **Below 6**: this is normal for someone arriving from a language with value
  semantics, and it is exactly why the module exists. Redo the exercise
  tomorrow, cold. The second attempt is the one that sticks.

---

## Exercise 02.2 — Six aliasing bugs

See [`ex02_aliasing_bugs_solution.py`](ex02_aliasing_bugs_solution.py) — every
fix is annotated with its cause, and each has the test that catches it.

The pattern across all six: **a mutable object crossed a boundary it should not
have.** Into a default argument, out of a getter, out of a shallow copy, into a
loop that was iterating it. When you review Python code, "who else can reach
this object?" is the question that finds this whole class of bug.

Three additional notes.

**Bug 2 has two leaks, not one.** Most people find the getter and miss the
constructor. `self._tracks = tracks` means the caller retains a live handle to
your internal state. Copy on the way in *and* on the way out. The underscore on
`_tracks` is a naming convention that documents intent; it enforces nothing.

**Bug 3 is the most dangerous of the six** because it corrupts a module-level
default. The symptom appears in a completely unrelated part of the program,
possibly hours later, possibly only in production where the code path that
mutates it actually runs. `dict.copy()` is shallow — one level. For anything
nested, use `deepcopy`, a recursive merge, or (best) make the default
structurally immutable so the write raises instead of silently succeeding.

**Bug 6 is two bugs stacked.** `ordered = scores` does not copy, and `.sort()`
mutates. Either alone would be a bug; together, a function documented as "without
disturbing the caller's list" reorders it. `sorted(scores, reverse=True)[:n]`
fixes both in one expression. (For large lists, `heapq.nlargest(n, scores)` is
O(n log k) rather than O(n log n) — Module 05.)

---

## Exercise 02.3 — Copy semantics

See [`ex03_copy_semantics_solution.py`](ex03_copy_semantics_solution.py).

Typical measured result on a small config:

```
shallow (copy + update)     0.14us     1.0x
recursive merge             1.30us     9.3x
freeze                      2.13us    15.3x
deepcopy                    7.34us    52.9x
```

The intended conclusion is not "use the fast one". It is that **a 50x ratio on a
7-microsecond operation is not a performance problem.** At 1000 requests per
second, choosing `deepcopy` costs about 0.7 percent of one core. People avoid
`deepcopy` on the strength of the ratio and end up shipping the shallow-copy bug
from bug 3, which costs a production incident. Measure the absolute cost against
your actual call rate, then decide. This is Module 23's lesson arriving early.

`deepcopy`'s two genuine hazards are correctness ones, not speed ones:

1. It recurses through **everything reachable**, including things that must not
   be duplicated — sockets, file handles, locks, DB connections, or a parent
   pointer that drags in the entire object graph. Types that must not be copied
   define `__deepcopy__` to return `self`; yours may need to.
2. It handles cycles correctly via a `memo` dict keyed on `id()`, which is worth
   knowing because it means the copy preserves the *shape* of shared references
   inside the structure, not just the values.

`MappingProxyType` is a **view, not a snapshot**. It blocks writes through the
proxy; the underlying dict remains writable by anyone holding it, and those
writes are visible through the proxy. It protects against accident, not against
a caller who kept the original. For real immutability, copy first, or use a
frozen dataclass (Module 11).

---

## Exercise 02.4 — Sentinels

See [`ex04_sentinel_solution.py`](ex04_sentinel_solution.py).

The key realisation: `None` is an ordinary object that callers may legitimately
want to store or pass. The moment it is a valid *value*, it can no longer serve
as your "absent" *marker*. You need an object nobody else can produce, and
identity (`is`) is the only test that cannot be forged.

Three implementations, increasing in quality:

```python
MISSING = object()              # works; reprs as <object object at 0x...>
MISSING = "__missing__"         # broken; a caller can pass that exact string
class _Missing: ...             # best; nice repr, annotatable, singleton
MISSING = _Missing()
```

The subtlety the exercise's `has()` method forces you to discover: **you cannot
reuse the public sentinel as an internal probe.** `MISSING` already means "no
default given", so passing it to `get()` triggers the `KeyError` branch. `has()`
needs its own private `object()`. A sentinel is unambiguous only within the
protocol that defines it; distinguishing more states needs more sentinels.

`update_user` is the PATCH problem. JSON has one `null`, but an API needs to
distinguish "field absent, leave it alone" from "field present and null, clear
it". Every serious API framework solves this with a sentinel: Pydantic exposes
`model_fields_set`, the OpenAPI generators emit an `Unset` type, and GraphQL
sidesteps it with explicit field selection. You will meet it again in Module 28.

---

## Exercise 02.5 — Reference counting, cycles, weakref

See [`ex05_refcount_lab_solution.py`](ex05_refcount_lab_solution.py); the full
answers are in the `ANSWERS` string at the bottom of that file. The five points
worth carrying forward:

1. **`getrefcount` always reports one extra** — passing the object to the
   function created a temporary reference. Read the deltas, not the absolute.

2. **Destruction is immediate under refcounting.** `del` on the last name calls
   `__del__` synchronously, inside the `del` statement. This is a real CPython
   advantage and a real trap: it stops being true the moment the object is in a
   cycle, is captured by a traceback, or is running on PyPy.

3. **A cycle is unreachable but not freed** until the generational collector
   runs. In a long-running service this shows up as memory that climbs between
   collections and GC pauses that grow with the surviving object count.

4. **A dead weakref returns `None` when called.** Every holder must check.
   Never write `self._ref().method()` — the object can vanish between two lines
   of your own code if another thread drops the last strong reference.

5. **`gc.get_referrers(obj)` answers "what is keeping this alive?"** — the
   actual first tool for a growing-memory investigation. Combine it with
   `tracemalloc` snapshots (Module 23) to see what is growing, then
   `get_referrers` to see why.

The four classic unintended-strong-reference bugs, all of which you will meet:
an unbounded module-level cache dict; a listener registry holding strong
references to "unsubscribed" objects; a stored exception dragging in every frame
and local on the stack via its traceback; and logging or metrics stashing whole
request objects.
