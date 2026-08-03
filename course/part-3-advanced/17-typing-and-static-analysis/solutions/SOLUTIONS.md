# Solutions — Module 17

## Exercise 17.2 — Narrowing

| # | mypy | Runtime | Point |
|---|---|---|---|
| q01 | error | `AttributeError` on `None` | No guard |
| q02 | clean | safe | `is None` narrows |
| q03 | clean | **see below** | Truthiness narrows too — and can be wrong |
| q04 | error | can fail | Reassignment discards the narrowing |
| q05 | error | can fail | The checker does not follow into helpers |
| q06 | clean | safe | `TypeGuard` tells it to |
| q07 | clean | **unsafe under `-O`** | `assert` narrows and can vanish |
| q08 | clean until Mode grows | safe | Exhaustiveness via `assert_never` |
| q09 | clean | can fail | `Any` disabled every check |
| q10 | error | would corrupt | Invariance, and why |

**q03 is the trap.** `if user:` narrows correctly for a plain `User`, but it
tests *truthiness*, not existence. A `User` subclass defining `__len__` or
`__bool__` — say, a `UserGroup` that is falsy when empty — takes the
"anonymous" branch while being a perfectly good object. Module 09's falsy-object
problem, arriving as a typing bug. **`is None` asks the question you meant.**

**q04.** The reassignment `user = lookup(...)` re-widens the type to
`User | None`, because that is what `lookup` returns. The narrowing from four
lines above is gone, correctly. The fix that is *not* an assert: bind the new
value to a different name and handle its `None` explicitly. Reusing a name for
a differently-typed value is what confused both you and the checker.

**q05 and q06.** mypy analyses one function at a time; `has_email(user)`
returning `True` tells it nothing about `user.email`. `TypeGuard` is how you
promise that a function performs a narrowing — and the promise is **unchecked**.
Lying in a `TypeGuard` silently disables safety for every caller, which makes it
a small, sharp `cast`.

**q07.** mypy accepts it, and `assert` narrows. But `python -O` removes assert
statements (Module 01), so the narrowing that the checker relied on does not
exist at runtime. For internal invariants that is fine. For validating anything
that crosses a boundary, it is a hole. Use an explicit `if not ...: raise`.

**q08 — exhaustiveness is one of the best reasons to use `Literal`.** With
`assert_never(mode)` in the `else`, adding `"append"` to `Mode` produces a mypy
error at *that* line, naming the unhandled value. Delete `assert_never` and the
error disappears — the checker has no way to know the `else` was meant to be
unreachable. **`assert_never` is what turns a `Literal` or an `Enum` into a
checked exhaustive match**, and it is worth adding to every such dispatch.

**q10.** mypy **rejects** `animals: list[object] = dogs`, and the exercise shows
why: if it were allowed, `animals.append(42)` would put an `int` into a list the
caller still believes contains only `str`, and `dogs[1].upper()` would crash.
`list` is invariant because it is *mutable*. `Sequence[str]` **is** acceptable as
`Sequence[object]`, because you cannot write through it. **The general rule:
mutability forces invariance.**

---

## Exercise 17.3 — Typed abstractions

**`Result[T, E]` and when it is worth it in Python.**

It shines where errors are *expected, frequent, and part of the return value* —
parsing user input, validating a batch, or any place you want to collect
failures rather than stop at the first. It makes the error path visible in the
type, so a caller cannot forget it.

It fights the language everywhere else. Python's ecosystem raises; a `Result`
at your boundary means wrapping every library call. There is no `?` operator, so
chaining is verbose. Tracebacks — Python's best debugging feature — are lost.
And a caller who forgets to check gets a `Result` object where they expected a
value, which fails *later* and more confusingly than an exception would.

**Recommendation:** use `Result` inside a bounded domain (a parser, a validator,
a rules engine) and convert to exceptions at its edge. Do not use it as a
project-wide error strategy in Python.

**The `Repository` variance question.** It must be **invariant**. Declaring
`Protocol[T_co]` fails, and mypy tells you why: `save(self, entity: T)` takes `T`
as a *parameter*, which requires contravariance, while `get() -> T | None`
returns it, which requires covariance. A type used in both positions can be
neither. This is the clearest possible demonstration of what variance actually
means — and it is why `list` is invariant and `Sequence` is not.

**The comparison Protocol** has a subtlety worth meeting: the natural
`def __lt__(self, other: T) -> bool` is wrong, because `__lt__` must accept the
*other* operand's type. typeshed's `SupportsRichComparison` uses `Any` for the
parameter precisely because the comparison protocol cannot be expressed
soundly — Module 09's `NotImplemented` dispatch is dynamic in a way the type
system cannot follow.

---

## Exercise 17.1 and 17.4 — Annotating and adopting

The three functions needing a `Protocol` are the ones taking something by
*capability* rather than by class: "anything with `.read()`", "anything
callable with these arguments", "anything that can be closed". Annotating those
as concrete classes is what makes a codebase rigid; annotating them as
`Protocol`s is what makes the types describe the actual contract.

**The adoption order, and it matters:**

1. **Green baseline.** Turn mypy on with everything permissive
   (`ignore_missing_imports`, no `disallow_untyped_defs`) and get CI passing at
   zero errors. You now have a ratchet — errors cannot increase.
2. **Boundaries first.** The public API, data models, and the I/O layer. That
   is where wrong types enter, and typing them is where most of the value is.
3. **Per-module strictness.** Add `[[tool.mypy.overrides]]` entries turning on
   `disallow_untyped_defs` for one module at a time, starting with the ones that
   change most often.
4. **New code strict from day one.** A module never has fewer types than the day
   it was written.
5. **Never big-bang.** Turning on `--strict` across an untyped codebase produces
   thousands of errors, the PR is unreviewable, it stalls, and the team disables
   the checker — leaving you worse off than before you started.

Recording the error count at each step is part of the exercise because the shape
of that curve is the argument: incremental adoption keeps it near zero
throughout, and the big-bang approach spikes it to a number nobody will ever
burn down.
