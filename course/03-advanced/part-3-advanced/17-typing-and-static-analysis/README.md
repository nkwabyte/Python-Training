# Module 17 — Typing and Static Analysis

**Time budget:** 5 hours lesson, 7 hours exercises
**Prerequisite:** Modules 04, 10, 11

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

Python's type hints are **not enforced at runtime**. `def f(x: int)` accepts a
string, happily, forever. So why write them?

Because a type checker reads them and finds, before you run anything, the class
of bug that Module 01's Case 4 demonstrated: a value that was the wrong type
three modules ago and only fails now. In a dynamic language, static typing is
the substitute for a compiler — and unlike a compiler, you can adopt it
gradually, file by file.

---

## 1. The basics, in modern syntax

```python
def greet(name: str, times: int = 1) -> str: ...

nums: list[int] = []                    # builtin generics, 3.9+
mapping: dict[str, list[int]] = {}
pair: tuple[str, int] = ("a", 1)        # a fixed 2-tuple
row: tuple[int, ...] = (1, 2, 3)        # a variable-length tuple
maybe: str | None = None                # union syntax, 3.10+
```

Do not write `List[int]`, `Dict[str, int]`, or `Optional[str]` in new code. They
are the pre-3.9 spellings, still valid and now noise. `ruff`'s `UP` rules rewrite
them for you.

**Accept the widest type, return the narrowest.**

```python
from collections.abc import Iterable, Sequence, Mapping

def total(values: Iterable[float]) -> float: ...     # any iterable works
def process(items: Sequence[str]) -> list[str]: ...  # needs len/indexing
def lookup(config: Mapping[str, int]) -> int: ...    # read-only dict
```

Taking `Iterable` means a list, tuple, set, generator, or dict-keys view all
work. Taking `list` rejects four of those for no reason. Returning `list` tells
the caller they can index it; returning `Iterable` makes them guess.

And a hard-won rule from Module 14: **if your function iterates its argument
twice, it must take `Sequence`, not `Iterable`.** The type is the contract, and
`Iterable` promises only one pass.

---

## 2. `Optional` is not "optional"

```python
def f(x: str | None) -> None: ...    # x MAY BE None. It is still REQUIRED.
def g(x: str = "default") -> None:   # x is omittable.
def h(x: str | None = None) -> None: # both
```

Confusing these is the single most common typing error. A parameter is omittable
because it has a **default**; `| None` says only that `None` is a permitted
*value*.

The payoff is narrowing:

```python
def process(user: User | None) -> str:
    return user.name          # error: Item "None" has no attribute "name"

def process(user: User | None) -> str:
    if user is None:
        raise ValueError("user is required")
    return user.name          # fine: mypy knows user is a User here
```

The checker follows `if x is None`, `isinstance`, `assert`, and early returns.
This is **type narrowing**, and it is where most of the day-to-day value is —
it forces you to handle the `None` case at the point you introduced it.

---

## 3. The vocabulary worth knowing

```python
from typing import Any, Literal, Final, TypeAlias, Self, NoReturn, cast, overload

x: Final = 3.14                          # never reassigned
Mode = Literal["r", "w", "a"]            # exactly these three strings
UserId: TypeAlias = int                  # a readable alias

def fail(msg: str) -> NoReturn:          # never returns normally
    raise RuntimeError(msg)

class Builder:
    def add(self, x: int) -> Self:       # 3.11+: returns THIS subclass
        return self
```

**`Literal` is underused and excellent.** `mode: Literal["r", "w"]` catches
`mode="rw"` at check time, and a `match` over a `Literal` can be checked for
exhaustiveness.

**`Any` disables checking**, silently and infectiously — every expression
involving an `Any` becomes `Any`. Treat it as a `# type: ignore` with a wider
blast radius. Prefer `object` when you truly do not know: `object` is safe (you
must narrow before using it), whereas `Any` permits everything.

**`cast` does nothing at runtime.** It is an assertion to the checker that you
know better. Each one is a place you have taken responsibility for a bug the
checker can no longer find.

---

## 4. Generics

```python
from collections.abc import Callable

def first[T](items: Sequence[T]) -> T | None:        # PEP 695, 3.12+
    return items[0] if items else None

class Stack[T]:                                       # generic class, 3.12+
    def __init__(self) -> None:
        self._items: list[T] = []
    def push(self, item: T) -> None: self._items.append(item)
    def pop(self) -> T: return self._items.pop()
```

Pre-3.12 syntax, still everywhere:

```python
from typing import TypeVar, Generic
T = TypeVar("T")

def first(items: Sequence[T]) -> T | None: ...
class Stack(Generic[T]): ...
```

Constrained and bounded type variables:

```python
T = TypeVar("T", int, str)          # CONSTRAINED: exactly int or str
N = TypeVar("N", bound=Number)      # BOUND: Number or any subclass
```

**Variance in one paragraph.** `Sequence[T]` is *covariant*: a
`Sequence[Dog]` is acceptable where a `Sequence[Animal]` is wanted, because you
can only read from it. `list[T]` is *invariant*: a `list[Dog]` is **not**
acceptable where a `list[Animal]` is wanted, because the callee could append a
`Cat` to it and break the caller's assumption. This is why taking `Sequence`
rather than `list` is not only more permissive but also more type-correct.

---

## 5. `Protocol`: structural typing

Module 10 covered the design side. Here is the typing side:

```python
from typing import Protocol, runtime_checkable

class Closeable(Protocol):
    def close(self) -> None: ...

def cleanup(resource: Closeable) -> None:
    resource.close()

cleanup(open("f.txt"))       # a file satisfies it
cleanup(socket)              # so does a socket
cleanup(MyThing())           # so does anything with close()
```

No inheritance, no registration, checked statically. This is how you type "duck
typing" without giving up either the duck or the typing.

`runtime_checkable` enables `isinstance`, which checks **method names only** —
not signatures. It is a weak check and should not be relied on for correctness.

---

## 6. `TypedDict`, `NewType`, `overload`

```python
from typing import TypedDict, NewType, overload

class UserRecord(TypedDict):
    id: int
    name: str
    email: NotRequired[str]        # 3.11+

UserId = NewType("UserId", int)    # a distinct type at check time, an int at runtime

def get_user(uid: UserId) -> UserRecord: ...
get_user(42)                        # error: int is not UserId
get_user(UserId(42))                # fine
```

`NewType` is how you stop passing an order id where a user id was expected —
both are `int` to Python and distinct to the checker, at zero runtime cost.

```python
@overload
def parse(raw: str, *, strict: Literal[True]) -> Config: ...
@overload
def parse(raw: str, *, strict: Literal[False]) -> Config | None: ...
def parse(raw: str, *, strict: bool = True) -> Config | None: ...
```

`overload` expresses "the return type depends on an argument value" — exactly
the shape Module 04 said to avoid in a signature. When you cannot avoid it
(often because you are typing someone else's API), this is how you describe it.

---

## 7. Running the checkers

```bash
mypy .                      # the reference implementation
mypy --strict .             # what this course uses
pyright .                   # faster, better inference, used by Pylance
```

```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_unreachable = true

[[tool.mypy.overrides]]      # a third-party library with no stubs
module = ["untyped_lib.*"]
ignore_missing_imports = true
```

`strict` turns on about a dozen flags, of which the ones that matter are
`disallow_untyped_defs` (every function must be annotated) and
`disallow_any_explicit`-adjacent checks that stop `Any` leaking.

**Adopting typing on an existing codebase:**

1. Turn the checker on with everything **off**, and make it pass. This gives you
   a green baseline and a CI gate.
2. Enable `disallow_untyped_defs` **per module**, starting with the ones that
   change most often or hurt most when wrong.
3. Type new code strictly from the start.
4. Type the boundaries first — the public API, the data models, the I/O layer.
   That is where the errors are.
5. Never do a big-bang conversion. It produces thousands of errors, gets
   abandoned, and leaves the codebase with a disabled checker.

```python
x = some_untyped_call()   # type: ignore[no-any-return]
```

Always use the bracketed error code, never a bare `# type: ignore`. A bare one
suppresses future, unrelated errors on that line forever.

---

## 8. Static types versus runtime validation

**They solve different problems and you need both.**

| | Static (mypy) | Runtime (Pydantic) |
|---|---|---|
| When | Before running | While running |
| Cost | Zero at runtime | Real, per object |
| Catches | Wrong types in *your* code | Wrong types in *incoming data* |
| Cannot catch | Bad JSON from a client | A bug in a branch never run |

```python
# a boundary: data you did not create
class UserIn(BaseModel):          # Pydantic: validates and coerces at runtime
    name: str
    age: int

# inside: data you did create
@dataclass(frozen=True)           # dataclass + mypy: checked statically, free
class User:
    name: str
    age: int
```

**Validate at the boundary, trust inside.** Once `UserIn` has parsed the
request, everything downstream can rely on `age` being an `int`, and mypy will
enforce that it stays one. Module 28 builds on this.

---

## Common mistakes in this module

| Mistake | Symptom | Fix |
|---|---|---|
| Believing hints are enforced | `f(x="abc")` runs fine | Run a checker; validate at boundaries |
| `Optional` meaning "omittable" | Required argument, confusing errors | `| None` is about the value; defaults are about omission |
| `list` where `Iterable` fits | Rejects generators and tuples | Widen the parameter |
| `Iterable` for a two-pass function | Silent empty second pass | `Sequence` |
| `Any` to silence an error | Checking disabled, infectiously | `object`, or narrow properly |
| Bare `# type: ignore` | Future errors on that line hidden | `# type: ignore[code]` |
| `List[int]`, `Optional[X]` | Pre-3.9 noise | `list[int]`, `X | None` |
| Big-bang strict conversion | Thousands of errors, abandoned | Per-module adoption |
| Typing only internals | Boundaries are where the bugs are | Type the edges first |
| `cast` used liberally | Silently disabled checks | Narrow with `isinstance`/`assert` |
| Trusting `isinstance` on a Protocol | Signatures unchecked | Static checking |

---

## Self-check quiz

1. Are type hints enforced at runtime? What is the practical consequence?
2. What is the difference between `x: str | None` and `x: str = "a"`?
3. State "accept the widest, return the narrowest" and give an example of each.
4. Why must a function that iterates its argument twice take `Sequence`?
5. Why is `list[T]` invariant while `Sequence[T]` is covariant?
6. What does `Any` do to the expressions it touches?
7. When is `object` better than `Any`?
8. What does `NewType` cost at runtime, and what does it buy?
9. Give the five-step plan for adopting typing on an existing codebase.
10. What can Pydantic catch that mypy cannot, and vice versa?

---

## Exercises

1. **[`ex01_annotate.py`](exercises/ex01_annotate.py)** — Annotate twelve
   untyped functions until `mypy --strict` is clean. Three need a `Protocol`.
2. **[`ex02_narrowing.py`](exercises/ex02_narrowing.py)** — Ten narrowing
   puzzles, including two where the checker is right and you are wrong.
3. **[`ex03_generics.py`](exercises/ex03_generics.py)** — Build a typed
   `Result[T, E]`, a typed pipeline, and a generic repository `Protocol`.
4. **[`ex04_adopt.py`](exercises/ex04_adopt.py)** — Take an untyped 200-line
   module to `--strict` clean, in the correct order, recording error counts.

---

## Going deeper

- [`typing`](https://docs.python.org/3/library/typing.html) and the [mypy cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
- [PEP 695 — Type parameter syntax](https://peps.python.org/pep-0695/) (3.12)
- [PEP 544 — Protocols](https://peps.python.org/pep-0544/)
- [typeshed](https://github.com/python/typeshed) — the stubs for the standard library; read one for a module you use

---

**Next:** [Module 18 — Testing, Debugging, and Quality](../18-testing-and-quality/README.md)
