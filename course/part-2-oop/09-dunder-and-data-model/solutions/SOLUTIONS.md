# Solutions — Module 09

---

## Exercise 09.1 — Which dunder gets called?

| # | Output | Dunder | If missing |
|---|---|---|---|
| q01 | `__getitem__(0..3)`, `[10,20,30]` | `__getitem__` legacy iteration | With `__iter__`, that runs instead |
| q02 | two calls, `True` | `__getitem__` again | `__contains__` would be used if defined |
| q03 | `TypeError: has no len()` | `__len__` | No fallback. `len()` requires it. |
| q04 | nice string / `<object...>` / `[<object...>]` | `__str__`, `__repr__`, `__repr__` | `__str__` falls back to `__repr__`, never the reverse |
| q05 | one call, `falsy` | `__bool__` → falls back to `__len__` | With neither, always truthy |
| q06 | `[1,2,3]` then `[]` | `__iter__` returning `self` | — |
| q07 | `Vec.__mul__(3)`, `Vec(15)` | `__mul__` | — |
| q08 | `TypeError` | `int.__mul__` declines, then `Vec.__rmul__` — absent | Define `__rmul__` |
| q09 | `False`, `True` | `__eq__`; `!=` is derived by negation | — |
| q10 | `__exit__ got ValueError`, `we got here` | `__exit__` returning `True` **suppressed** it | — |
| q11 | `TypeError: has no len()` | Special methods are looked up on the **type** | — |
| q12 | `B.__eq__`, `True` | Subclass reflected method tried **first** | — |

Four that repay attention:

**q01–q03.** A class with only `__getitem__` is iterable and supports `in`, via
the legacy protocol that calls it with 0, 1, 2… until `IndexError`. It is *not*
sized — `len()` has no fallback at all. So "iterable" and "sized" are separate
capabilities, and a great many APIs assume both.

**q04.** `__str__` falls back to `__repr__`, never the reverse. A class with only
`__str__` prints as `<object at 0x...>` inside a list — exactly where you most
need to read it. Define `__repr__` first, always.

**q06.** Two `for` loops, and the second sees nothing. No exception, no warning.
This is why `__iter__` must return a *fresh* iterator (or be written as a
generator).

**q11.** Special methods are looked up on the **type**, not the instance. Setting
`instance.__len__` does nothing. This is why you cannot monkeypatch a dunder onto
a single object, and why mocking libraries need `MagicMock` specifically.

**q12** shows the refinement most people do not know: when the right operand's
type is a *proper subclass* of the left's, its reflected method is tried
**first**, so a subclass can override its parent's behaviour.

---

## Exercise 09.2 — Matrix

See [`ex02_matrix_solution.py`](ex02_matrix_solution.py). Five decisions:

**Immutable, therefore hashable — one decision, not two.** A mutable Matrix must
not be hashable (a mutated key becomes unreachable), and an immutable one may as
well be. It costs one method and makes matrices usable as memoisation keys.

**`type(self)(...)` for slices, not `Matrix(...)`.** A subclass slicing itself
gets its own type back rather than being silently downgraded.

**`len()` returns rows, `size` returns cells.** When two answers are defensible,
pick the one matching the nearest built-in (a nested list) and give the other an
explicit name.

**`__contains__` tests values, not rows.** The default derived from `__iter__`
would make `5 in m` False for a matrix full of fives — technically consistent,
completely surprising. NumPy, pandas and every spreadsheet treat a matrix as a
container of cells; match the mental model your users already have.

**`NotImplemented` versus `ValueError`, and this distinction is not arbitrary:**

- `NotImplemented` means *"I do not handle this type."* It is a message to the
  interpreter: try the reflected method, then raise `TypeError`. Returning it
  keeps the door open for a type written later to interoperate.
- `ValueError` means *"correct type, impossible value."* Adding a 2×3 to a 1×1 is
  not something another operand could rescue — it is a caller error and must be
  reported with the shapes.

Getting these backwards fails in both directions: `ValueError` where
`NotImplemented` belongs breaks interoperability silently; `NotImplemented` where
`ValueError` belongs produces `unsupported operand type(s) for +: 'Matrix' and
'Matrix'`, which is genuinely baffling.

---

## Exercise 09.3 — Broken equality and hashing

See [`ex03_eq_hash_solution.py`](ex03_eq_hash_solution.py). All five bugs break
one of three rules, and all three are consequences of how a hash table works
rather than conventions to memorise:

> **R1** Equal objects must have equal hashes.
> **R2** A hashed value must not change while the object is in a hash container.
> **R3** `__eq__` must return `NotImplemented`, not `False`, for unknown types.

**1. `__eq__` without `__hash__`.** Python sets `__hash__ = None` deliberately:
the default hash is identity-based, so two objects your `__eq__` calls equal
would hash differently, breaking R1. Rather than let you build unreachable dict
entries silently, Python makes the failure immediate.

**2. Hash and eq disagreeing** produces a dict containing two keys that are equal
to each other — supposed to be impossible, and every downstream assumption about
key uniqueness is now false.

**3. Mutable hashed state.** Insert, rename, and the object sits in a bucket
chosen by its old hash while lookup computes the new one. `len()` proves it is
there; lookup cannot find it. Three fixes, best first: make it immutable (the bug
becomes unrepresentable); hash an immutable identity instead; or
remove-mutate-reinsert at every call site (correct and fragile — one forgotten
site restores the bug).

**4. `False` instead of `NotImplemented`** makes equality **asymmetric**:
`Cents(500) == Money(500)` is True while `Money(500) == Cents(500)` is False,
because the first returns a definitive False and Python never asks the other
side. Asymmetric equality breaks sorting, set membership, and every caller's
assumptions.

**5. A constant hash is correct and pathological.** It satisfies R1, so nothing
is unreachable — but every object lands in one bucket and the hash table
degenerates into a linked list. The measured cost in the solution:

```
good hash       3600 items, 2000 lookups:    0.31 ms
constant hash   3600 items, 2000 lookups:  610.19 ms      ~2000x
```

O(1) has become O(n) with no error and no warning, only a program that gets
slower as it grows. The same thing happens *accidentally* when you hash a field
with few distinct values — a status enum, a boolean, a truncated timestamp.

---

## Exercise 09.4 — Context managers

Four points the exercise is built around:

**`try/finally`, not `try/except`, in a `@contextmanager`.** The cleanup must run
on both paths; `except` alone silently drops the clean case, and catching to
re-raise adds nothing.

**`perf_counter`, not `time`.** `time.time()` is wall-clock and can jump
backwards (NTP corrections, DST, manual changes), producing negative durations.
`perf_counter` is monotonic and is the only correct choice for measuring
intervals.

**`__exit__` must re-raise on rollback.** "The rollback handled it" is exactly
wrong: rolling back undoes the *data* changes, but the caller still needs to know
the operation failed. Suppressing turns a failed transaction into a silent no-op
that returns as if it succeeded.

**The cleanup-fails-too case.** If both the block and the cleanup raise, the
cleanup's exception replaces the block's, and the original — the one that
explains what went wrong — is lost. Wrap risky cleanup in its own `try` and log
rather than raise, or use `contextlib.ExitStack`, which handles this correctly.

**Why `contextlib.suppress` is a legitimate `return True`:** suppression is its
*stated single purpose*, it is narrowly scoped to named exception types, and the
name says so at every call site. Almost every other `return True` is a bug
because it suppresses invisibly — a reader of the `with` block has no indication
that exceptions vanish.

---

## Exercise 09.5 — FrozenDict

The three abstract methods `collections.abc.Mapping` requires are `__getitem__`,
`__len__` and `__iter__`. In exchange you get `get`, `keys`, `values`, `items`,
`__contains__`, `__eq__` and `__ne__` — the argument for inheriting from an ABC
rather than reimplementing a protocol by hand.

**The hash is the interesting part.** `hash(frozenset(self.items()))` solves
ordering in one step: a frozenset has no order, so `{"a":1,"b":2}` and
`{"b":2,"a":1}` produce the same hash — which they must, because `Mapping.__eq__`
says they are equal. Building it from `tuple(sorted(...))` also works but breaks
on unorderable keys.

**Raise `TypeError` if any value is unhashable.** `FrozenDict({"a": [1,2]})`
cannot honestly claim to be hashable, and `frozenset` will raise anyway — the
point is to let it, rather than catching and returning something wrong.

**Cache the hash.** It is O(n), and hashable objects get hashed repeatedly.

**`MappingProxyType` versus `FrozenDict` — two real differences:** a proxy is a
*live view* of a dict someone else can still mutate (Module 02), and a proxy is
**not hashable**, so it cannot be a dict key. `FrozenDict` owns a private copy
and is hashable. Use the proxy for cheap read-only exposure of state you own; use
`FrozenDict` when it must be a key or must never change.

**Should `FrozenDict({"a": 1}) == {"a": 1}` be True?** Yes.
`Mapping.__eq__` compares items, and a `FrozenDict` and a `dict` with the same
contents *are* the same mapping. Note this does not violate the hash rule: a
`dict` is unhashable, so the two can never both be keys in the same container,
and R1 is never tested.
