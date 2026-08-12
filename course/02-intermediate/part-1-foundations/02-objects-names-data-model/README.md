# Module 02 — Objects, Names, and the Data Model

**Time budget:** 5 hours lesson, 6 hours exercises
**Prerequisite:** Module 01

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md). This is the
> module where the visuals matter most — the entire subject is invisible in
> source code.

---

## Why this module is the most important one in Part 1

Almost every confusing Python bug that is not a typo comes from one
misunderstanding: believing that a variable is a **box that holds a value**.

In Python it is not. A name is a **label tied to an object**. Objects live in
memory; names are strings in a namespace that point at them. Assignment never
copies. Two names can point at the same object, and if that object is mutable,
changing it through one name changes what you see through the other.

That single sentence explains:

- why appending to one list changed a different list,
- why a default argument "remembered" a value between calls,
- why every object in your list of objects turned out to be the same object,
- why a class attribute was shared across all instances,
- why `copy()` did not actually protect you,
- why `is` and `==` disagree, and why `if x is 5` sometimes works and sometimes
  does not.

Get this module properly and the rest of Python stops surprising you.

---

## 1. Everything is an object

Not "almost everything". Integers, strings, functions, classes, modules,
exceptions, and the `None` singleton are all objects with a type, an identity,
and attributes.

```python
>>> (42).bit_length()
6
>>> "hello".upper()
'HELLO'
>>> def f(): pass
>>> f.__name__
'f'
>>> f.custom = "you can attach attributes to functions"
>>> type(int)
<class 'type'>
>>> type(type)
<class 'type'>
```

Every object has exactly three things:

| Property | Accessed by | Changes? |
|---|---|---|
| **Identity** | `id(obj)` | Never, for the object's whole life |
| **Type** | `type(obj)` | Effectively never |
| **Value** | the object itself | Only if the type is mutable |

In CPython, `id()` happens to be the memory address. That is an implementation
detail — the language only promises it is a unique integer that is constant for
the object's lifetime, and that it may be reused after the object dies.

---

## 2. Names are not boxes

The most important diagram in this course:

```
    WRONG mental model              RIGHT mental model

    a: [ 1, 2, 3 ]                  a ──┐
    b: [ 1, 2, 3 ]                      ├──> [ 1, 2, 3 ]   (one object)
                                    b ──┘
```

```python
a = [1, 2, 3]
b = a              # binds the name b to the SAME object. No copy happens.

b.append(4)        # MUTATES the object
print(a)           # [1, 2, 3, 4]   -- a "changed" without being mentioned
print(a is b)      # True
```

Now the crucial contrast:

```python
a = [1, 2, 3]
b = a
b = [9, 9, 9]      # REBINDS the name b to a NEW object
print(a)           # [1, 2, 3]  -- unchanged
print(a is b)      # False
```

**Mutation changes the object. Rebinding changes the name.** Everyone who has
been bitten by this bug confused the two. Two operations, similar syntax,
opposite consequences:

| Operation | Effect | Visible through other names? |
|---|---|---|
| `b = [9]` | Rebind `b` | No |
| `b.append(9)` | Mutate the object | **Yes** |
| `b += [9]` (list) | Mutate in place (`__iadd__`) | **Yes** |
| `b = b + [9]` | Build new list, rebind | No |

That third and fourth row are the same operation in most languages. In Python
they are not, and the difference is `list.__iadd__` existing. For tuples, which
have no `__iadd__`, `t += (9,)` falls back to `t = t + (9,)` and rebinds.

```python
def demo() -> None:
    x = [1]; y = x; y += [2];      print(x)   # [1, 2]  mutated
    x = [1]; y = x; y = y + [2];   print(x)   # [1]     rebound
```

---

## 3. Mutable and immutable

| Immutable | Mutable |
|---|---|
| `int`, `float`, `complex`, `bool` | `list` |
| `str`, `bytes` | `dict` |
| `tuple`, `frozenset` | `set` |
| `range`, `None` | `bytearray` |
| most enum members | most of your own classes |

Immutability is about the object, not the name. A name bound to an immutable
object can always be rebound; the object simply cannot be changed.

```python
s = "hello"
s.upper()          # returns a NEW string; s is untouched
print(s)           # 'hello'
s = s.upper()      # rebinding is how you "change" an immutable
```

### The tuple trap

A tuple is immutable. That means the *references it holds* cannot be changed.
It says nothing about the objects those references point to.

```python
t = ([1, 2], "fixed")
t[0].append(3)     # legal! the tuple still holds the same list object
print(t)           # ([1, 2, 3], 'fixed')
t[0] = [9]         # TypeError: 'tuple' object does not support item assignment
```

This is why a tuple containing a list is unhashable, and cannot be a dict key:

```python
{([1], 2): "x"}    # TypeError: unhashable type: 'list'
{((1,), 2): "x"}   # fine
```

---

## 4. `is` versus `==`

```python
a is b      # identity: are these the SAME object?         (id(a) == id(b))
a == b      # equality: do these objects COMPARE equal?    (calls __eq__)
```

```python
a = [1, 2, 3]
b = [1, 2, 3]
a == b     # True   -- same contents
a is b     # False  -- two distinct objects
```

**The rule: use `is` only for singletons.**

```python
if x is None: ...          # correct, always
if x is True: ...          # correct but usually unnecessary; prefer `if x:`
if flag is Sentinel: ...   # correct for your own sentinel objects
if name is "admin": ...    # WRONG. Use ==. It may appear to work. It is a bug.
```

Why is `is` wrong for values? Because whether two equal values are the same
object is an implementation detail:

```python
>>> a = 256; b = 256; a is b
True
>>> a = 257; b = 257; a is b
False          # in a REPL. In a single compiled block, possibly True.
```

CPython pre-allocates the integers -5 through 256 at startup and reuses them.
That is **small-int caching**, a CPython optimisation, not a language rule.
String literals get similar treatment (**interning**) for identifier-like
strings. Python 3.8+ emits a `SyntaxWarning` for `is` with a literal, precisely
because this bug was so common.

```python
>>> x = "hello"; y = "hello"; x is y
True                    # both interned
>>> x = "hello world!"; y = "hello world!"; x is y
False                   # not interned (contains characters that make it
                        #  ineligible under the current heuristic)
```

Never build logic on any of this. Use `==` for values, `is` for `None` and
sentinels. Full stop.

### The sentinel pattern

`is` has one genuinely important use beyond `None`: distinguishing "not
provided" from "provided as None".

```python
_MISSING = object()      # a unique object that equals nothing else

def get(config: dict[str, object], key: str, default: object = _MISSING) -> object:
    if key in config:
        return config[key]
    if default is _MISSING:
        raise KeyError(key)      # caller gave no default: missing is an error
    return default               # caller gave a default, possibly None
```

You will see this in the standard library and in every serious library. It is
the only way to let `None` be a legitimate default value.

---

## 5. Function arguments: call by object reference

Python is neither "pass by value" nor "pass by reference". Both terms mislead,
and material using them is a reliable signal that the author has not thought
about it. Python passes **object references, by value**. The parameter name is
a new name bound to the same object.

```python
def rebind(lst: list[int]) -> None:
    lst = [9, 9, 9]        # rebinds the LOCAL name. Caller sees nothing.

def mutate(lst: list[int]) -> None:
    lst.append(9)          # mutates the SHARED object. Caller sees it.

data = [1, 2]
rebind(data);  print(data)      # [1, 2]
mutate(data);  print(data)      # [1, 2, 9]
```

Same parameter, same call syntax, opposite effect — determined entirely by
whether the body rebinds or mutates.

### The mutable default argument

The most famous Python bug, and now you can explain it rather than memorise it.

```python
def add_item(item: str, basket: list[str] = []) -> list[str]:
    basket.append(item)
    return basket

print(add_item("apple"))    # ['apple']
print(add_item("pear"))     # ['apple', 'pear']    <-- !
```

**Default arguments are evaluated once, when the `def` statement executes**, not
on each call. That one list object is stored on the function and reused forever.
You can see it:

```python
>>> add_item.__defaults__
(['apple', 'pear'],)
```

The fix, every time:

```python
def add_item(item: str, basket: list[str] | None = None) -> list[str]:
    if basket is None:
        basket = []
    basket.append(item)
    return basket
```

Note `is None`, not `== None` or `if not basket` — an empty list passed
deliberately is falsy and would be silently replaced.

The same trap applies to `{}`, `set()`, and to any expression evaluated at def
time: `def log(t=datetime.now())` freezes the timestamp at import.

`ruff` catches this with rule `B006`, which is enabled in this course's config.

---

## 6. Copying

```python
import copy

original = [[1, 2], [3, 4]]

alias    = original                 # same object
shallow  = original[:]              # new outer list, SAME inner lists
shallow2 = list(original)           # identical to the above
shallow3 = copy.copy(original)      # identical to the above
deep     = copy.deepcopy(original)  # new outer AND new inner objects

original[0].append(99)
print(alias)     # [[1, 2, 99], [3, 4]]
print(shallow)   # [[1, 2, 99], [3, 4]]   <-- shared inner list
print(deep)      # [[1, 2], [3, 4]]       <-- fully independent
```

```
alias    ────────────────> [ ● , ● ]
                             │   │
original ──────────────────> │   │
                             v   v
shallow  ──> [ ● , ● ] ────> [1,2] [3,4]
                ^ ^            ^     ^
                └─┴────────────┴─────┘   (shared!)

deep     ──> [ ● , ● ] ────> [1,2]' [3,4]'   (fresh copies)
```

Practical guidance:

- A shallow copy is enough when the contents are immutable. `list(nums)` for a
  list of ints is genuinely safe.
- `deepcopy` is correct but slow, and it recurses through everything reachable —
  including, by accident, a database connection or a whole object graph.
- The best answer is usually **avoid needing a copy**: use immutable data, or
  return new objects instead of mutating in place. This is the theme that
  Modules 11 and 14 build on.

---

## 7. Memory: reference counting and the cycle collector

CPython frees an object when its reference count hits zero.

```python
import sys

a = [1, 2, 3]
sys.getrefcount(a)      # 2: one for `a`, one for the temporary argument
b = a
sys.getrefcount(a)      # 3
del b
sys.getrefcount(a)      # 2
```

Refcounting is immediate and predictable, which is why this works:

```python
with open("f.txt") as fh:      # closed deterministically at the end of the block
    ...
```

But refcounting alone cannot free a **cycle**:

```python
a = {}; b = {}
a["b"] = b; b["a"] = a         # each holds a reference to the other
del a, b                        # refcounts are still 1 each. Unreachable, but not freed.
```

That is why CPython also runs a **generational cycle collector** (`gc` module).
It finds unreachable cycles periodically. Two consequences worth carrying:

1. Object destruction is *usually* immediate but not *guaranteed* immediate.
   Never rely on `__del__` for cleanup — use a context manager (Module 09).
2. Cycles are collected, so they are not a leak, but they delay collection and
   cost CPU. `weakref` breaks them where it matters (caches, parent pointers,
   observer registries).

Other implementations (PyPy, GraalPy) do not refcount at all. Code that assumes
"the file closes when the variable goes out of scope" breaks on them. Use `with`.

---

## 8. Truthiness

`if x:` does not test `x == True`. It calls `bool(x)`, which consults
`__bool__`, or failing that `__len__`, or failing that returns `True`.

Falsy by default: `False`, `None`, `0`, `0.0`, `Decimal(0)`, `""`, `b""`, `[]`,
`()`, `{}`, `set()`, `range(0)`, and any object whose `__len__` returns 0.

**Everything else is truthy**, including `"0"`, `"False"`, `[0]`, `{"": None}`,
and `-1`.

The trap:

```python
def process(items: list[int] | None = None) -> None:
    if not items:          # True for None AND for []  -- are those the same case?
        ...
```

If "no argument given" and "an empty list given" should behave differently, that
check has silently merged them. Be explicit:

```python
    if items is None:      # not provided
    if not items:          # provided but empty
```

Same issue with numbers: `if count:` is wrong when `0` is a legitimate value.
`if count is not None:` is what you meant.

---

## 9. Namespaces are dictionaries

A namespace is a mapping from name strings to objects. That is all it is, and
you can look at it:

```python
x = 1
def f() -> None:
    y = 2
    print(locals())        # {'y': 2}

print(globals()["x"])      # 1
print(f.__globals__ is globals())   # True

class C:
    z = 3
print(C.__dict__["z"])     # 3

import math
print(math.__dict__["pi"]) # 3.14159...
```

Once you see that modules, classes, and instances are all essentially
dictionaries with lookup rules layered on top, a lot of Python stops being
special-cased and starts being mechanical. Module 08 uses this to explain
attribute lookup; Module 24 shows the bytecode.

---

## Common mistakes in this module

| Mistake | Symptom | Fix |
|---|---|---|
| `b = a` expecting a copy | Changing `b` changes `a` | `b = a.copy()` / `list(a)` / `deepcopy` |
| Mutable default argument | State leaks between calls | `= None` + `if x is None:` |
| `x is "value"` | Works, then mysteriously stops | `==` for values, `is` for `None`/sentinels |
| `[[0]*3]*3` grid | Setting one cell sets a whole column | `[[0]*3 for _ in range(3)]` |
| `if not x:` for "not provided" | `[]`, `0`, `""` treated as missing | `if x is None:` |
| Shallow copy of nested data | Inner objects still shared | `copy.deepcopy`, or restructure |
| Relying on `__del__` | Cleanup never runs, or runs late | `with` / context manager |
| Mutating a list while iterating it | Items silently skipped | Iterate a copy, or build a new list |
| `sort()` vs `sorted()` confusion | `x = lst.sort()` gives `None` | `sort()` mutates and returns None |

The `[[0]*3]*3` one deserves its own demonstration, because it catches people
who understood everything above:

```python
grid = [[0] * 3] * 3       # ONE inner list, referenced three times
grid[0][0] = 1
print(grid)                # [[1, 0, 0], [1, 0, 0], [1, 0, 0]]

grid = [[0] * 3 for _ in range(3)]   # three separate lists
grid[0][0] = 1
print(grid)                # [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
```

`*` on a list repeats *references*, never contents.

---

## Self-check quiz

1. What three things does every Python object have, and which of them can
   change?
2. Explain in one sentence why `b = a; b.append(1)` changes `a` but
   `b = a; b = [1]` does not.
3. Why is `x is 257` unreliable while `x is None` is always correct?
4. Default arguments are evaluated when? Give the consequence.
5. Is Python pass-by-value or pass-by-reference? Answer the question properly.
6. When is a shallow copy sufficient, and when is it a bug?
7. A tuple is immutable. Explain how `t[0].append(1)` can still succeed.
8. What does `if x:` actually call? Name three values where it does something
   you might not intend.
9. Why can reference counting not free a cycle, and what handles it?
10. Predict the output of `g = [[0]*2]*2; g[0][0] = 5; print(g)` and explain.

---

## Exercises

Work in [`exercises/`](exercises/).

1. **[`ex01_identity_lab.py`](exercises/ex01_identity_lab.py)** — Twelve
   predictions. Write your answer for each *before* running. Scoring yourself
   honestly here is the single best diagnostic in Part 1.
2. **[`ex02_aliasing_bugs.py`](exercises/ex02_aliasing_bugs.py)** — Six
   functions with real aliasing bugs. Diagnose, then fix, then write the test
   that would have caught each one.
3. **[`ex03_copy_semantics.py`](exercises/ex03_copy_semantics.py)** — Implement
   copying correctly for a nested configuration structure, three different ways,
   and measure the cost of each.
4. **[`ex04_sentinel.py`](exercises/ex04_sentinel.py)** — Build a cache API
   where `None` is a legitimate stored value. Impossible without sentinels.
5. **[`ex05_refcount_lab.py`](exercises/ex05_refcount_lab.py)** — Observe
   refcounting, build a cycle, watch the collector, then break the cycle with
   `weakref`.

---

## Going deeper (optional)

- [The Python Data Model](https://docs.python.org/3/reference/datamodel.html) —
  read section 3.1 now, the whole chapter after Module 09
- [`copy`](https://docs.python.org/3/library/copy.html) and
  [`weakref`](https://docs.python.org/3/library/weakref.html)
- [`gc` module](https://docs.python.org/3/library/gc.html) — `gc.get_referrers`
  is excellent for "what is keeping this alive?"
- Ned Batchelder, "Facts and Myths about Python Names and Values" — the
  definitive talk on this module's subject

---

**Next:** [Module 03 — Core Types and Their Behaviour](../03-core-types/README.md)
