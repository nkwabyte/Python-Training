# Solutions — Module 04

---

## Exercise 04.1 — Scope and closure predictions

| # | Output | Mechanism |
|---|---|---|
| q01 | `0` | Read-only access to a global. No assignment in the body, so `counter` stays global |
| q02 | `UnboundLocalError` | `counter += 1` is an assignment, so the compiler marks `counter` local for the whole function; the read happens before any write |
| q03 | `[1] {'debug': True}` | Mutation is not assignment. No `global` needed to call `.append()` or set a key |
| q04 | `outer` | `inner` finds `x` in the enclosing scope (the E of LEGB) |
| q05 | `outer` | `x = "inner"` created a *new local* in `inner`; the enclosing `x` was untouched |
| q06 | `inner` | `nonlocal` rebinds the enclosing `x` rather than creating a local |
| q07 | `[2, 2, 2]` | All three lambdas share one cell; by call time the loop has finished |
| q08 | `[0, 1, 2]` | The default argument is evaluated at `def` time, snapshotting each value |
| q09 | `untouched [0, 1, 4]` | Comprehensions have their own scope since Python 3 |
| q10 | `2` | A plain `for` loop does *not* have its own scope; `j` survives |
| q11 | `q11a else ran`, `q11c else ran` | `else` runs when no `break` occurred — including for an empty iterable |
| q12 | `[10, 11, 12]` | The `n=n` default captures the value per iteration |

The three to sit with:

**q02 next to q01 and q03.** Three near-identical functions, and only the one
containing an assignment fails. The compiler scans the whole body before
execution and marks every assigned name as local for the entire function. That
is why the read on the same line fails: the local slot exists, it is just empty.
Mutation (`items.append`) is not assignment, which is why q03 works without
`global`.

**q07 versus q08.** A closure captures the *variable*, not its value. All three
lambdas hold the same cell, so they all see the loop's final value. The default
argument in q08 is evaluated once per `def`, at definition time, which
snapshots each value — the same "defaults are evaluated at def time" mechanism
that causes the mutable-default bug is here doing exactly what you want.

**q09 versus q10.** Comprehensions have their own scope; `for` loops do not.
Both behaviours are deliberate, and the asymmetry catches people who learned one
rule and assumed it generalised.

---

## Exercise 04.2 — Six signatures

See [`ex02_signatures_solution.py`](ex02_signatures_solution.py). The general
principles behind the six fixes:

**1. Any boolean parameter should be keyword-only.** `resize(img, 800, 600,
True, False, 90)` carries no information about which flag is which, and swapping
two produces silently wrong output rather than an error.

**2. `is None`, not `if not tags`.** An explicitly passed empty list is falsy;
the truthiness check silently discards the caller's list.

**3. Ten parameters means the parameters are a thing.** Group them into a frozen
dataclass. You gain reusable configuration, no signature churn when an option is
added, one documented place for the defaults, and — because it is frozen — a
safe default value with no mutable-default trap.

**4. "Exactly one of these optional parameters" is a union type pretending to be
a signature.** Split it into three named functions. The constraint moves from a
runtime check into the type system. What you lose is a single entry point for
callers who receive a tagged lookup at runtime; if that case is common, add a
thin dispatcher on top rather than collapsing the three.

**5. Offer both a raising and a tolerant version, named so the difference is
visible at the call site.** The standard library models this consistently:
`int()` raises and `d.get()` does not; `d[k]` raises and `next(it, default)`
does not. Never make one function do both depending on a flag — the return type
then depends on an argument *value*, which no type checker can follow.

**6. Use `Iterable` for parameters you only walk once, `Sequence` for ones you
index, and empty tuples as defaults.** A tuple default is immutable, so the
whole mutable-default category disappears at zero cost.

---

## Exercise 04.3 — Closures

See [`ex03_closures_solution.py`](ex03_closures_solution.py).

**The counter** demonstrates that two closures from the same call share one cell
(`inc.__closure__[0] is reset.__closure__[0]`), while two closures from
different calls do not. That is the entire mechanism, and it is what makes the
next three possible.

**The memoiser** is `functools.lru_cache`, written out. Three findings worth
keeping:

- An unhashable argument raises `TypeError` when building the key, and that is
  the *right* behaviour. Silently skipping the cache hides a performance cliff;
  stringifying the argument produces wrong hits for distinct objects with equal
  reprs.
- `f(1)`, `f(1.0)` and `f(True)` share **one** cache entry, because all three
  are equal and hash equally (Module 03). If your function distinguishes them,
  the cache returns wrong answers. This is a real footgun in `lru_cache` too.
- Caching a function with side effects means the side effect happens only once.
  `@cache` on a `save()` function makes the second save silently do nothing.

**The event bus** hides a subtle bug the tests catch: `emit` must iterate a
**snapshot** of the handler list. A handler that unsubscribes itself — the very
common "once" listener — mutates the list mid-iteration and silently skips the
next handler. That is Module 02's rule appearing in real code.

**The retry decorator** is the three-level shape that Module 15 formalises:
factory returns decorator returns wrapper. Writing it once makes decorator
syntax stop being magic. Two details matter: re-raise the *original* exception
rather than wrapping it (the traceback is the useful part), and use
`functools.wraps` — the solution also shows what `wraps` does by hand, which is
why unwrapped decorators break `help()`, pdb, Sphinx, pytest fixtures, and
FastAPI's signature inspection.

And the design point: **retrying a non-idempotent operation is a
duplicate-side-effect generator.** If `charge_card()` times out, you do not know
whether the charge happened. The fix is an idempotency key (Module 33), not more
retries.

---

## Exercise 04.4 — Pattern matching

See [`ex04_match_solution.py`](ex04_match_solution.py).

**Mapping patterns match a subset of keys.** `{"type": "click", "pos": (1,2),
"timestamp": 999}` still matches `case {"type": "click", "pos": (x, y)}`. For an
event router that is the right default — events gain fields over time, and a
router that broke on every new field would be unusable. It is tolerant reading,
the same principle as protocol design. The cost is that this is *not* validation:
a typo'd key is silently accepted. Validate at the boundary with a schema
(Module 28); route on shape here.

**`int(x)` inside a pattern is a class pattern, not a call.** It means "match if
this is an `int`, and bind it to `x`". This is how you get type checks inside
patterns.

**`@dataclass` generates `__match_args__`**, which is what makes positional class
patterns like `Point(0, 0)` work. Remove the decorator and you get
`TypeError: Point() accepts 0 positional sub-patterns`. `NamedTuple` provides it
too; a plain class does not.

**The capture trap.** A bare identifier in a pattern position matches *anything*
and binds it. Only dotted names, literals, and class patterns compare. `_` is
the one bare name that does not bind.

There is a genuinely useful safety net here that the exercise makes you
discover: if a bare-name capture is followed by any further cases, CPython
refuses to compile the file —

```
SyntaxError: name capture 'OK' makes remaining patterns unreachable
```

So the compiler catches the trap whenever it makes later branches dead. It
*cannot* catch it when the capture is the last case, which is exactly the form
that ships to production. Enable the mypy and ruff rules for the remainder.

---

## Exercise 04.5 — Six loops

See [`ex05_control_flow_solution.py`](ex05_control_flow_solution.py).

| # | Was | Became | Eliminated |
|---|---|---|---|
| 1 | manual index + while | `enumerate(names, start=1)` | counter, bounds check, off-by-one |
| 2 | `range(len(...))` | `zip(..., strict=True)` | double subscripting, silent truncation |
| 3 | found flag + break | `any(...)` | the flag |
| 4 | two appends in a loop | two comprehensions | branching noise |
| 5 | nested loops + sentinel | a `set` of complements | **O(n²) → O(n)** |
| 6 | `+=` on strings | two `join`s | quadratic building, trailing-separator dance |

Three notes.

**Case 4 has a real caveat.** Two comprehensions iterate the input twice. That is
fine for a materialised list with a cheap predicate, and it is a *silent bug* for
a generator or a file handle — the second pass sees an exhausted iterator and
returns nothing. The solution file includes a test that demonstrates exactly
this. When the input is an iterator or the predicate is expensive, use the
single-pass loop.

**Case 5 is the only one that is not just tidier.** Replacing a search with a
lookup takes it from O(n²) to O(n): for each element, the partner you need is
fully determined, so ask a set whether you have already seen it. This is the
single most useful pattern in algorithm problems.

It also carries a warning: the two versions return the pair in different orders
for some inputs. An "equivalent" rewrite that changes result ordering is a
classic silent regression — check whether callers care before swapping.

**Case 6, but for real CSV, use the `csv` module** (Module 19). Hand-rolled CSV
writing is correct for exactly as long as no field contains a comma, a quote, or
a newline.
