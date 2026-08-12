# Module 03 — Core Types and Their Behaviour

**Time budget:** 5 hours lesson, 6 hours exercises
**Prerequisite:** Module 02

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

You know what a string and a list are. What you probably do not know is where
each of them will quietly betray you:

- `0.1 + 0.2 != 0.3`, and it is not a Python bug.
- `round(2.5)` is `2`, not `3`, and that is also not a bug.
- A `str` and a `bytes` are not interchangeable, and the boundary between them
  is where every encoding disaster in your career will happen.
- `x in some_list` is O(n) and `x in some_set` is O(1), and the difference is
  visible at 10,000 items.
- `dict` preserves insertion order — but that only became a language guarantee
  in 3.7, which matters when reading older code.

This module is about the properties of the built-in types that determine whether
your program is correct and how fast it is.

---

## 1. Numbers

### `int` is arbitrary precision

```python
>>> 2 ** 1000
10715086071862673209484250490600018105614048117055336074437503883703510511249361...
>>> (2**64).bit_length()
65
```

No overflow, ever. Python promotes silently and without limit. This is a
genuine relief coming from C or Java — no `long long`, no wraparound bugs.

The cost is that ints are objects, not machine words:

```python
>>> import sys
>>> sys.getsizeof(0), sys.getsizeof(1), sys.getsizeof(2**100)
(28, 28, 44)
```

28 bytes for the number 1, against 8 for a C `int64`. That is the memory story
behind "use NumPy for numeric arrays" (Module 29): a list of a million Python
ints is roughly 40 MB; a NumPy `int64` array of the same is 8 MB, contiguous.

Since 3.11 there is a safety limit on `int`↔`str` conversion (default 4300
digits) to prevent quadratic-time denial of service. `sys.set_int_max_str_digits`
adjusts it if you genuinely need giant decimal output.

### `float` is IEEE 754, and it will lie to you

```python
>>> 0.1 + 0.2
0.30000000000000004
>>> 0.1 + 0.2 == 0.3
False
>>> from decimal import Decimal
>>> Decimal(0.1)
Decimal('0.1000000000000000055511151231257827021181583404541015625')
```

Binary floating point cannot represent 0.1 exactly, the same way decimal cannot
represent 1/3. This is not a Python flaw; it is IEEE 754 and it is true in
JavaScript, C, Java, and your calculator. Python is merely honest about it in
the REPL.

**Never compare floats with `==`.**

```python
import math
math.isclose(0.1 + 0.2, 0.3)                          # True
math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)       # tune for your domain
```

Note the two tolerances. Relative tolerance is right for large numbers, absolute
for values near zero (where relative tolerance degenerates). If either matters,
set both.

Other float facts that bite:

```python
>>> round(2.5), round(3.5), round(0.5)
(2, 4, 0)                       # banker's rounding: ties go to even
>>> float('inf') > 10**1000
True
>>> float('nan') == float('nan')
False                           # NaN is not equal to itself. By design.
>>> math.isnan(x)               # the only correct NaN test
>>> 1e16 + 1 == 1e16
True                            # beyond 2**53, integers are not exact in float
```

Banker's rounding is deliberate: always rounding halves up biases sums upward.
It matches IEEE 754's default mode. If you need "round half up", use `Decimal`
with an explicit rounding mode.

### `Decimal` for money, `Fraction` for exactness

```python
from decimal import Decimal, ROUND_HALF_UP, getcontext

Decimal("0.1") + Decimal("0.2") == Decimal("0.3")     # True
Decimal("19.99") * 3                                   # Decimal('59.97') exactly

getcontext().prec = 28
Decimal("1.005").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)  # 1.01
```

**Construct `Decimal` from strings, never from floats.** `Decimal(0.1)` faithfully
copies the float's error into the Decimal; `Decimal("0.1")` is exact.

**Use `Decimal` for money.** Or, better still, store money as an integer number
of minor units (cents) and format on display — that is what most payment systems
do, and it makes the arithmetic trivially exact.

```python
from fractions import Fraction
Fraction(1, 3) + Fraction(1, 6) == Fraction(1, 2)      # True, exactly
```

### `bool` is an `int`

```python
>>> True + True
2
>>> isinstance(True, int)
True
>>> sum([True, False, True])       # a legitimate idiom for counting matches
2
>>> sum(1 for x in data if x > 5)  # clearer, and the one to prefer
```

### Division and the operators worth knowing

```python
7 / 2       # 3.5    true division, ALWAYS float (even 4/2 -> 2.0)
7 // 2      # 3      floor division
-7 // 2     # -4     floors toward negative infinity, not toward zero
7 % 3       # 1
-7 % 3      # 2      the result carries the sign of the DIVISOR
divmod(7, 3)        # (2, 1)
7 ** 2      # 49
```

`-7 // 2 == -4` surprises people from C, where it truncates to `-3`. Python's
choice keeps the invariant `a == (a // b) * b + (a % b)` true for negatives,
which is what makes `%` useful for cyclic indexing: `-1 % 7 == 6`.

---

## 2. Strings and bytes: the boundary that matters

This is the most important section in the module.

```
str                                   bytes
"text, a sequence of characters"      b"data, a sequence of 0-255 integers"
        |                                      ^
        |  .encode('utf-8')                    |
        +--------------------------------------+
        ^                                      |
        |  .decode('utf-8')                    |
        +--------------------------------------+
```

- **`str` is text.** A sequence of Unicode code points. It has no encoding. It
  is what you compute with.
- **`bytes` is data.** A sequence of integers 0-255. It is what files, sockets,
  and disks actually hold.

Everything entering your program from outside is bytes. Everything leaving is
bytes. The rule, sometimes called the Unicode sandwich:

> **Decode at the input boundary. Work in `str`. Encode at the output boundary.**

```python
raw = b'\xc3\xa9clair'
text = raw.decode('utf-8')       # 'éclair'   <- decode ON THE WAY IN
print(len(raw), len(text))       # 8 6        <- bytes != characters
back = text.encode('utf-8')      # b'\xc3\xa9clair'  <- encode ON THE WAY OUT
```

Note `len(raw) != len(text)`. In UTF-8, one character can be 1 to 4 bytes. This
is why slicing bytes is dangerous and slicing str is safe.

### Always specify the encoding

```python
open("f.txt")                                 # uses the LOCALE default. A bug.
open("f.txt", encoding="utf-8")               # correct, always
Path("f.txt").read_text(encoding="utf-8")     # correct
open("f.bin", "rb")                           # binary: no encoding involved
```

The default encoding differs between Linux (usually UTF-8) and Windows (often
cp1252), which is the classic "works on my machine" file bug. Python 3.15 will
make UTF-8 the default; until then, be explicit. You can opt in early with
`PYTHONUTF8=1` or `python -X utf8`, and you can catch every unspecified-encoding
call with `python -X warn_default_encoding`.

### Handling bad bytes

```python
raw.decode('utf-8')                       # UnicodeDecodeError on invalid input
raw.decode('utf-8', errors='replace')     # invalid bytes -> U+FFFD
raw.decode('utf-8', errors='ignore')      # invalid bytes silently dropped
raw.decode('utf-8', errors='surrogateescape')  # round-trippable, for filenames
```

Prefer failing loudly. `errors='ignore'` converts a data problem into silent
corruption, which is worse. Use `surrogateescape` for filesystem paths, where
you must round-trip whatever the OS gave you.

### `str` methods you will actually use

```python
s.strip() / .lstrip() / .rstrip()      # whitespace or given chars
s.split(",") / .rsplit(",", 1)         # rsplit with maxsplit is underused
s.partition(":")                       # ('before', ':', 'after') -- never raises
"-".join(parts)                        # the ONLY correct way to build from a list
s.startswith(("http://", "https://"))  # accepts a TUPLE of prefixes
s.replace(old, new, count)
s.casefold()                           # aggressive lowercase for comparison
s.removeprefix("v") / .removesuffix(".txt")   # 3.9+, better than slicing
s.encode("utf-8")
```

Two notes. `s.lower()` is for display; `s.casefold()` is for comparison (it
handles the German ß and similar correctly). And `s.strip("abc")` strips *any of
those characters*, not the substring — a very common misreading:

```python
>>> "example.com".strip("moc.")
'example'                # not what most people expect
>>> "example.com".removesuffix(".com")
'example'                # what they meant
```

### f-strings and the format mini-language

```python
name, value, ratio = "cpu", 1234.5678, 0.8532

f"{name}: {value}"              # cpu: 1234.5678
f"{value:.2f}"                  # 1234.57
f"{value:,.2f}"                 # 1,234.57
f"{value:>12.2f}"               # right-align in 12 cols
f"{value:<12.2f}"               # left-align
f"{value:^12.2f}"               # centre
f"{ratio:.1%}"                  # 85.3%
f"{255:#x}  {255:08b}  {255:o}" # 0xff  11111111  377
f"{value:e}"                    # 1.234568e+03
f"{name!r}"                     # 'cpu'   -- repr, quotes visible
f"{value=}"                     # value=1234.5678   -- debugging gold
f"{value:{width}.{prec}f}"      # nested: width and precision from variables

from datetime import datetime
f"{datetime.now():%Y-%m-%d %H:%M}"
```

`f"{x=}"` prints both the expression text and its value. It is the single best
replacement for `print("x is", x)` and you should adopt it today.

Use `!r` in every error message and log line. `repr` shows quotes, escapes, and
whitespace — precisely the things that matter when the bug is an empty string or
a trailing space.

**Building strings in a loop:**

```python
parts = []
for item in items:
    parts.append(transform(item))
result = "".join(parts)                     # correct

result = ""
for item in items:
    result += transform(item)               # O(n^2) in principle
```

CPython has an optimisation that often makes the second form linear anyway, but
it is fragile (it only applies when the string has a refcount of 1) and it does
not hold on other implementations. `"".join()` is both faster and clearer.

---

## 3. Slicing

Slicing works on every sequence: `str`, `bytes`, `list`, `tuple`, `range`.

```python
s = "abcdefgh"
s[2]        # 'c'
s[2:5]      # 'cde'      start inclusive, stop EXCLUSIVE
s[:3]       # 'abc'
s[3:]       # 'defgh'
s[-2:]      # 'gh'
s[::2]      # 'aceg'     every 2nd
s[::-1]     # 'hgfedcba' reversed
s[1:6:2]    # 'bdf'
```

The half-open convention `[start, stop)` gives you three useful invariants:
`len(s[a:b]) == b - a`, `s[:i] + s[i:] == s`, and adjacent slices tile without
overlap or gaps.

**Slices never raise IndexError**, which is a frequent source of silent bugs:

```python
>>> "abc"[10]
IndexError
>>> "abc"[10:20]
''                      # no error, just empty
```

Slice assignment on lists is powerful and worth knowing:

```python
lst = [1, 2, 3, 4, 5]
lst[1:3] = [9]          # [1, 9, 4, 5]     replace, lengths need not match
lst[::2] = [0, 0, 0]    # extended slice assignment MUST match length
del lst[1:3]
lst[:] = other          # replace CONTENTS in place -- visible to all aliases
lst = other             # rebind -- visible to nobody else  (Module 02!)
```

That last pair is Module 02 again. `lst[:] = other` mutates; `lst = other`
rebinds.

---

## 4. The four containers, at a glance

Module 05 goes deep. What you need now is the shape of the decision.

| | `list` | `tuple` | `dict` | `set` |
|---|---|---|---|---|
| Mutable | yes | no | yes | yes |
| Ordered | yes | yes | insertion (3.7+) | no |
| Duplicates | yes | yes | keys unique | no |
| Indexable | yes | yes | by key | no |
| Hashable | no | if contents are | no | `frozenset` is |
| `x in c` | **O(n)** | **O(n)** | **O(1)** avg | **O(1)** avg |
| Typical use | ordered, changing | fixed record | lookup by key | membership, dedupe |

The `in` row is the one that changes programs:

```python
# 10,000 lookups against 10,000 items
if item in big_list:      # ~100,000,000 comparisons
if item in big_set:       # ~10,000 hash lookups
```

Converting a list to a set before a membership-heavy loop is the single most
common easy win in Python performance work.

---

## 5. Hashability

An object is hashable if it has a `__hash__` and its hash never changes. Only
hashable objects can be dict keys or set members.

```python
hash("abc")            # fine
hash((1, 2))           # fine
hash([1, 2])           # TypeError: unhashable type: 'list'
hash((1, [2]))         # TypeError -- tuple hashes its CONTENTS
```

**The rule:** immutable built-ins are hashable; mutable ones are not. Your own
classes are hashable by default (by identity), and Module 09 covers what happens
when you define `__eq__`.

Why the restriction? A dict finds a key by its hash. If a key's hash changed
after insertion, the dict would look in the wrong bucket and the entry would be
unreachable — present in memory, invisible to lookup. Forbidding mutable keys
makes that unrepresentable.

Note that hash equality does not imply object equality — collisions exist, and
dicts handle them by comparing with `==` after matching hashes. This is why
`__eq__` and `__hash__` must agree (Module 09).

```python
>>> hash(1) == hash(1.0) == hash(True)
True
>>> {1: "int", 1.0: "float", True: "bool"}
{1: 'bool'}            # all three are equal AND hash equal: one key, last wins
```

That last one is a genuinely surprising result worth staring at.

---

## Common mistakes in this module

| Mistake | Symptom | Fix |
|---|---|---|
| `0.1 + 0.2 == 0.3` | False | `math.isclose` |
| `Decimal(0.1)` | Inherits the float's error | `Decimal("0.1")` |
| Floats for money | Cents drift over many operations | `Decimal`, or integer cents |
| `open(path)` with no encoding | Works locally, breaks on another OS | `encoding="utf-8"` |
| Mixing `str` and `bytes` | `TypeError: can't concat str to bytes` | Decode at input, encode at output |
| Slicing multibyte `bytes` | Corrupted characters | Decode first, then slice |
| `x in big_list` in a loop | Quadratic runtime | Build a `set` first |
| `"a.b.c".strip(".c")` | Removes too much | `removesuffix` |
| `+=` in a string loop | Quadratic in principle | `"".join(parts)` |
| `round(2.5) == 3` | It is 2 | Banker's rounding; use `Decimal` if you need half-up |
| `nan == nan` | False | `math.isnan(x)` |
| `dict` key `1` vs `True` | They collide | They are equal and hash equal |

---

## Self-check quiz

1. Why is `0.1 + 0.2 != 0.3`, and what is the correct comparison?
2. Why must `Decimal` be constructed from a string?
3. What is the difference between `str` and `bytes`, and where does each belong
   in a program?
4. Why does `len(b"éclair") != len("éclair")`?
5. What does `open("f.txt")` use as its encoding, and why is that a bug?
6. Explain `-7 // 2 == -4` and `-7 % 3 == 2`.
7. Why is `"abc"[10]` an error but `"abc"[10:20]` not?
8. Give the complexity of `in` for `list`, `set`, and `dict`, and say when the
   difference starts to matter.
9. Why can a list not be a dict key? Answer with the mechanism, not the rule.
10. What does `{1: "a", True: "b"}` evaluate to, and why?

---

## Exercises

1. **[`ex01_float_lab.py`](exercises/ex01_float_lab.py)** — Twelve numeric
   predictions, then implement a money type that does not drift.
2. **[`ex02_encoding.py`](exercises/ex02_encoding.py)** — Fix a program that
   corrupts non-ASCII data. Build a robust file reader that handles unknown
   encodings.
3. **[`ex03_text_toolkit.py`](exercises/ex03_text_toolkit.py)** — Implement
   nine text utilities using the right method each time. Tests provided.
4. **[`ex04_container_choice.py`](exercises/ex04_container_choice.py)** — Six
   scenarios, wrong container chosen in each. Fix and measure the difference.

---

## Going deeper

- [Floating Point Arithmetic: Issues and Limitations](https://docs.python.org/3/tutorial/floatingpoint.html)
- [Unicode HOWTO](https://docs.python.org/3/howto/unicode.html) — read this once, properly
- [Format Specification Mini-Language](https://docs.python.org/3/library/string.html#format-specification-mini-language)
- [PEP 686 — UTF-8 mode as default](https://peps.python.org/pep-0686/)
- Ned Batchelder, "Pragmatic Unicode, or, How Do I Stop the Pain?"

---

**Next:** [Module 04 — Control Flow, Functions, and Scope](../04-control-flow-and-functions/README.md)
