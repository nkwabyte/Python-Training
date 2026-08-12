# Module 10 — Inheritance, Composition, and the MRO

**Time budget:** 6 hours lesson, 8 hours exercises
**Prerequisite:** Modules 08, 09

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

Inheritance is the most overused tool in object-oriented programming, and
Python's version has a mechanism — the MRO — that most people who use `super()`
daily could not describe.

Three things to take away:

1. `super()` does **not** mean "the parent class". It means "the next class in
   the MRO", which depends on the type of the *instance*, not on where the code
   is written.
2. Composition is the default. Inheritance is for when you genuinely need
   substitutability, and it is a much stronger commitment than it looks.
3. `Protocol` gives you interfaces without inheritance at all, which is usually
   what you actually wanted.

---

## 1. Is-a versus has-a

```python
class Engine:
    def start(self) -> str: return "vroom"

# COMPOSITION: a Car HAS an Engine
class Car:
    def __init__(self) -> None:
        self._engine = Engine()
    def start(self) -> str:
        return self._engine.start()

# INHERITANCE: a SportsCar IS a Car
class SportsCar(Car):
    def start(self) -> str:
        return self._engine.start().upper()
```

**The test for inheritance is not "does it share code".** It is the Liskov
substitution principle: *anywhere the base type is expected, an instance of the
subclass must work without the caller noticing.* If a subclass has to raise
`NotImplementedError` for an inherited method, weaken a guarantee, or document
"do not call this on subclass X", the relationship is not is-a.

The canonical failure:

```python
class Rectangle:
    def set_width(self, w): self.w = w
    def set_height(self, h): self.h = h

class Square(Rectangle):        # a square IS a rectangle, mathematically
    def set_width(self, w): self.w = self.h = w
    def set_height(self, h): self.w = self.h = h

def stretch(r: Rectangle) -> None:
    r.set_width(10); r.set_height(5)
    assert r.w * r.h == 50      # holds for Rectangle, fails for Square
```

Mathematics is not the criterion. **Behaviour under substitution is.**

### What inheritance actually commits you to

| You get | You also get |
|---|---|
| Code reuse | Every base method becomes part of your public API |
| `isinstance` passes | Base changes can break you silently |
| Polymorphic dispatch | The base's `__init__` contract, forever |
| A shared vocabulary | Tight coupling that is hard to unwind later |

Composition gives you the reuse without the rest, at the cost of a little
delegation code. That trade is almost always worth making.

---

## 2. `super()` and the MRO

```python
class A:
    def greet(self) -> str: return "A"

class B(A):
    def greet(self) -> str: return "B -> " + super().greet()

class C(A):
    def greet(self) -> str: return "C -> " + super().greet()

class D(B, C):
    def greet(self) -> str: return "D -> " + super().greet()

D().greet()          # 'D -> B -> C -> A'
D.__mro__            # (D, B, C, A, object)
```

**Look at `B.greet` again.** Its `super()` call went to `C`, not to `A` — even
though `B`'s only base is `A`, and `C` is nowhere in `B`'s definition. That is
the whole lesson:

> `super()` follows the MRO **of the instance's type**, not the class hierarchy
> written in the file.

This is why the mental model "super means my parent" is not merely imprecise but
actively wrong, and why cooperative multiple inheritance works at all.

### C3 linearisation

The MRO is computed by the C3 algorithm, which guarantees:

1. A class appears before all of its bases.
2. Bases appear in the order written.
3. The order is **monotonic** — a class's MRO is consistent with the MRO of
   every subclass.

If no order satisfies all three, the class statement raises at definition time:

```python
class X: pass
class Y(X): pass
class Z(X, Y): pass
# TypeError: Cannot create a consistent method resolution order (MRO)
```

That is Python refusing to build a hierarchy whose behaviour would be
ambiguous — a much better outcome than resolving it arbitrarily.

Read `SomeClass.__mro__` any time you are unsure. It is not something to
compute in your head.

### Cooperative inheritance

For multiple inheritance to work, **every** class in the chain must call
`super()`, and signatures must be compatible:

```python
class Base:
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)          # reaches object at the end

class Loggable:
    def __init__(self, *, log_level="INFO", **kwargs) -> None:
        self.log_level = log_level
        super().__init__(**kwargs)          # pass the rest ON

class Serializable:
    def __init__(self, *, fmt="json", **kwargs) -> None:
        self.fmt = fmt
        super().__init__(**kwargs)

class Widget(Loggable, Serializable, Base):
    def __init__(self, name: str, **kwargs) -> None:
        self.name = name
        super().__init__(**kwargs)

Widget("w", log_level="DEBUG", fmt="xml")
```

The `**kwargs` threading is what makes this work: each class consumes its own
keywords and passes the rest along. One class forgetting `super().__init__()`
silently breaks every class after it in the MRO — and "after it" is not visible
from that class's own source.

That fragility is the practical argument for keeping multiple inheritance to
**stateless mixins** (see below).

---

## 3. Mixins

A mixin adds behaviour to a class it knows nothing about.

```python
class ReprMixin:
    """Adds a useful __repr__ to any class with a __dict__."""
    def __repr__(self) -> str:
        args = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"{type(self).__name__}({args})"

class ComparableMixin:
    """Adds ordering from a _key() method the host class provides."""
    def _key(self):
        raise NotImplementedError
    def __lt__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._key() < other._key()

class Product(ReprMixin, ComparableMixin):
    def __init__(self, name: str, price: float) -> None:
        self.name, self.price = name, price
    def _key(self):
        return (self.price, self.name)
```

Rules that keep mixins from becoming a maze:

- **Mixins first in the bases list.** They must come before the concrete base in
  the MRO to be able to override it.
- **No state, or as little as possible.** A stateful mixin needs `__init__`
  cooperation, which is where multiple inheritance gets fragile.
- **Name them `-Mixin`.** The name is documentation.
- **Never instantiate one directly.** It is not a complete type.
- **Depend on a small, documented interface** (here: `_key`). Say what the host
  class must provide.

---

## 4. Abstract base classes

```python
from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def read(self, key: str) -> bytes: ...

    @abstractmethod
    def write(self, key: str, value: bytes) -> None: ...

    def read_text(self, key: str, encoding: str = "utf-8") -> str:
        return self.read(key).decode(encoding)      # a CONCRETE helper

class MemoryStorage(Storage):
    def __init__(self) -> None:
        self._data: dict[str, bytes] = {}
    def read(self, key: str) -> bytes:
        return self._data[key]
    def write(self, key: str, value: bytes) -> None:
        self._data[key] = value

Storage()          # TypeError: Can't instantiate abstract class
```

ABCs give you: instantiation refused until every abstract method is implemented,
shared concrete helpers, and `isinstance` working. The cost is that
implementations must **inherit** — which is fine inside your own codebase and a
real imposition on third-party types you do not control.

---

## 5. `Protocol`: interfaces without inheritance

```python
from typing import Protocol, runtime_checkable

class SupportsRead(Protocol):
    def read(self, key: str) -> bytes: ...

def load(storage: SupportsRead, key: str) -> bytes:
    return storage.read(key)
```

Any object with a matching `read` satisfies this — **no inheritance, no
registration, nothing imported by the implementer.** This is static duck typing:
the type checker verifies structurally, at compile time, what Python was already
doing dynamically at runtime.

| | ABC | Protocol |
|---|---|---|
| Implementer must inherit | Yes | No |
| Works with third-party types | No | Yes |
| Checked | At instantiation, runtime | By mypy, statically |
| `isinstance` | Always | Only with `@runtime_checkable`, and it checks method *names* only |
| Can provide implementations | Yes | Only defaults (3.8+), rarely used |

**Rule of thumb:** `Protocol` for describing what you *accept*; ABC for a family
of types you *own* and want to share code between. When in doubt, `Protocol` —
it couples less.

Note the `runtime_checkable` limitation: `isinstance` against a protocol checks
only that the attribute *names* exist, not their signatures. It is a weak check
and should not be relied on for correctness.

---

## 6. Duck typing, and when to stop `isinstance`

```python
def process(items):
    if isinstance(items, list):        # rejects tuples, sets, generators
        ...
```

That check makes your function worse. It rejects perfectly good arguments for no
benefit. Prefer:

- **Just use it.** If it quacks, it works, and a `TypeError` from the actual
  failure is more informative than yours.
- **`isinstance(x, collections.abc.Iterable)`** if you must check — test the
  *capability*, not the concrete class.
- **Type hints plus a type checker** for static verification with zero runtime
  cost.

`isinstance` is genuinely right in three places: implementing `__eq__` and the
arithmetic dunders (Module 09), dispatching on a closed set of types you own
(prefer `match` or `singledispatch`), and validating at a system boundary where
data arrives untyped.

---

## Common mistakes in this module

| Mistake | Symptom | Fix |
|---|---|---|
| Inheriting for code reuse | Fragile hierarchy, LSP violations | Compose, or extract a function |
| "`super()` is my parent" | Wrong method called in multiple inheritance | It is the next class in the MRO |
| Forgetting `super().__init__()` | Later classes silently uninitialised | Every class in the chain must cooperate |
| Mixin listed after the base | Mixin never overrides anything | Mixins first |
| Deep hierarchies | Nobody can find where a method comes from | Two levels is usually the limit |
| ABC where a Protocol fits | Third-party types cannot participate | `Protocol` |
| `isinstance(x, list)` | Rejects valid arguments | Check the capability, or do not check |
| Overriding with a narrower signature | Substitution breaks; mypy flags it | Accept at least what the base accepts |
| Mutable class attribute in a base | Shared across every subclass and instance | `__init__` |
| Calling an abstract method in `__init__` | Runs the subclass override before it is ready | Do not; use a factory |

---

## Self-check quiz

1. State the test for whether inheritance is appropriate.
2. In the diamond, why does `B.greet`'s `super()` reach `C`?
3. What three properties does C3 linearisation guarantee?
4. What happens when no consistent MRO exists, and when?
5. Why must every class in a cooperative chain call `super().__init__()`?
6. Why do mixins go first in the bases list?
7. Give two things an ABC does that a Protocol does not, and vice versa.
8. What exactly does `isinstance` check against a `runtime_checkable` Protocol?
9. Name three places `isinstance` is genuinely correct.
10. Why is Square/Rectangle a problem, given that a square *is* a rectangle?

---

## Exercises

1. **[`ex01_mro_lab.py`](exercises/ex01_mro_lab.py)** — Predict ten MROs and
   the output of `super()` chains, including one that fails to linearise.
2. **[`ex02_refactor.py`](exercises/ex02_refactor.py)** — A five-level
   inheritance hierarchy with three LSP violations. Convert it to composition.
3. **[`ex03_protocols.py`](exercises/ex03_protocols.py)** — Build the same
   plugin system three ways — ABC, Protocol, duck typing — and compare.
4. **[`ex04_mixins.py`](exercises/ex04_mixins.py)** — Write four mixins that
   compose cleanly, and one deliberately stateful one that does not. Explain.

---

## Going deeper

- [Python's MRO](https://docs.python.org/3/howto/mro.html) — the C3 algorithm, from the source
- [`abc`](https://docs.python.org/3/library/abc.html) and [`typing.Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)
- [PEP 544 — Protocols](https://peps.python.org/pep-0544/)
- Raymond Hettinger, "Super considered super!" — the definitive talk on `super()`

---

**Next:** [Module 11 — Dataclasses, Enums, and Value Semantics](../11-dataclasses-and-value-semantics/README.md)
