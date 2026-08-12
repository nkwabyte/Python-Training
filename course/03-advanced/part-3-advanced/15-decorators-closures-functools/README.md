# Module 15 — Decorators, Closures, and functools

**Time budget:** 5 hours lesson, 7 hours exercises
**Prerequisite:** Modules 04 (closures), 14

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

A decorator is a function that takes a function and returns a function. That is
the whole idea; the `@` is sugar. Once that lands, the entire ecosystem stops
being magic: `@app.get("/users")`, `@pytest.fixture`, `@lru_cache`,
`@dataclass`, `@property`, `@task` — all of them are this one mechanism.

You already built two decorators in Module 04 without the syntax. This module
makes them correct, composable, and introspectable.

---

## 1. `@` is sugar

```python
@decorator
def f(): ...

# is exactly
def f(): ...
f = decorator(f)
```

Nothing more. The decorator runs **at definition time**, once, and the name `f`
is rebound to whatever it returns.

```python
def log_calls(fn):
    def wrapper(*args, **kwargs):
        print(f"calling {fn.__name__}")
        return fn(*args, **kwargs)
    return wrapper

@log_calls
def add(a, b): return a + b
```

`*args, **kwargs` in the wrapper means it works for any signature. That is why
almost every decorator wrapper looks like this.

---

## 2. `functools.wraps` is not optional

```python
@log_calls
def add(a, b):
    """Add two numbers."""

add.__name__      # 'wrapper'    <- wrong
add.__doc__       # None         <- gone
inspect.signature(add)   # (*args, **kwargs)   <- useless
```

The wrapper replaced the function, so all of its metadata is the wrapper's.
What breaks, concretely:

- `help()` and every documentation generator
- debuggers and profilers reporting "wrapper" for every decorated function
- **pytest fixture resolution**, which inspects parameter names
- **FastAPI and Pydantic**, which build schemas from signatures
- `singledispatch`, which reads annotations
- any logging that uses `__name__`

```python
import functools

def log_calls(fn):
    @functools.wraps(fn)          # copies __name__, __doc__, __module__,
    def wrapper(*args, **kwargs): # __qualname__, __dict__, and sets __wrapped__
        return fn(*args, **kwargs)
    return wrapper
```

`__wrapped__` is what lets `inspect.signature` see through the wrapper to the
real signature. **Always use `wraps`.** There is no case where omitting it is
correct.

---

## 3. Decorators with arguments: three levels

```python
def retry(attempts=3, delay=1.0):        # 1. the FACTORY takes the arguments
    def decorator(fn):                   # 2. the DECORATOR takes the function
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):    # 3. the WRAPPER takes the call
            for attempt in range(attempts):
                try:
                    return fn(*args, **kwargs)
                except Exception:
                    if attempt == attempts - 1:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(attempts=5)          # note: CALLED. retry(5) returns `decorator`.
def flaky(): ...
```

`@retry` without parentheses passes the *function* as `attempts`, and the error
appears far away and makes no sense. To support both forms:

```python
def retry(fn=None, *, attempts=3):
    if fn is None:                       # called with arguments
        return functools.partial(retry, attempts=attempts)
    @functools.wraps(fn)
    def wrapper(*a, **kw): ...
    return wrapper

@retry              # works
@retry(attempts=5)  # also works
```

---

## 4. Stacking order

```python
@a
@b
@c
def f(): ...

# f = a(b(c(f)))
```

**Bottom-up at definition; top-down at call time.** The decorator closest to the
`def` wraps first, so it is *innermost*, so its wrapper code runs *last* on the
way in.

This ordering matters and gets people:

```python
@app.route("/admin")        # registers whatever is beneath it
@require_auth               # so the route registered is the AUTHENTICATED one
def admin(): ...

@require_auth               # WRONG ORDER
@app.route("/admin")        # registers the RAW function; auth is never applied
def admin(): ...
```

The second version registers the undecorated function with the framework and
then wraps a name nobody calls. It looks right, runs fine, and has no
authentication.

Rules of thumb: `@staticmethod`/`@classmethod` outermost; caching outside
logging (so cached calls are not logged as work); registration outermost so it
registers the fully decorated function.

---

## 5. `functools`

### `lru_cache` / `cache`

```python
@functools.lru_cache(maxsize=128)
def expensive(n: int) -> int: ...

@functools.cache                  # 3.9+: unbounded lru_cache
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)

expensive.cache_info()            # hits, misses, maxsize, currsize
expensive.cache_clear()
```

Five things to know before using it:

1. **Arguments must be hashable.** A list argument raises `TypeError`.
2. **Equal-but-distinct arguments can collide.** `1`, `1.0` and `True` are equal
   and hash equally (Module 03), so a function that treats them differently can
   get the wrong cached answer. The exact behaviour is subtler than it looks —
   `lru_cache` has a fast path for a single `int` or `str` argument, so the real
   grouping is not the one you would predict. Exercise 15.3 measures it. The
   safe rule: if your function's behaviour depends on the *type* of a numeric
   argument, do not cache it by that argument.
3. **`f(1)` and `f(x=1)` are different entries.** Same call, two cache slots.
4. **It keeps a strong reference to every argument and result.** `@cache` on a
   method keeps every instance alive forever — a genuine and common memory leak.
   Use `maxsize`, or `cached_property`, or a `WeakValueDictionary`.
5. **Only cache pure functions.** A cached function with side effects performs
   them once and silently skips them thereafter.

### `partial`

```python
from functools import partial
int2 = partial(int, base=2)
int2("1010")                       # 10
sorted(rows, key=partial(get_field, "name"))
```

`partial` beats a lambda for a callback: it has a useful `repr`, it is
picklable (so it works with `multiprocessing`, Module 21), and it does not
capture variables by reference — which sidesteps Module 04's late-binding trap.

### `singledispatch`

```python
@functools.singledispatch
def serialise(obj) -> str:
    raise TypeError(f"cannot serialise {type(obj).__name__}")

@serialise.register
def _(obj: datetime) -> str: return obj.isoformat()

@serialise.register
def _(obj: Decimal) -> str: return str(obj)
```

Type-based dispatch without an `isinstance` chain, and — importantly —
**open for extension**: a third party can register a handler for their own type
without touching your code. This is the Visitor pattern, dissolved (Module 12).

`singledispatchmethod` does the same for methods.

### `cached_property`, `total_ordering`, `reduce`

```python
@functools.cached_property        # Module 08: computed once, stored in __dict__
def stats(self): ...

@functools.total_ordering         # Module 09: fills in <=, >, >= from < and ==
class Version: ...

functools.reduce(operator.mul, nums, 1)     # rarely clearer than a loop
```

`reduce` is worth knowing and rarely worth using. `sum`, `math.prod`,
`itertools.accumulate` and an explicit loop are all clearer.

---

## 6. `contextlib`

```python
from contextlib import contextmanager, suppress, ExitStack, closing, nullcontext

@contextmanager                    # Module 14: __enter__/__exit__ from a generator
def timer():
    start = time.perf_counter()
    try:
        yield
    finally:
        print(f"{time.perf_counter() - start:.3f}s")

with suppress(FileNotFoundError):  # the ONE legitimate exception-swallower
    path.unlink()

with ExitStack() as stack:         # a DYNAMIC number of context managers
    files = [stack.enter_context(open(p)) for p in paths]
    # all closed on exit, in reverse order, even if one open() fails

with nullcontext():                # a no-op, for conditional context managers
    ...
```

`ExitStack` is the answer to "I need N context managers where N is not known
until run time", and it handles the case where entering the third one raises —
the first two are still unwound correctly. Hand-rolled versions of this are
almost always subtly wrong.

---

## 7. Class-based decorators, and when to use one

```python
class CountCalls:
    def __init__(self, fn):
        functools.update_wrapper(self, fn)     # the class-based `wraps`
        self.fn = fn
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.fn(*args, **kwargs)

@CountCalls
def greet(): ...

greet.count                # inspectable state, on the decorated function
```

Use a class when the decorator needs **inspectable state** (a counter, a
registry, a circuit breaker's open/closed status) or several methods
(`.reset()`, `.stats()`). Use a function otherwise — it is lighter and more
common.

**One trap:** a class-based decorator on a *method* does not get the descriptor
protocol for free, so `self` is not bound correctly. You need `__get__`
returning `partial(self.__call__, obj)`, or just use a function-based decorator.

---

## Common mistakes in this module

| Mistake | Symptom | Fix |
|---|---|---|
| No `functools.wraps` | `help()`, pytest, FastAPI all break | Always use it |
| `@retry` instead of `@retry()` | Function passed as the first argument | Add parentheses, or support both |
| Wrong stacking order | Auth silently skipped; cache logs as work | Bottom-up wraps, top-down calls |
| `lru_cache` on a method | Every instance kept alive forever | `cached_property`, or `maxsize` |
| `lru_cache` on an impure function | Side effects happen once | Cache pure functions only |
| `lru_cache` with a list argument | `TypeError: unhashable` | Convert to a tuple |
| Decorator with state as a function | Nowhere to keep it | Use a class, or a closure cell |
| `except Exception` in a wrapper | Swallows `KeyboardInterrupt` context | Catch what you expect (Module 16) |
| Class decorator on a method | `self` not bound | Add `__get__`, or use a function |
| Assuming the decorator runs per call | Registration side effects duplicated | It runs once, at definition |

---

## Self-check quiz

1. Rewrite `@decorator` above `def f` without the `@` syntax.
2. Name four things that break without `functools.wraps`.
3. Draw the three levels of a decorator with arguments and say what each takes.
4. What happens if you write `@retry` when `retry` expects arguments?
5. Given `@a @b @c`, what is the wrapping order and what is the call order?
6. Why does `@app.route` need to be above `@require_auth`?
7. Give five things to know before using `lru_cache`.
8. Why does `partial` beat a lambda for a callback? Give three reasons.
9. What does `singledispatch` give you that an `isinstance` chain does not?
10. What problem does `ExitStack` solve that a nested `with` cannot?

---

## Exercises

1. **[`ex01_build.py`](exercises/ex01_build.py)** — Build eight decorators of
   increasing sophistication, all `wraps`-correct and signature-preserving.
2. **[`ex02_order.py`](exercises/ex02_order.py)** — Ten stacking puzzles.
   Predict the output, including one that silently disables authentication.
3. **[`ex03_functools.py`](exercises/ex03_functools.py)** — Cache traps: the
   method leak, the `1`/`True` collision, the unhashable argument, and the
   impure function.
4. **[`ex04_contextlib.py`](exercises/ex04_contextlib.py)** — Four context
   managers with `ExitStack`, including dynamic resources and partial-failure
   unwinding.

---

## Going deeper

- [`functools`](https://docs.python.org/3/library/functools.html) and [`contextlib`](https://docs.python.org/3/library/contextlib.html) — read both pages fully
- [PEP 318 — Decorators](https://peps.python.org/pep-0318/), including the rationale
- Graham Dumpleton's `wrapt` library and its blog series — the definitive treatment of decorator edge cases
- Read `functools.lru_cache`'s source. It is pure Python, ~100 lines, and it is Module 05's LRU cache with thread safety.

---

**Next:** [Module 16 — Error Handling and Robustness](../16-error-handling-and-robustness/README.md)
