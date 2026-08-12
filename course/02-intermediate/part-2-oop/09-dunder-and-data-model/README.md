# Module 09 — The Data Model: Dunder Methods

**Time budget:** 6 hours lesson, 8 hours exercises
**Prerequisite:** Module 08

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

Python has almost no special syntax. It has **protocols**, and every piece of
syntax is a call to a dunder method:

| You write | Python calls |
|---|---|
| `len(x)` | `x.__len__()` |
| `x[k]` | `x.__getitem__(k)` |
| `x + y` | `x.__add__(y)`, then `y.__radd__(x)` |
| `x == y` | `x.__eq__(y)`, then `y.__eq__(x)` |
| `for i in x` | `x.__iter__()`, then `__next__` repeatedly |
| `k in x` | `x.__contains__(k)`, or falls back to iteration |
| `with x:` | `x.__enter__()` / `x.__exit__(...)` |
| `x(...)` | `x.__call__(...)` |
| `print(x)` | `x.__str__()`, falling back to `__repr__` |
| `f"{x}"` | `x.__format__(spec)` |
| `bool(x)` | `x.__bool__()`, or `__len__`, or `True` |

This is what "Pythonic" actually means: **your types participate in the same
protocols as the built-in ones.** A class implementing `__len__` and
`__getitem__` works with `len()`, indexing, slicing, iteration, `in`,
`reversed()`, and every function that takes a sequence — without inheriting from
anything.

---

## 1. `__repr__` and `__str__`

Implement `__repr__` on every class you write. It costs one line and it pays
back in every debugging session.

```python
class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x, self.y = x, y

    def __repr__(self) -> str:
        return f"Point(x={self.x!r}, y={self.y!r})"    # for DEVELOPERS

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"                  # for USERS
```

| | `__repr__` | `__str__` |
|---|---|---|
| Audience | Developers | End users |
| Goal | Unambiguous | Readable |
| Called by | REPL, `repr()`, containers, debuggers, logging | `print()`, `str()`, f-strings |
| Default | `<Point object at 0x7f...>` | Falls back to `__repr__` |
| Ideal | Valid Python that reconstructs the object | Whatever reads best |

Define `__repr__` always; define `__str__` only when the user-facing form
genuinely differs.

**The rule that matters:** a container's `str()` uses its elements' `repr()`.

```python
>>> print([Point(1, 2)])
[Point(x=1, y=2)]           # __repr__, not __str__
```

So a class with only `__str__` still prints as `<object at 0x...>` inside a
list, which is exactly when you most need to see it. And use `!r` inside your
repr: `f"{self.name!r}"` shows `'Ada'` rather than `Ada`, which distinguishes an
empty string from a missing value.

---

## 2. `__eq__` and `__hash__` are a pair

```python
class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x, self.y = x, y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented          # let the OTHER side try
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))      # hash what __eq__ compares
```

**Three rules, and violating any one causes silent, hard-to-find bugs:**

1. **Equal objects must have equal hashes.** If not, a dict looks in the wrong
   bucket and your key becomes unreachable — present in memory, invisible to
   lookup.
2. **Only hash immutable state.** If a hashed attribute changes after insertion,
   the same unreachable-entry bug appears.
3. **Defining `__eq__` sets `__hash__` to `None`.** Python does this
   deliberately, because a default identity hash would violate rule 1. Your
   class becomes unhashable unless you define `__hash__` too:

```python
class Bad:
    def __eq__(self, other): return True

{Bad()}     # TypeError: unhashable type: 'Bad'
```

**Return `NotImplemented`, not `False`, for unknown types.** `NotImplemented`
tells Python "I do not know", so it tries `other.__eq__(self)` before falling
back to identity. Returning `False` claims authority you do not have and breaks
comparison with types written to interoperate with yours.

`@dataclass` generates all of this correctly (Module 11), which is the main
reason to use it.

---

## 3. Ordering

```python
from functools import total_ordering

@total_ordering
class Version:
    def __init__(self, major: int, minor: int, patch: int) -> None:
        self.parts = (major, minor, patch)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return self.parts == other.parts

    def __lt__(self, other: "Version") -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return self.parts < other.parts

    def __hash__(self) -> int:
        return hash(self.parts)
```

`@total_ordering` derives `<=`, `>`, `>=` from `__lt__` and `__eq__`. The
derived versions are slightly slower (each is two calls); define all six by hand
only if profiling says so.

Tuple comparison does most of the work for you: `(1, 2, 3) < (1, 3, 0)` compares
element by element, short-circuiting at the first difference. Comparing tuples of
your fields is almost always the right implementation.

Note that `sorted()` needs only `__lt__`, and `max`/`min` need only `__gt__`/
`__lt__`. You do not always need the full set.

---

## 4. The container protocols

```python
class Deck:
    def __init__(self, cards: list[str]) -> None:
        self._cards = list(cards)

    def __len__(self) -> int:                 # len(deck)
        return len(self._cards)

    def __getitem__(self, index):             # deck[0], deck[1:3]
        return self._cards[index]             # slices work for free

    def __setitem__(self, index, value) -> None:
        self._cards[index] = value

    def __delitem__(self, index) -> None:
        del self._cards[index]

    def __contains__(self, card: str) -> bool:  # "AS" in deck
        return card in self._cards

    def __iter__(self):                        # for card in deck
        return iter(self._cards)

    def __reversed__(self):                    # reversed(deck)
        return reversed(self._cards)
```

**`__getitem__` alone gives you a great deal.** Without `__iter__`, Python falls
back to calling `__getitem__` with 0, 1, 2, ... until `IndexError`. So iteration,
`in`, `list()`, and unpacking all work from `__getitem__` alone. This is the old
protocol, kept for compatibility — implement `__iter__` explicitly anyway,
because the fallback only works for integer-indexed sequences and produces
confusing errors when it does not apply.

**Handling slices:** `__getitem__` receives a `slice` object for `deck[1:3]`.
Delegating to a list (as above) handles it automatically. If you build the result
yourself, return **your own type** for a slice and a single element for an int:

```python
def __getitem__(self, index):
    if isinstance(index, slice):
        return type(self)(self._cards[index])     # type(self), not Deck --
    return self._cards[index]                     # subclasses get their type
```

---

## 5. Iteration

```python
class Countdown:
    def __init__(self, start: int) -> None:
        self.start = start

    def __iter__(self):
        return CountdownIterator(self.start)      # a FRESH iterator each time


class CountdownIterator:
    def __init__(self, current: int) -> None:
        self.current = current

    def __iter__(self):
        return self                                # iterators return themselves

    def __next__(self) -> int:
        if self.current <= 0:
            raise StopIteration                    # the protocol's "done"
        self.current -= 1
        return self.current + 1
```

**Iterable versus iterator** is the distinction that matters:

| | Iterable | Iterator |
|---|---|---|
| Defines | `__iter__` | `__iter__` **and** `__next__` |
| Reusable | Yes — a fresh iterator each time | **No.** Once exhausted, done. |
| Examples | `list`, `dict`, `str`, `range` | `iter([])`, a generator, a file object |

Making a class its own iterator (returning `self` from `__iter__` and keeping the
position on the instance) means **two `for` loops over it cannot both work** —
the second sees an exhausted object. That is a real and confusing bug. Return a
fresh iterator, or write `__iter__` as a generator, which does it for you:

```python
    def __iter__(self):
        current = self.start          # local state -> fresh each call
        while current > 0:
            yield current
            current -= 1
```

Module 14 covers generators properly.

---

## 6. Context managers

```python
class Timer:
    def __enter__(self) -> "Timer":
        self.start = time.perf_counter()
        return self                    # what `as x` binds

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        self.elapsed = time.perf_counter() - self.start
        return False                   # False/None: do NOT suppress exceptions
```

`__exit__` runs **whether or not** an exception occurred — that is the entire
point. Its three arguments are `None, None, None` on a clean exit.

**Returning `True` from `__exit__` swallows the exception.** Almost always
wrong. Do it only when suppression is the explicit purpose, as in
`contextlib.suppress`.

The concise form, which is what you will actually write (Module 15):

```python
from contextlib import contextmanager

@contextmanager
def timer():
    start = time.perf_counter()
    try:
        yield
    finally:                      # finally, not bare -- runs on exception too
        print(f"{time.perf_counter() - start:.3f}s")
```

---

## 7. Operators

```python
class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.x, self.y = x, y

    def __add__(self, other: "Vector") -> "Vector":
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> "Vector":
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vector(self.x * scalar, self.y * scalar)

    __rmul__ = __mul__            # makes 3 * v work as well as v * 3

    def __neg__(self) -> "Vector":
        return Vector(-self.x, -self.y)

    def __abs__(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5
```

**How Python resolves `a + b`:**

1. Try `type(a).__add__(a, b)`. If it returns `NotImplemented`, continue.
2. Try `type(b).__radd__(b, a)`. If that also returns `NotImplemented`:
3. `TypeError: unsupported operand type(s)`.

(With one refinement: if `type(b)` is a *subclass* of `type(a)`, the reflected
method is tried first, so a subclass can override its parent's behaviour.)

This is why `NotImplemented` matters. Returning it is how you say "not my
problem" and let the other operand try. Note the trap: `NotImplemented` is
**truthy**, so accidentally returning it from `__eq__` and using the result in an
`if` gives you a silent wrong answer plus a `DeprecationWarning`.

**In-place operators** (`__iadd__` etc.) should mutate and `return self` — for a
mutable type. For an immutable one, omit them and Python falls back to
`__add__` plus rebinding. This is exactly Module 02's list-versus-tuple `+=`
distinction, now from the implementer's side.

Only overload operators where the meaning is obvious. `Vector + Vector` is
clear. `User + User` is not, and a `merge()` method would be better.

---

## 8. `__call__`, `__bool__`, `__format__`

```python
class Multiplier:
    def __init__(self, factor: int) -> None:
        self.factor = factor

    def __call__(self, x: int) -> int:          # instances become callable
        return x * self.factor

double = Multiplier(2)
double(21)                                       # 42
```

`__call__` gives you a function with state and a useful `repr` — often clearer
than a closure when the state is inspectable, and the basis for class-based
decorators.

```python
    def __bool__(self) -> bool:
        return bool(self._items)      # else falls back to __len__, else True

    def __format__(self, spec: str) -> str:
        if spec == "short":
            return self.name[:8]
        return format(str(self), spec)          # delegate the rest
```

`__format__` powers `f"{obj:spec}"`. Useful for domain types with conventional
renderings — dates, money, durations.

---

## 9. The whole map

| Group | Methods |
|---|---|
| Representation | `__repr__` `__str__` `__format__` `__bytes__` |
| Comparison | `__eq__` `__ne__` `__lt__` `__le__` `__gt__` `__ge__` `__hash__` |
| Container | `__len__` `__getitem__` `__setitem__` `__delitem__` `__contains__` `__reversed__` |
| Iteration | `__iter__` `__next__` `__aiter__` `__anext__` |
| Numeric | `__add__` `__sub__` `__mul__` `__truediv__` `__floordiv__` `__mod__` `__pow__` `__neg__` `__abs__` `__round__` and the `__r*__` / `__i*__` variants |
| Conversion | `__bool__` `__int__` `__float__` `__index__` `__complex__` |
| Context | `__enter__` `__exit__` `__aenter__` `__aexit__` |
| Callable | `__call__` |
| Attributes | `__getattr__` `__getattribute__` `__setattr__` `__delattr__` `__dir__` |
| Descriptors | `__get__` `__set__` `__delete__` `__set_name__` |
| Class machinery | `__init__` `__new__` `__init_subclass__` `__class_getitem__` `__slots__` |
| Copying | `__copy__` `__deepcopy__` `__reduce__` |
| Pattern matching | `__match_args__` |

You do not need to memorise this. You need to know it exists, so that when you
want your type to work with some piece of syntax, you look up which method
provides it.

---

## Common mistakes in this module

| Mistake | Symptom | Fix |
|---|---|---|
| `__eq__` without `__hash__` | `TypeError: unhashable type` | Define both, or `frozen=True` |
| Hashing mutable state | Dict key becomes unreachable | Hash only immutable fields |
| Returning `False` from `__eq__` for other types | Breaks interop, `NotImplemented` is truthy | Return `NotImplemented` |
| Only `__str__`, no `__repr__` | `<object at 0x...>` in every list and debugger | Always define `__repr__` |
| `__iter__` returning `self` with instance state | Second loop sees nothing | Return a fresh iterator, or use `yield` |
| `__exit__` returning `True` | Exceptions silently swallowed | Return `False`/`None` |
| No `__radd__` | `3 * v` fails while `v * 3` works | Add the reflected method |
| Expensive `__len__` or `__bool__` | Slow truthiness checks in loops | Cache, or do not implement |
| `__getitem__` ignoring slices | `obj[1:3]` returns something wrong | Handle `slice` explicitly |
| `__repr__` raising | Debugging becomes impossible | Make it total; never raise |
| Overloading an operator with no obvious meaning | Unreadable code | Use a named method |

---

## Self-check quiz

1. When is `__repr__` used instead of `__str__`? Give three callers of each.
2. Why does defining `__eq__` set `__hash__` to `None`?
3. What are the two rules relating `__eq__` and `__hash__`, and what breaks when
   each is violated?
4. Why return `NotImplemented` rather than `False` from `__eq__`? What is the
   extra hazard with `NotImplemented`?
5. Describe the full resolution order for `a + b`.
6. What is the difference between an iterable and an iterator?
7. Why does returning `self` from `__iter__` break a second loop?
8. What does returning `True` from `__exit__` do, and when is it right?
9. Which methods must you define for `sorted()` to work? For `sorted(reverse=True)`?
10. If a class defines only `__getitem__`, what syntax works, and why?

---

## Exercises

1. **[`ex01_protocols.py`](exercises/ex01_protocols.py)** — Twelve predictions
   about which dunder each syntax calls, including the fallbacks.
2. **[`ex02_matrix.py`](exercises/ex02_matrix.py)** — Build a `Matrix` type
   supporting `+`, `*`, `==`, indexing with tuples, slicing, iteration, `len`,
   `repr`, and `format`.
3. **[`ex03_eq_hash.py`](exercises/ex03_eq_hash.py)** — Five classes with broken
   equality or hashing. Find the bug, fix it, prove it with a dict.
4. **[`ex04_context.py`](exercises/ex04_context.py)** — Four context managers:
   a timer, a transaction with rollback, a temporary directory, and a
   suppressor. Both class-based and `@contextmanager`.
5. **[`ex05_frozen_dict.py`](exercises/ex05_frozen_dict.py)** — A hashable,
   immutable mapping that works everywhere a `dict` does, and can be a dict key.

---

## Going deeper

- [The Python Data Model](https://docs.python.org/3/reference/datamodel.html) — read the whole chapter now
- [`collections.abc`](https://docs.python.org/3/library/collections.abc.html) — the protocol table with required methods
- [`functools.total_ordering`](https://docs.python.org/3/library/functools.html#functools.total_ordering)
- Luciano Ramalho, *Fluent Python*, chapters 1 and 11-16 — the best treatment of
  this material in print

---

**Next:** [Module 10 — Inheritance, Composition, and the MRO](../10-inheritance-composition-mro/README.md)
