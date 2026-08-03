# Module 08 — Classes and Encapsulation

**Time budget:** 5 hours lesson, 7 hours exercises
**Prerequisite:** Part 1 complete

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

You have written classes in other languages. Python's are different in ways
that matter:

- There is no `private`. There is a naming convention and one mangling rule.
- A class body is **executable code**, not a declaration.
- Attributes live in dictionaries, and lookup follows a specific ladder you can
  observe.
- `self` is explicit because a method is a plain function that got bound.
- `@property` lets you turn an attribute into a computation *later*, without
  changing a single call site — which is why Python code has almost no getters.

Get the attribute-lookup ladder and the rest of Part 2 is mechanical.

---

## 1. A class body is executable code

```python
class Config:
    print("this runs at class creation time")     # it really does
    VERSION = "1.0"
    NAMES = [n.upper() for n in ("a", "b")]

    def method(self):                              # def is a statement
        ...
```

`class` is a statement that executes its body in a fresh namespace, then calls
`type(name, bases, namespace)` to build the class object. What you get back is
an object, bound to a name, like everything else.

```python
>>> Config.__dict__.keys()
dict_keys(['__module__', 'VERSION', 'NAMES', 'method', ...])
>>> type(Config)
<class 'type'>
```

This is why decorators, `__init_subclass__`, and metaclasses can work at all
(Module 12), and why a class body can contain loops and conditionals — though
if yours does, consider whether a factory function would be clearer.

---

## 2. The attribute-lookup ladder

**The single most useful diagram in Part 2.** When you write `obj.x`, Python:

```
1. type(obj).__mro__  -- looking for a DATA DESCRIPTOR named x
                         (something with __get__ AND __set__ -- e.g. @property)
                         found? call its __get__ and STOP.
2. obj.__dict__['x']  -- the instance's own dictionary
                         found? return it and STOP.
3. type(obj).__mro__  -- the class and its bases, in MRO order
                         found? return it (binding it if it is a function)
4. type(obj).__getattr__('x')   -- last-resort hook, if defined
5. AttributeError
```

Two consequences that explain a great deal:

**Instance attributes shadow class attributes** (step 2 beats step 3) — but
**properties beat instance attributes** (step 1 beats step 2). That ordering is
what makes `@property` able to intercept an attribute that used to be plain
data.

**A method is found on the class, not the instance.** Every instance of a class
shares one function object; the binding happens at lookup time.

```python
class Dog:
    def speak(self): return "woof"

d = Dog()
Dog.speak            # <function Dog.speak>       -- a plain function
d.speak              # <bound method Dog.speak>   -- function + instance
d.speak()            # == Dog.speak(d)
```

That is all `self` is: the first parameter, filled in by the binding. Python
makes it explicit rather than implicit, which is why you can do this:

```python
Dog.speak(d)                      # call it unbound
handler = d.speak                 # store a bound method as a callback
list(map(str.upper, ["a", "b"]))  # use an unbound method as a function
```

---

## 3. Class attributes versus instance attributes

```python
class Counter:
    count = 0                     # CLASS attribute -- one, shared

    def __init__(self):
        self.items = []           # INSTANCE attribute -- one per object
```

The trap, and it is Module 02 wearing a class costume:

```python
class Basket:
    contents = []                 # SHARED between every instance

a, b = Basket(), Basket()
a.contents.append("apple")        # MUTATES the shared list
print(b.contents)                 # ['apple']   <-- !
```

Whereas:

```python
a.contents = ["apple"]            # REBINDS: creates an INSTANCE attribute
print(b.contents)                 # []          -- b still sees the class one
```

Mutation hits the shared object; assignment creates a per-instance shadow. Same
two operations from Module 02, same opposite outcomes.

**Rule: mutable state goes in `__init__`.** Class attributes are for constants,
defaults that are immutable, and things genuinely shared by all instances (a
registry, a counter of instances created).

---

## 4. There is no `private`

```python
class Account:
    def __init__(self):
        self.balance = 0          # public: part of the API
        self._ledger = []         # "internal": convention only
        self.__secret = "x"       # name-mangled, not private
```

| Form | Meaning | Enforced? |
|---|---|---|
| `name` | Public API | — |
| `_name` | Internal. Do not touch from outside. | No. Convention only. |
| `__name` | Mangled to `_ClassName__name` | Not privacy — see below |

`_name` is a message to other developers, and tools respect it: `from x import *`
skips it, IDEs de-emphasise it, documentation generators hide it. Nothing stops
you reading it. Python's position is that you are an adult and sometimes need to
reach into internals, and that a language-enforced barrier costs more than it
saves.

`__name` is different and frequently misunderstood. It exists for **one
purpose**: preventing accidental name collisions with subclasses.

```python
class Base:
    def __init__(self):
        self.__data = "base"      # becomes self._Base__data

class Child(Base):
    def __init__(self):
        super().__init__()
        self.__data = "child"     # becomes self._Child__data -- no collision

c = Child()
c._Base__data, c._Child__data     # ('base', 'child')  -- both alive
```

Use `__name` when you are writing a base class intended for subclassing and an
attribute must not be accidentally overridden. That is rare. Use `_name`
everywhere else.

---

## 5. `@property`: why Python has no getters

In Java you write getters from the start because changing a public field to a
method later breaks every caller. **In Python it does not**, because
`@property` intercepts attribute access at the same syntax.

```python
class Circle:
    def __init__(self, radius: float) -> None:
        self.radius = radius      # start plain. No getter, no setter.

    @property
    def area(self) -> float:      # a computed, read-only attribute
        return 3.14159 * self.radius ** 2

c = Circle(2)
c.area                            # 12.56...   -- no parentheses
c.area = 5                        # AttributeError: property has no setter
```

Adding validation later, without changing any call site:

```python
class Circle:
    def __init__(self, radius: float) -> None:
        self.radius = radius      # this now goes through the setter

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        if value <= 0:
            raise ValueError(f"radius must be positive, got {value}")
        self._radius = value
```

Every existing `c.radius` and `c.radius = 5` keeps working, now validated. This
is why **you should not write a getter and setter until you need one.** Start
with a plain attribute; promote it to a property when there is a reason.

Two things to watch:

**Infinite recursion.** Inside the property, use `self._radius`, never
`self.radius` — the latter calls the property again.

**Cheapness.** A property looks like an attribute, so callers assume it is
cheap. A property that issues a database query will be called in a loop by
someone who had no way to know. If it is expensive, make it a method named
`compute_x()`, or cache it:

```python
from functools import cached_property

class Dataset:
    @cached_property
    def stats(self) -> dict[str, float]:      # computed once, then stored
        return expensive_analysis(self.rows)  # in the instance __dict__
```

`cached_property` works by writing the result into `self.__dict__`, so step 2 of
the lookup ladder finds it on every subsequent access and the descriptor never
runs again. (Which means it needs a `__dict__` — it does not work with
`__slots__`.)

---

## 6. `@classmethod` and `@staticmethod`

```python
class Temperature:
    def __init__(self, kelvin: float) -> None:
        self.kelvin = kelvin

    @classmethod
    def from_celsius(cls, c: float) -> "Temperature":
        return cls(c + 273.15)             # cls, not Temperature

    @classmethod
    def from_fahrenheit(cls, f: float) -> "Temperature":
        return cls.from_celsius((f - 32) * 5 / 9)

    @staticmethod
    def is_valid_kelvin(value: float) -> bool:
        return value >= 0                   # no self, no cls
```

**`@classmethod` is how Python does named constructors.** A class can have only
one `__init__`, so alternative constructors become classmethods. Using `cls`
rather than the class name means subclasses get the right type back:

```python
class Kelvin(Temperature): ...
Kelvin.from_celsius(0)          # a Kelvin, not a Temperature
```

**`@staticmethod` is a function that lives in the class's namespace.** It gets
neither `self` nor `cls`. If it does not use either, ask whether it should be a
module-level function — often the honest answer is yes. It earns its place when
the grouping genuinely aids discovery, or when subclasses should be able to
override it.

---

## 7. `__slots__`

By default every instance carries a `__dict__`. `__slots__` replaces it with a
fixed array of named slots.

```python
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

p = Point(1, 2)
p.z = 3            # AttributeError: 'Point' object has no attribute 'z'
```

| | Without slots | With slots |
|---|---|---|
| Memory per instance | ~56 bytes + dict (~104+) | ~48 bytes |
| Attribute access | dict lookup | array index (slightly faster) |
| Add new attributes | yes | no |
| `__dict__` | yes | no |
| Multiple inheritance | free | restricted |
| `cached_property`, `weakref` | work | need explicit slots entries |

**Use it when you have many instances of a small, fixed-shape object**: points,
tokens, tree nodes, cache entries, parsed records. Typical saving is 40 to 50
percent of memory, which at 10⁶ instances is the difference between fitting in
RAM and not.

Do not reach for it by default. It removes flexibility that libraries
(especially mocking and serialization ones) sometimes rely on, and the memory
saving is meaningless at 10³ instances. `@dataclass(slots=True)` (Module 11)
gives you it without the boilerplate.

---

## 8. Encapsulation that actually works

Since `private` does not exist, encapsulation in Python is about **not handing
out mutable internals** — the Module 02 lesson, applied to design.

```python
class Playlist:
    def __init__(self, tracks: list[str]) -> None:
        self._tracks = list(tracks)          # copy IN

    @property
    def tracks(self) -> tuple[str, ...]:
        return tuple(self._tracks)           # immutable view OUT

    def add(self, track: str) -> None:
        self._tracks.append(track)
```

Without the copy on the way in, the caller keeps a handle on your internal list.
Without the conversion on the way out, anyone can mutate it. The underscore
documents intent; the copies enforce it.

The alternatives, each with a trade-off:

| Return | Cost | Caller can |
|---|---|---|
| `tuple(self._tracks)` | O(n) copy | read, index, not mutate |
| `list(self._tracks)` | O(n) copy | mutate their own copy |
| `iter(self._tracks)` | O(1) | iterate once; sees later mutations |
| `MappingProxyType(d)` | O(1) | read a dict; a live view, not a snapshot |
| `self._tracks` | O(1) | **everything.** Not encapsulation. |

---

## Common mistakes in this module

| Mistake | Symptom | Fix |
|---|---|---|
| Mutable class attribute | State shared across all instances | Assign it in `__init__` |
| Property using `self.x` inside itself | `RecursionError` | Use `self._x` |
| Getters and setters everywhere | Java in Python | Plain attributes; promote to property when needed |
| Expensive property | Called in a loop by an innocent caller | `cached_property`, or a method |
| `__name` believed to be private | Surprise when someone reads `_C__name` | It prevents collisions, not access |
| `@staticmethod` on everything | A class used as a namespace | Module-level functions |
| Returning `self._items` | Callers mutate your internals | Return a copy or a tuple |
| `__slots__` by reflex | Lost flexibility for no measured gain | Only when instance count is large |
| `Temperature(...)` inside a classmethod | Subclasses get the wrong type | `cls(...)` |
| Forgetting `self` on a method | `TypeError: takes 0 positional arguments but 1 was given` | Add `self` |

---

## Self-check quiz

1. What does `class` actually do, mechanically?
2. Name the five steps of attribute lookup in order.
3. Why does a property beat an instance attribute of the same name?
4. Explain why `a.contents.append(x)` and `a.contents = [x]` differ for a class
   attribute.
5. What does `__name` do, and what problem does it exist to solve?
6. Why does Python code rarely have getters, when Java code always does?
7. When is `@classmethod` the right tool? Why `cls` rather than the class name?
8. What does `__slots__` trade away, and when is the trade worth it?
9. How does `cached_property` avoid recomputing, and why does that mean it
   cannot work with `__slots__`?
10. Give three ways to expose an internal list, with the trade-off of each.

---

## Exercises

1. **[`ex01_lookup_lab.py`](exercises/ex01_lookup_lab.py)** — Twelve attribute
   lookups to predict. Then implement `__getattr__` and watch the ladder.
2. **[`ex02_properties.py`](exercises/ex02_properties.py)** — Take a class with
   eight getters and setters and reduce it to plain attributes plus three
   properties, without breaking any call site.
3. **[`ex03_encapsulation.py`](exercises/ex03_encapsulation.py)** — Six classes
   that leak internals. Fix each, and write the test that proves it.
4. **[`ex04_slots_bench.py`](exercises/ex04_slots_bench.py)** — Measure memory
   and speed with and without `__slots__` at four instance counts, and find
   where it starts to matter.
5. **[`ex05_bank.py`](exercises/ex05_bank.py)** — Design a small `Account` class
   properly: validated construction, computed properties, named constructors,
   and no way for a caller to corrupt the balance.

---

## Going deeper

- [Data model: customizing attribute access](https://docs.python.org/3/reference/datamodel.html#customizing-attribute-access)
- [`property`](https://docs.python.org/3/library/functions.html#property) and [`functools.cached_property`](https://docs.python.org/3/library/functools.html#functools.cached_property)
- [`__slots__`](https://docs.python.org/3/reference/datamodel.html#slots)
- Raymond Hettinger, "Python's Class Development Toolkit" — the definitive talk
  on this module's material

---

**Next:** [Module 09 — The Data Model: Dunder Methods](../09-dunder-and-data-model/README.md)
