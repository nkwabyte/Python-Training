# Module 12 — Design Principles in Python

**Time budget:** 5 hours lesson, 6 hours exercises
**Prerequisite:** Modules 08-11

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

SOLID and the Gang of Four patterns were written for Java and C++ in the 1990s.
Applied literally to Python they produce ceremony without benefit, because
**Python has first-class functions, and about half the classic patterns exist
solely to work around not having them.**

This module translates the principles that survive, dissolves the patterns that
do not, and covers the three metaprogramming tools — descriptors,
`__init_subclass__`, metaclasses — with an honest account of when to use them,
which is rarely.

---

## 1. SOLID, translated

### S — Single responsibility

*A module should have one reason to change.* Survives intact, and applies to
functions and modules at least as much as to classes.

The practical test is not "does this class do one thing" (unanswerably vague) but
**"who asks for changes to this?"** If the finance team and the marketing team
both file tickets against one class, it has two responsibilities.

```python
class Report:                     # three reasons to change
    def fetch(self): ...          # the database team
    def calculate(self): ...      # the finance team
    def render_pdf(self): ...     # the design team
```

### O — Open/closed

*Open for extension, closed for modification.* In Java this means inheritance and
interfaces. **In Python it usually means a function argument.**

```python
# closed for modification: you never edit this
def process(items, transform=lambda x: x, key=None, on_error=None): ...

# extension is a registry, not a subclass
HANDLERS: dict[str, Callable[[Event], None]] = {}

def handles(event_type: str):
    def register(fn):
        HANDLERS[event_type] = fn
        return fn
    return register

@handles("click")
def on_click(event): ...
```

That registry is the Strategy pattern, the Command pattern, and half of the
Visitor pattern, in eight lines and with no classes.

### L — Liskov substitution

Covered in Module 10, and it applies unchanged. Python's dynamism makes it easier
to violate and no less costly when you do — the failure just moves from compile
time to runtime.

### I — Interface segregation

*No client should depend on methods it does not use.* This is where `Protocol`
shines (Module 10): define the **narrowest** interface your function actually
needs.

```python
class Readable(Protocol):
    def read(self, n: int) -> bytes: ...

def parse(source: Readable) -> Document: ...   # not "a File", just "readable"
```

Now a file, a socket, a `BytesIO`, and a test fake all qualify. Typing the
parameter as a concrete class instead would have excluded three of them for no
reason.

### D — Dependency inversion

*Depend on abstractions, not concretions.* In Python, the abstraction is usually
a **function parameter**, not an interface hierarchy:

```python
# concrete dependency: untestable without a database and a clock
class OrderService:
    def __init__(self):
        self.db = PostgresConnection("prod")
        self.clock = datetime.now

# inverted: the caller supplies both
class OrderService:
    def __init__(self, db: SupportsQuery, now: Callable[[], datetime] = datetime.now):
        self.db = db
        self.now = now
```

That second version is testable with a dict and a lambda. No framework, no
container, no annotations — this **is** dependency injection, and in Python it
needs no library.

---

## 2. Patterns that Python dissolves

| Pattern | In Java | In Python |
|---|---|---|
| **Strategy** | An interface + N classes | Pass a function |
| **Command** | An interface + N classes | Pass a function, or `partial` |
| **Factory** | A factory class | A function, or a `@classmethod` |
| **Abstract Factory** | Two class hierarchies | A dict of constructors |
| **Singleton** | Private ctor + static instance | A module. Modules are singletons. |
| **Decorator** | Wrapper class hierarchy | `@decorator` (Module 15) |
| **Observer** | Listener interfaces | A list of callables |
| **Iterator** | An interface | `__iter__` / `yield` (Module 14) |
| **Template Method** | Abstract base + hooks | A function taking hook functions |
| **Adapter** | A wrapper class | Often just duck typing |
| **Builder** | A builder class | Keyword arguments, or a frozen dataclass + `replace` |
| **Visitor** | Double dispatch | `match`, or `functools.singledispatch` |

The patterns that remain useful in Python — because they solve a real structural
problem rather than a missing language feature — are Adapter (when the interfaces
genuinely differ), Facade, Proxy, Repository, and Unit of Work.

**Singleton deserves a note**, because it is the one people reach for most and
need least:

```python
# config.py
_settings = load_settings()

def get_settings() -> Settings:
    return _settings
```

A module is imported once per process and cached in `sys.modules` (Module 06).
That is a singleton, with none of the thread-safety problems of the
double-checked-locking version and none of the testability problems of a class
that hides its own construction.

---

## 3. Composition over inheritance, concretely

```python
# inheritance: every combination needs a class
class Logger: ...
class TimestampLogger(Logger): ...
class JSONLogger(Logger): ...
class TimestampJSONLogger(TimestampLogger, JSONLogger): ...
# ... and now add compression. And filtering. 2^n classes.

# composition: combinations are constructed, not declared
@dataclass
class Logger:
    formatters: tuple[Callable[[str], str], ...] = ()
    sink: Callable[[str], None] = print

    def log(self, message: str) -> None:
        for fmt in self.formatters:
            message = fmt(message)
        self.sink(message)

Logger(formatters=(add_timestamp, to_json, compress), sink=write_to_file)
```

The inheritance version needs a new class per combination; the composition
version needs none. **That combinatorial difference is the whole argument**, and
it is why "favour composition" is advice rather than taste.

---

## 4. Descriptors

The mechanism under `@property`, `@classmethod`, `@staticmethod`,
`cached_property`, and every ORM field you have ever used.

```python
class Positive:
    """A reusable validated attribute."""

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = f"_{name}"          # called at CLASS creation time

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self                   # accessed on the CLASS, not an instance
        return getattr(obj, self._name)

    def __set__(self, obj, value) -> None:
        if value <= 0:
            raise ValueError(f"{self._name[1:]} must be positive, got {value}")
        setattr(obj, self._name, value)


class Product:
    price = Positive()          # written ONCE
    weight = Positive()
    quantity = Positive()
```

Three properties would have been thirty lines of near-identical code. The
descriptor is written once and reused.

**Data versus non-data descriptors** (Module 08, exercise 1): defining both
`__get__` and `__set__` makes it a *data* descriptor, which takes priority over
the instance `__dict__`. Defining only `__get__` makes it *non-data*, which the
instance dict beats — and that asymmetry is precisely how `cached_property`
works.

**When to use a descriptor:** the same attribute logic repeated across three or
more attributes, or across several classes. Below that, `@property` is clearer.

---

## 5. `__init_subclass__` and class decorators

Before reaching for a metaclass, try these two. They cover most of what people
use metaclasses for, at a fraction of the complexity.

```python
class Plugin:
    registry: dict[str, type] = {}

    def __init_subclass__(cls, *, name: str = "", **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.registry[name or cls.__name__.lower()] = cls

class CsvPlugin(Plugin, name="csv"): ...     # registers itself automatically
```

```python
def auto_repr(cls: type) -> type:
    """A class decorator: takes a class, returns a (usually modified) class."""
    def __repr__(self) -> str:
        args = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"{cls.__name__}({args})"
    cls.__repr__ = __repr__
    return cls
```

`@dataclass` is exactly this — a class decorator, no metaclass involved.

---

## 6. Metaclasses

> "Metaclasses are deeper magic than 99% of users should ever worry about. If you
> wonder whether you need them, you don't." — Tim Peters

A metaclass is the class of a class. `type` is the default.

```python
class Meta(type):
    def __new__(mcls, name, bases, namespace, **kwargs):
        namespace["created_by"] = "Meta"
        return super().__new__(mcls, name, bases, namespace)

class Thing(metaclass=Meta): ...
Thing.created_by            # 'Meta'
```

**Use one only when you must change how the class object itself is created** —
before it exists. In practice that means: ABCs (`ABCMeta`), enums (`EnumMeta`),
and ORM/serialization frameworks that rewrite the class namespace. Django models,
SQLAlchemy declarative, and Pydantic v1 all use them.

Everything else is better served by:

| Want | Use |
|---|---|
| React to subclass creation | `__init_subclass__` |
| Modify a class after creation | A class decorator |
| Reusable attribute behaviour | A descriptor |
| Prevent instantiation | ABC with `@abstractmethod` |
| Enforce an interface | `Protocol` + a type checker |
| Register implementations | `__init_subclass__` or a decorator |

Two costs worth knowing: metaclass conflicts (a class cannot inherit from two
classes with unrelated metaclasses) and the fact that they defeat most readers'
ability to follow the code.

---

## 7. When not to use a class at all

The most common over-engineering in Python is a class that should be a function.

```python
class EmailValidator:                    # a class with no state
    def __init__(self, strict=False):
        self.strict = strict
    def validate(self, email): ...

def validate_email(email: str, *, strict: bool = False) -> bool: ...
```

**Signs you wanted a function:**

- The class has one public method, and it is not `__call__`.
- `__init__` only stores arguments the single method uses.
- It is constructed and used on the same line.
- Every method is a `@staticmethod`.
- Its name ends in `-er` or `-Manager` and describes an action rather than a
  thing.

**A class earns its place when** it holds state across calls, has several
operations over shared data, participates in a protocol (Module 09), needs
several implementations behind one interface, or manages a resource lifecycle.

The corollary: a module full of functions is a perfectly good design. Python is
not Java; there is no requirement that everything live inside a class.

---

## Common mistakes in this module

| Mistake | Symptom | Fix |
|---|---|---|
| Java patterns transplanted | AbstractFactoryBuilderStrategy | Pass a function |
| A class with one method | Ceremony around a function call | Make it a function |
| Singleton class | Global state that is hard to test | A module |
| Deep inheritance for reuse | 2ⁿ classes for n features | Compose |
| A metaclass | Nobody can follow the code | `__init_subclass__`, decorator, descriptor |
| Fat interfaces | Implementers forced to stub methods | Narrow `Protocol`s |
| Constructing dependencies inside `__init__` | Untestable without a database | Inject them |
| DI framework | Configuration complexity for nothing | Default arguments |
| Getter/setter pairs | Java in Python | Plain attributes (Module 08) |
| Abstract base with one implementation | Speculative generality | Wait for the second one |

---

## Self-check quiz

1. Give the practical test for single responsibility.
2. How is open/closed usually achieved in Python, versus Java?
3. Why do Strategy, Command and Template Method largely disappear?
4. Why is a module a better singleton than a singleton class?
5. Show dependency injection in Python without a framework.
6. What makes a descriptor a *data* descriptor, and why does it matter?
7. Name three things to try before a metaclass, and what each covers.
8. Name two real, legitimate uses of metaclasses in libraries you have used.
9. Give five signs a class should have been a function.
10. Why does composition need n components where inheritance needs 2ⁿ classes?

---

## Exercises

1. **[`ex01_depatternise.py`](exercises/ex01_depatternise.py)** — Six
   Java-style pattern implementations. Rewrite each idiomatically and count the
   lines removed.
2. **[`ex02_descriptors.py`](exercises/ex02_descriptors.py)** — Build
   `Positive`, `Typed`, `Lazy` and `Unit` descriptors, then use them to remove
   duplication from a real class.
3. **[`ex03_plugins.py`](exercises/ex03_plugins.py)** — A plugin registry four
   ways: manual dict, decorator, `__init_subclass__`, entry points. Compare.
4. **[`ex04_di.py`](exercises/ex04_di.py)** — Take an untestable service class
   and invert its dependencies until it can be tested with no I/O at all.

---

## Going deeper

- [Data model: implementing descriptors](https://docs.python.org/3/howto/descriptor.html) — the official HOWTO is excellent
- [PEP 487 — `__init_subclass__` and `__set_name__`](https://peps.python.org/pep-0487/)
- Jack Diederich, "Stop Writing Classes" — 27 minutes, and it will change how you write Python
- Brandon Rhodes, [Python Design Patterns](https://python-patterns.guide/) — the GoF patterns, honestly reassessed for Python

---

**Next:** [Module 13 — Milestone Project: Plugin Document Pipeline](../13-project-plugin-pipeline/README.md)
