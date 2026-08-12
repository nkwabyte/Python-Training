# Module 04 — Control Flow, Functions, and Scope

**Time budget:** 5 hours lesson, 7 hours exercises
**Prerequisite:** Modules 02 and 03

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

You can already write an `if` and a `def`. What this module adds is the parts
that are genuinely Python-specific and that you will otherwise get wrong for
years:

- `for ... else` and `while ... else`, which almost nobody guesses correctly
- the six kinds of function parameter and the `/` and `*` markers that select
  them
- LEGB scope resolution, and why `x += 1` inside a function raises
  `UnboundLocalError` while `x` alone does not
- closures, which are what make decorators (Module 15) possible
- `match`, which is not a switch statement
- type hints, which are documentation the tooling can check

---

## 1. Statements and expressions

Python draws a hard line between the two, and it explains several syntax errors.

An **expression** produces a value: `1 + 1`, `f(x)`, `[i for i in xs]`,
`a if b else c`. A **statement** does something: `x = 1`, `if`, `for`, `def`,
`return`, `import`.

Assignment is a statement, so this is a syntax error:

```python
if (line = input()):      # SyntaxError
```

That is deliberate: it is what stops `if (x = 1)` when you meant `==`. When you
genuinely want assignment inside an expression, use the walrus:

```python
if (line := input()):     # assignment EXPRESSION, 3.8+
    process(line)

while (chunk := fh.read(8192)):
    handle(chunk)

# best use: avoid computing something twice
if (m := pattern.search(text)) is not None:
    print(m.group(1))

[y for x in data if (y := transform(x)) is not None]
```

Use `:=` when it removes a repeated computation or a duplicated call. Do not use
it to compress two clear lines into one clever one.

### The conditional expression

```python
status = "on" if enabled else "off"
```

Note the order: value-if-true, condition, value-if-false. Do not nest more than
one; use a dict lookup or a function instead.

---

## 2. Loops, and the `else` nobody expects

```python
for item in collection:      # iterates ANYTHING iterable (Module 14)
    ...

for i, item in enumerate(collection, start=1):
    ...

for a, b in zip(xs, ys, strict=True):    # strict=True is 3.10+ and you want it
    ...

for key, value in mapping.items():
    ...
```

`zip(strict=True)` raises if the iterables have different lengths. Without it,
`zip` silently stops at the shortest, which has hidden many data bugs. Default
to `strict=True` unless truncation is genuinely intended.

### `for ... else`

The `else` clause runs **if the loop completed without `break`**. It is not "if
the loop body never ran".

```python
for user in users:
    if user.is_admin:
        print("found an admin")
        break
else:
    print("no admin found")        # runs only if we never broke out
```

Read `else` here as `nobreak` and it becomes obvious. It exists to remove the
`found = False` flag variable:

```python
found = False                       # the pattern for ... else replaces
for user in users:
    if user.is_admin:
        found = True
        break
if not found:
    ...
```

It is rare in real code, and it is on every Python quiz.

### Loop control

```python
break        # exit the innermost loop
continue     # next iteration
```

There is no labelled break. To exit nested loops, either extract the loops into
a function and `return`, or use a flag, or iterate a product:

```python
from itertools import product
for i, j in product(range(n), range(m)):
    if done(i, j):
        break                       # one loop, so one break is enough
```

Extracting to a function is almost always the cleanest of the three.

### Do not mutate what you are iterating

```python
for x in items:
    if pred(x):
        items.remove(x)             # silently skips elements (Module 02, q11)

items = [x for x in items if not pred(x)]      # correct
items[:] = [x for x in items if not pred(x)]   # correct, and in place
```

---

## 3. `match`: structural pattern matching, not a switch

`match` (3.10+) destructures values. Using it as a C-style switch wastes it.

```python
match command.split():
    case ["go", direction]:
        move(direction)
    case ["take", *items]:                 # capture the rest
        for item in items:
            take(item)
    case ["quit" | "exit"]:                # alternatives
        raise SystemExit
    case []:
        print("say something")
    case _:                                 # the default; _ matches anything
        print(f"unknown: {command}")
```

It matches structure, types, and attributes:

```python
match event:
    case {"type": "click", "pos": (x, y)}:          # dict + tuple shape
        handle_click(x, y)
    case {"type": "key", "code": int() as code}:    # type check + capture
        handle_key(code)
    case Point(x=0, y=0):                            # class patterns
        print("origin")
    case Point(x=x, y=y) if x == y:                  # a guard
        print("diagonal")
```

Two traps:

**A bare name is a capture, not a comparison.**

```python
case OK:              # binds anything to the name OK. Always matches!
case Status.OK:       # a dotted name IS compared. This is what you meant.
```

This is the number one `match` bug. Any pattern that is a plain identifier
captures; only dotted names, literals, and class patterns compare.

**Class patterns need `__match_args__`** for positional matching, which
`@dataclass` provides automatically (Module 11).

When is `match` worth it? When you are destructuring nested data — parsing,
protocol handling, AST walking, event dispatch. For dispatching on a single
value, a dict of functions is clearer and faster.

---

## 4. Functions: the six kinds of parameter

```python
def f(pos_only, /, standard, *args, kw_only, **kwargs):
    ...
```

| Kind | Declared | Called as |
|---|---|---|
| Positional-only | before `/` | `f(1)` only |
| Positional-or-keyword | between `/` and `*` | `f(1)` or `f(standard=1)` |
| Var-positional | `*args` | extra positionals collected into a tuple |
| Keyword-only | after `*` | `f(kw_only=1)` only |
| Var-keyword | `**kwargs` | extra keywords collected into a dict |

```python
def connect(host, port=5432, /, *, timeout=30, retries=3, **options):
    ...

connect("db", 5432, timeout=10, ssl=True)      # ok
connect(host="db")                              # TypeError: host is positional-only
connect("db", 5432, 10)                         # TypeError: timeout is keyword-only
```

**Why bother?**

- `/` (positional-only) frees you to rename parameters later without breaking
  callers. The standard library uses it heavily for exactly this reason.
- `*` (keyword-only) forces call sites to be readable. `resize(img, 800, 600,
  True, False)` is unreadable; `resize(img, width=800, height=600,
  preserve_aspect=True, upscale=False)` is not.

**Rule of thumb: any boolean parameter should be keyword-only.** A bare `True`
at a call site carries no information.

### Arguments are unpacked, not copied

```python
args = (1, 2)
kwargs = {"c": 3}
f(*args, **kwargs)          # equivalent to f(1, 2, c=3)
```

### The mutable default, again

```python
def f(items=[]):            # WRONG -- evaluated once at def time (Module 02)
def f(items=None):          # right
    if items is None:
        items = []
```

Same for `{}`, `set()`, `datetime.now()`, and any expression whose value should
be per-call. `ruff` rule `B006` catches it.

### Functions are objects

```python
def greet(name): return f"hi {name}"

greet.__name__          # 'greet'
greet.__doc__           # the docstring
greet.__defaults__      # the default values tuple
greet.__annotations__   # the type hints, as a dict

handlers = {"greet": greet}          # store them
def apply(fn, x): return fn(x)       # pass them
def make(): return greet             # return them
```

This is what makes decorators, callbacks, and higher-order functions possible,
and it is the subject of Module 15.

---

## 5. Scope: LEGB

Name lookup walks four scopes, in order:

```
L  Local        the current function's own names
E  Enclosing    any enclosing function's names (closures)
G  Global       the module's top-level names
B  Builtins     print, len, list, ...
```

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)        # local
    inner()
    print(x)            # enclosing
outer()
print(x)                # global
```

### Assignment makes a name local for the whole function

This is the rule that produces the most confusing error in the language:

```python
counter = 0

def increment():
    counter += 1        # UnboundLocalError: local variable 'counter'
                        # referenced before assignment
```

The compiler scans the function body *before* it runs. It sees `counter` being
assigned somewhere in the body, so `counter` is a **local** for the entire
function — including on the line that reads it, which happens before any write.
Reading it there is reading an unassigned local.

Note the asymmetry that makes this so confusing:

```python
def read_only():
    print(counter)      # fine -- no assignment in this body, so it is global

def mutate_ok():
    items.append(1)     # fine -- MUTATION is not assignment
```

The fixes, in order of preference:

```python
def increment(counter: int) -> int:      # 1. best: take it in, hand it back
    return counter + 1

class Counter:                            # 2. state belongs in an object
    def __init__(self): self.n = 0
    def increment(self): self.n += 1

def increment():                          # 3. last resort
    global counter
    counter += 1
```

`global` is almost always a design smell. It makes a function's behaviour depend
on invisible state and makes it untestable in isolation.

### `nonlocal` for closures

```python
def make_counter():
    count = 0
    def increment():
        nonlocal count       # rebind the ENCLOSING count, not a new local
        count += 1
        return count
    return increment

c = make_counter()
c(); c(); c()          # 1, 2, 3
```

`global` reaches the module scope. `nonlocal` reaches the nearest enclosing
*function* scope. Neither reaches a class body.

### Comprehensions have their own scope

```python
i = "untouched"
squares = [i * i for i in range(5)]
print(i)                # 'untouched' -- the loop variable did not leak
```

True since Python 3. A plain `for` loop *does* leak its variable; a comprehension
does not.

---

## 6. Closures

A closure is a function that remembers names from the scope where it was
*defined*, not where it is *called*.

```python
def multiplier(factor):
    def multiply(x):
        return x * factor      # `factor` comes from the enclosing scope
    return multiply

double = multiplier(2)
triple = multiplier(3)
double(5), triple(5)           # 10, 15
```

`factor` survives after `multiplier` has returned, because the inner function
holds a reference to a **cell** containing it:

```python
double.__closure__[0].cell_contents      # 2
double.__code__.co_freevars              # ('factor',)
```

### The late-binding trap

The single most common closure bug, and it appears in every language with
closures over mutable bindings:

```python
funcs = [lambda: i for i in range(3)]
[f() for f in funcs]           # [2, 2, 2]   -- not [0, 1, 2]
```

Each lambda captured the **variable** `i`, not its value at creation time. By
the time any of them runs, the loop has finished and `i` is 2.

The fix is to bind the value at definition time, with a default argument:

```python
funcs = [lambda i=i: i for i in range(3)]     # default evaluated at def time
[f() for f in funcs]                           # [0, 1, 2]
```

or with a factory:

```python
def make(i):
    return lambda: i
funcs = [make(i) for i in range(3)]
```

or `functools.partial` (Module 15). You will meet this again with event
handlers, callbacks, and anything built in a loop.

---

## 7. Type hints

Hints are not enforced at runtime. They are checked by mypy or pyright, read by
your editor, and used by libraries like Pydantic and FastAPI. Module 17 is the
full treatment; this is the working subset.

```python
def greet(name: str, times: int = 1) -> str: ...

def parse(raw: str) -> dict[str, int]: ...            # builtin generics, 3.9+
def find(xs: list[int]) -> int | None: ...            # union syntax, 3.10+
def apply(fn: Callable[[int], str], x: int) -> str: ...

from collections.abc import Iterable, Sequence
def total(values: Iterable[float]) -> float: ...      # accept ANY iterable
```

Two habits worth forming now:

**Accept the widest type, return the narrowest.** Take `Iterable[str]`, not
`list[str]` — then a generator, a tuple, or a set all work. Return `list[str]`,
not `Iterable[str]` — then the caller knows they can index it.

**`X | None` is not optional-as-in-omittable**; it means the value may be `None`.
A parameter is omittable because it has a default.

Write hints on every function you write in this course. Not because Python needs
them, but because writing the return type forces you to decide what the function
actually produces — which is where half of all design bugs are found.

---

## Common mistakes in this module

| Mistake | Symptom | Fix |
|---|---|---|
| `x += 1` on a global | `UnboundLocalError` | Pass it in and return it |
| `for...else` read as "if empty" | Wrong branch runs | It means "no break" |
| `zip` without `strict=True` | Silent truncation of data | `strict=True` |
| `lambda: i` in a loop | All closures see the last value | `lambda i=i: i` |
| Mutable default argument | State leaks between calls | `=None` sentinel |
| `case SOME_NAME:` | Always matches | Use a dotted name or literal |
| Boolean positional args | Unreadable call sites | Make them keyword-only with `*` |
| Mutating a list while iterating | Elements skipped | Build a new list |
| `global` for shared state | Untestable, order-dependent | Parameters, or a class |
| Returning different types by branch | Callers must type-check | One return type, or an explicit union |

---

## Self-check quiz

1. Why is `if (x = f()):` a syntax error, and what is the correct form?
2. When exactly does a `for ... else` clause run?
3. What does `zip(a, b)` do when the lengths differ, and how do you make that
   an error?
4. Explain `UnboundLocalError` in terms of when the compiler decides a name is
   local.
5. What is the difference between `global` and `nonlocal`?
6. Why does `[lambda: i for i in range(3)]` produce three identical results,
   and give two fixes?
7. What do `/` and `*` do in a parameter list, and why would you use each?
8. In a `match`, why does `case OK:` always match?
9. Why is `def f(items=[])` wrong, and why is `def f(items=())` less wrong?
10. What does "accept the widest type, return the narrowest" mean, with an
    example?

---

## Exercises

1. **[`ex01_scope_lab.py`](exercises/ex01_scope_lab.py)** — Twelve scope and
   closure predictions.
2. **[`ex02_signatures.py`](exercises/ex02_signatures.py)** — Redesign six bad
   function signatures. Tests check the calling conventions.
3. **[`ex03_closures.py`](exercises/ex03_closures.py)** — Build a counter, a
   memoiser, an event system, and a retry wrapper using closures only. No
   classes.
4. **[`ex04_match.py`](exercises/ex04_match.py)** — Write a command parser and
   an event router with `match`. Includes the capture-vs-compare trap.
5. **[`ex05_control_flow.py`](exercises/ex05_control_flow.py)** — Rewrite six
   loops that use flags, nesting, or index arithmetic into idiomatic Python.

---

## Going deeper

- [Execution model](https://docs.python.org/3/reference/executionmodel.html) — the binding rules, formally
- [PEP 636 — Structural Pattern Matching tutorial](https://peps.python.org/pep-0636/)
- [PEP 570 — Positional-only parameters](https://peps.python.org/pep-0570/)
- [PEP 572 — The walrus operator](https://peps.python.org/pep-0572/), including the rationale section

---

**Next:** [Module 05 — Collections in Depth and Comprehensions](../05-collections-and-comprehensions/README.md)
