# Solutions — Module 03

---

## Exercise 03.1 Part A — numeric predictions

| Expression | Result | Mechanism |
|---|---|---|
| `0.1 + 0.2 == 0.3` | `False` | Neither 0.1 nor 0.2 is exactly representable in binary |
| `0.1 + 0.2` | `0.30000000000000004` | The accumulated representation error, made visible |
| `round(2.5), round(3.5)` | `(2, 4)` | Round-half-to-even (banker's rounding), the IEEE 754 default |
| `Decimal(0.1)` | `Decimal('0.1000000000000000055511151231257827021181583404541015625')` | Faithfully copies the float's error |
| `Decimal("0.1") + Decimal("0.2") == Decimal("0.3")` | `True` | Decimal stores digits and an exponent, not a binary fraction |
| `-7 // 2` | `-4` | Floor division floors toward negative infinity, not toward zero |
| `-7 % 3` | `2` | The result carries the sign of the divisor, preserving `a == (a//b)*b + a%b` |
| `7 / 1` | `7.0` | `/` is true division and always returns a float |
| `nan == nan` | `False` | IEEE 754 defines NaN as unequal to everything, including itself |
| `1e16 + 1 == 1e16` | `True` | Beyond 2**53, consecutive integers are not distinguishable in a float64 |
| `sum([0.1] * 10) == 1.0` | `False` | Ten accumulated representation errors |
| `True + True`, `sum([True, False, True])` | `2`, `2` | `bool` is a subclass of `int` |

Two of these deserve a second look.

`round(2.5) == 2` is not a bug. Always rounding halves up biases sums upward,
which matters when you round millions of values. Round-half-to-even keeps the
bias centred and is IEEE 754's default mode. If your domain genuinely requires
half-up (many tax rules do), say so explicitly:

```python
Decimal("2.5").quantize(Decimal("1"), rounding=ROUND_HALF_UP)   # 3
```

`nan != nan` has a practical consequence: a NaN in a list breaks sorting,
membership, and deduplication in surprising ways, because the usual identities
no longer hold. `math.isnan(x)` is the only correct test. In pandas (Module 29)
this becomes `.isna()`, and it is the same underlying rule.

---

## Exercise 03.1 Part B — Money

See [`ex01_float_lab_solution.py`](ex01_float_lab_solution.py).

**Representation.** Integer minor units plus a currency code. Exactness becomes
structural rather than a matter of remembering to quantize: there are no
fractions, so there is no rounding mode to get wrong. It also matches how
payment processors and double-entry ledgers actually store money, which makes
serialisation unambiguous.

**Rejecting float construction is the most valuable line in the class.**
`Money(19.99)` accepts a value that is already slightly wrong; the error is then
permanent and invisible. A `TypeError` with a message explaining why costs
nothing and prevents a whole category of incident.

**`allocate` is the part people do not anticipate.** Splitting $10.00 three ways
cannot give three equal parts. The remainder has to go *somewhere*, and
accounting requires that somewhere to be explicit and deterministic — hence
`[3.34, 3.33, 3.33]`, distributing leftover minor units to the earliest parts.
Every invoice-splitting, tax-apportioning, and revenue-sharing system needs
this, and every one that used naive division has a "we lost a cent" ticket in
its history.

---

## Exercise 03.2 — Encoding

See [`ex02_encoding_solution.py`](ex02_encoding_solution.py).

**Should malformed bytes raise?** By default, yes. A decode failure means either
the wrong encoding (a configuration bug) or corrupted input (a data bug), and
both deserve attention. `errors="replace"` turns a loud, findable problem into a
silent one whose only trace is a U+FFFD somewhere downstream. The exception is a
bulk pipeline where partial results beat no results — and there the right shape
is `replace` **plus** a counter of replacement characters **plus** an alert
threshold. The policy should be a decision, never a default.

**BOM ordering is a real bug source.** UTF-32-LE begins with the same two bytes
as UTF-16-LE (`FF FE 00 00` versus `FF FE`), so the longer BOM must be tested
first. Hand-rolled detectors get this wrong constantly.

**"latin-1 never fails" is a warning, not a feature.** Every byte 0-255 maps to
some character, so decoding always succeeds — including on data that is not
latin-1, including on a JPEG. It cannot report an error because it has no
invalid inputs. That makes it a safe *last* resort (it round-trips bytes
losslessly) and a terrible first guess.

**`safe_truncate` is a genuinely common production problem.** Database columns,
log fields, and HTTP headers are limited in *bytes*; your text is measured in
*characters*. `text[:n]` uses the wrong unit; `text.encode()[:n].decode()` raises
when it cuts mid-character. The `errors="ignore"` on the decode is the one place
that flag is correct rather than negligent, because the discarded bytes are
known to be an incomplete character, not lost data. This works because UTF-8 is
self-synchronising; it would not be safe for a stateful encoding.

---

## Exercise 03.3 — Text toolkit

See [`ex03_text_toolkit_solution.py`](ex03_text_toolkit_solution.py). The
method-selection reasoning:

| Function | Method | Why not the obvious alternative |
|---|---|---|
| `normalise_key` | `.split()` with no argument | Splits on any whitespace run *and* drops empties; `.split(" ")` does neither |
| `parse_header` | `.partition(":")` | Always returns 3 items and never raises; `.split(":", 1)` returns a 1-list with no separator, forcing a length check |
| `strip_extension` | `.rpartition(".")` | Handles multi-dot names; the empty-head check is what makes `.hidden` work |
| `is_url` | `.startswith(tuple)` | `startswith` accepts a tuple — one call, no `or` chain, no regex |
| `to_snake_case` | regex with lookarounds | The rule *is* a boundary condition; str methods would need a character loop |
| `align_table` | `f"{cell:<{w}}"` | Nested braces take the width from a variable; manual `ljust` loops are noisier |
| `caseless_equal` | `.casefold()` | `.lower()` leaves ß alone, so `"straße".lower() != "STRASSE".lower()` |

The `to_snake_case` entry is the point of the exercise: **a regex earns its place
when the rule is genuinely a pattern**, and is the wrong tool when a single
string method already expresses the intent. Eight of these nine did not need one.

`.lower()` versus `.casefold()` is worth memorising as a rule: **lower for
display, casefold for comparison.** Casefold applies full Unicode case folding,
handling ß → ss, Greek final sigma, and Cherokee correctly.

---

## Exercise 03.4 — Container choice

See [`ex04_container_choice_solution.py`](ex04_container_choice_solution.py).
Representative measured results:

| Case | Pattern | Before | After | Speedup |
|---|---|---|---|---|
| 1 | Repeated membership | list `in`, O(n·m) | set `in`, O(n) | ~380x |
| 2 | Dedupe with order | `x not in result`, O(n²) | `dict.fromkeys`, O(n) | ~600x |
| 3 | FIFO queue | `list.pop(0)`, O(n²) | `deque.popleft`, O(n) | ~120x |
| 4 | Counting | manual dict branch | `Counter` | ~2x |
| 5 | Lookup by key in a loop | linear scan | dict index | ~1000x |
| 6 | Top-k of n | `sorted()[:k]`, O(n log n) | `heapq.nlargest`, O(n log k) | ~13x |

**The shape of each result matters more than the number.** Cases 1, 2, 3 and 5
are *asymptotic* wins — the ratio grows with n, so whatever you measured
understates the problem at production scale. Cases 4 and 6 are constant-factor
or log-factor wins with roughly stable ratios. Knowing which kind you are looking
at tells you whether the fix is urgent or merely nice.

**Case 5 is the most common real bug in Python code**: a lookup inside a loop.
The break-even is `k·n > n + k`, so building an index pays off from the second
lookup onward. Any lookup inside a loop should be indexed, always.

**Case 3, `list.pop(0)`, deserves emphasis** because it looks innocent. Every
remaining element shifts down one slot, so draining a list this way is O(n²).
`collections.deque` gives O(1) at both ends and is a drop-in replacement.

**Case 6 has a bonus property**: `heapq.nlargest` streams its input, so it works
on an iterator too large to fit in memory. `sorted()` cannot.
