# Module 11 — Dataclasses, Enums, and Value Semantics

**Time budget:** 4 hours lesson, 6 hours exercises
**Prerequisite:** Modules 08, 09, 10

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

Most classes are records: a bundle of fields plus a little behaviour. Written by
hand, a good one needs `__init__`, `__repr__`, `__eq__`, `__hash__`, ordering,
and validation — thirty lines of boilerplate in which any typo is a silent bug.

`@dataclass` generates all of it correctly, and generating it correctly matters:
the `__eq__`/`__hash__` contract from Module 09 is easy to break by hand and
impossible to break with `frozen=True`.

This module is also where **immutability becomes a design tool** rather than a
constraint.

---

## 1. `@dataclass`

```python
from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float
    label: str = ""
```

That generates `__init__`, `__repr__`, and `__eq__`. The annotations are not
decoration — the decorator reads `__annotations__` at class creation time to
find the fields, which is why a field without an annotation is silently ignored:

```python
@dataclass
class Broken:
    x: int
    y = 0            # NO annotation -> a class attribute, NOT a field
                     # It will not appear in __init__, __repr__ or __eq__.
```

### The options that matter

```python
@dataclass(
    frozen=True,      # immutable: __setattr__ raises; also generates __hash__
    slots=True,       # 3.10+: generate __slots__, saving ~40% memory
    order=True,       # generate __lt__, __le__, __gt__, __ge__ from field order
    kw_only=True,     # 3.10+: all fields keyword-only at the call site
    eq=True,          # default; set False to keep identity comparison
    repr=True,        # default
)
```

**`frozen=True` should be your default.** It gives you `__hash__` for free,
makes aliasing bugs (Module 02) unrepresentable, and makes the object safe to
share between threads (Module 21) and to use as a dict key or cache key.

**`slots=True` costs nothing** for a data-shaped class and saves real memory
(Module 08). The exception is anything needing `cached_property` or `weakref`.

**`kw_only=True` for anything with more than three fields.**
`Config(30, 3, True, False)` is unreadable; `Config(timeout=30, retries=3, ...)`
is not.

**`order=True` compares fields in declaration order**, as a tuple. If that is
not the ordering you want, write `__lt__` yourself — silently sorting by the
wrong field is worse than not sorting.

### `field()`

```python
@dataclass
class Config:
    name: str
    tags: list[str] = field(default_factory=list)      # NOT `= []`
    _cache: dict = field(default_factory=dict, repr=False, compare=False)
    created: datetime = field(default_factory=datetime.now)
    version: int = field(default=1, metadata={"docs": "schema version"})
```

`default_factory` runs **per instance**, which is the fix for Module 02's
mutable-default trap. `@dataclass` refuses a mutable default outright:

```python
@dataclass
class Bad:
    items: list = []      # ValueError: mutable default <class 'list'> ...
```

That is one of the nicest things about dataclasses: a whole bug category becomes
a startup error.

`compare=False` excludes a field from `__eq__` and ordering — right for caches,
timestamps, and derived values. `repr=False` keeps secrets out of logs
(Module 08).

### `__post_init__`

```python
@dataclass(frozen=True)
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)        # computed, not passed in

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError(f"dimensions must be positive: {self}")
        object.__setattr__(self, "area", self.width * self.height)
        # object.__setattr__ because frozen blocks the normal assignment.
        # This is the documented way to set computed fields on a frozen
        # dataclass, and it is the one place you should use it.
```

Validation in `__post_init__` means **an invalid instance cannot exist**
(Module 08's rule), and every caller — the constructor, the deserializer, the
test fixture — gets it.

### Working with instances

```python
from dataclasses import replace, asdict, astuple, fields

p2 = replace(p, x=10)          # a NEW instance with one field changed
asdict(p)                       # recursive dict; follows nested dataclasses
astuple(p)                      # recursive tuple
[f.name for f in fields(p)]     # introspection
```

`replace()` is how you "modify" a frozen dataclass, and it is the pattern that
makes immutability practical.

Note that `asdict()` **deep-copies** everything, including nested dataclasses,
lists and dicts. That is usually what you want and occasionally an expensive
surprise.

---

## 2. Choosing a record type

| | `dict` | `NamedTuple` | `TypedDict` | `dataclass` | Pydantic |
|---|---|---|---|---|---|
| Fixed fields | no | yes | yes | yes | yes |
| Type-checked | no | yes | yes | yes | yes |
| Runtime validation | no | no | no | manual | **automatic** |
| Mutable | yes | no | yes | optional | optional |
| Attribute access | `d["x"]` | `t.x` | `d["x"]` | `o.x` | `o.x` |
| Methods | no | yes | no | yes | yes |
| Iterable/unpackable | keys | yes | keys | no | no |
| Cost | zero | zero | zero (a dict at runtime) | small | a dependency |

**The decision:**

- **`dict`** — genuinely dynamic keys, or data passing straight through.
- **`TypedDict`** — you must stay a `dict` (JSON in and out, an existing API)
  but want static checking. It *is* a dict at runtime; there is no validation.
- **`NamedTuple`** — a small immutable record that benefits from tuple
  behaviour: unpacking, indexing, use as a dict key. Returning multiple values
  from a function is the classic case.
- **`dataclass`** — the default for a record you own.
- **Pydantic** — data crossing a **trust boundary**: HTTP bodies, config files,
  message queues. It validates and coerces at runtime, which is exactly what a
  boundary needs and what a dataclass does not do. Module 28.

The distinction worth internalising: **a dataclass's type hints are checked by
mypy, not by Python.** `Point(x="not a number")` runs happily. Pydantic checks
at runtime. Use dataclasses inside your program, Pydantic at its edges.

---

## 3. `Enum`

```python
from enum import Enum, IntEnum, StrEnum, auto, Flag

class Status(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    CLOSED = "closed"

Status.ACTIVE           # <Status.ACTIVE: 'active'>
Status.ACTIVE.value     # 'active'
Status("active")        # lookup BY VALUE -> Status.ACTIVE
Status["ACTIVE"]        # lookup by NAME
list(Status)            # iterable, in definition order
```

Enums replace magic strings and give you three things a string cannot: a typo is
a `ValueError` at the boundary rather than a silent no-match, the valid set is
discoverable and iterable, and a type checker can verify exhaustiveness in a
`match`.

```python
class Priority(IntEnum):        # comparable and usable as an int
    LOW = 1
    HIGH = 3

Priority.HIGH > Priority.LOW    # True
sorted(tasks, key=lambda t: t.priority)

class Colour(StrEnum):          # 3.11+: IS a str, so it JSON-serialises
    RED = "red"

json.dumps({"c": Colour.RED})   # works; a plain Enum raises

class Perm(Flag):               # combinable
    READ = auto()
    WRITE = auto()
    ALL = READ | WRITE

Perm.READ in (Perm.READ | Perm.WRITE)     # True
```

`IntEnum` and `StrEnum` exist for interoperability with code that expects a
plain int or str — serialization, database columns, HTTP headers. Prefer plain
`Enum` unless you need that, because the looseness that makes them convenient
also lets `Status.ACTIVE == "active"` be True, which defeats part of the point.

Enums with behaviour are fine and underused:

```python
class Status(Enum):
    PENDING = "pending"
    ACTIVE = "active"

    @property
    def is_terminal(self) -> bool:
        return self is Status.CLOSED

    @classmethod
    def from_legacy_code(cls, code: int) -> "Status":
        return {0: cls.PENDING, 1: cls.ACTIVE}[code]
```

---

## 4. Value semantics

A **value object** is defined by its contents, not its identity. Two `Money`
objects holding $5 are interchangeable; two `BankAccount` objects with a $5
balance are not.

| | Value object | Entity |
|---|---|---|
| Identity | its contents | an ID that outlives changes |
| Equality | field by field | by ID |
| Mutability | immutable | usually mutable |
| Examples | `Money`, `Point`, `DateRange`, `Email` | `User`, `Order`, `Account` |
| Build with | `@dataclass(frozen=True)` | `@dataclass` with an id field |

**Prefer value objects.** The benefits compound:

- Aliasing bugs cannot happen (Module 02).
- Hashable, so usable as dict keys and cache keys.
- Thread-safe for free (Module 21) — no lock can be forgotten if there is
  nothing to protect.
- Trivially testable: construct, assert, done. No setup, no teardown.
- Easy to reason about: a value that cannot change cannot change *behind you*.

The objection is allocation cost. For records at ordinary scale it does not
matter; measure before you let it drive the design (Module 23).

### Making illegal states unrepresentable

```python
# weak: every consumer must re-check
@dataclass
class Order:
    status: str
    shipped_at: datetime | None = None

# strong: the type enforces it
@dataclass(frozen=True)
class Pending: ...

@dataclass(frozen=True)
class Shipped:
    shipped_at: datetime          # cannot be absent

Order = Pending | Shipped
```

In the second version, "shipped with no timestamp" cannot be constructed, so no
code needs to handle it and no test needs to cover it. Combined with `match`
(Module 04), the type checker verifies you handled every case.

This is the highest-leverage idea in Part 2: **push invariants into types, so
that the checking happens once at construction rather than everywhere else
forever.**

---

## 5. Copy semantics revisited

```python
import copy

@dataclass
class Team:
    name: str
    members: list[str]

a = Team("eng", ["ada"])
b = copy.copy(a)                # shallow: SAME list
b.members.append("bo")
a.members                        # ['ada', 'bo']   <-- Module 02 again

c = copy.deepcopy(a)            # independent
d = replace(a, name="ops")      # NEW object, but members is still SHARED
```

**`replace()` is a shallow copy.** It creates a new instance with the fields you
name changed and the rest **shared**. For a fully frozen structure that is
perfect and free. For one containing a mutable field, it is the shallow-copy
trap wearing a dataclass costume.

The fix is not to remember it — the fix is to make the fields immutable:

```python
@dataclass(frozen=True)
class Team:
    name: str
    members: tuple[str, ...] = ()      # tuple, not list
```

Now `replace()` is always safe, because nothing reachable can change. Note that
`frozen=True` alone would **not** have saved you: it prevents rebinding the
attribute, not mutating the list it points at. Module 02's tuple trap, one more
time, and it is the single most common dataclass mistake.

---

## Common mistakes in this module

| Mistake | Symptom | Fix |
|---|---|---|
| Field without an annotation | Silently not a field | `y: int = 0`, never `y = 0` |
| `= []` as a default | `ValueError` at class creation | `field(default_factory=list)` |
| `frozen=True` with a `list` field | Still mutable through the list | Use a `tuple` |
| Assuming type hints are enforced | `Point(x="abc")` works | mypy, or Pydantic at boundaries |
| `order=True` with the wrong field order | Sorted by the wrong key, silently | Reorder fields, or write `__lt__` |
| Mutable dataclass as a dict key | Unhashable, or an unreachable entry | `frozen=True` |
| `replace()` believed to be deep | Shared mutable state | Make fields immutable |
| `Enum` compared to its value | `Status.ACTIVE == "active"` is False | Compare enum to enum, or use `StrEnum` |
| Plain `Enum` in `json.dumps` | `TypeError: not JSON serializable` | `StrEnum`, or `.value` |
| Secrets in a dataclass `repr` | Credentials in logs | `field(repr=False)` |
| `__post_init__` assigning on a frozen class | `FrozenInstanceError` | `object.__setattr__` |

---

## Self-check quiz

1. Why is a field without an annotation silently ignored?
2. What does `frozen=True` give you beyond preventing assignment?
3. Why does `@dataclass` reject `items: list = []` outright?
4. When is `NamedTuple` a better choice than a frozen dataclass?
5. What does Pydantic do that a dataclass does not, and where does that matter?
6. Explain why `frozen=True` does not make a dataclass with a `list` field
   immutable.
7. What does `order=True` compare, and what is the risk?
8. When would you use `IntEnum` or `StrEnum` rather than `Enum`?
9. Define a value object and give the four benefits of preferring one.
10. What does "make illegal states unrepresentable" mean? Give an example.

---

## Exercises

1. **[`ex01_convert.py`](exercises/ex01_convert.py)** — Convert five hand-written
   classes to dataclasses. One of them should *not* be converted; identify it.
2. **[`ex02_choose.py`](exercises/ex02_choose.py)** — Eight scenarios. Pick
   `dict`, `TypedDict`, `NamedTuple`, `dataclass`, or Pydantic, and defend it.
3. **[`ex03_enums.py`](exercises/ex03_enums.py)** — Replace stringly-typed state
   handling with enums, including a `Flag` for permissions and an exhaustive
   `match`.
4. **[`ex04_value_objects.py`](exercises/ex04_value_objects.py)** — Build
   `Email`, `Money`, `DateRange` and `Percentage` as value objects that make
   invalid values unconstructible.

---

## Going deeper

- [`dataclasses`](https://docs.python.org/3/library/dataclasses.html)
- [`enum`](https://docs.python.org/3/library/enum.html) — including the excellent HOWTO
- [PEP 557 — Data Classes](https://peps.python.org/pep-0557/), especially the rejected-ideas section
- [attrs](https://www.attrs.org/) — the library dataclasses came from; still ahead on validators and converters

---

**Next:** [Module 12 — Design Principles in Python](../12-design-principles-in-python/README.md)
