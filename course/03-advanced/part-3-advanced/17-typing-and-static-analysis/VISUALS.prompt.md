# NotebookLM Visual Prompts — Module 17: Typing and Static Analysis

---

## Sources to add

| Source | Type |
|---|---|
| `17-typing-and-static-analysis/README.md` | Upload |
| `10-inheritance-composition-mro/README.md` | Upload |
| https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html | Website |
| https://peps.python.org/pep-0544/ | Website |
| https://docs.python.org/3/library/typing.html | Website |

---

## 1. Cinematic Video Overview

**Format:** Explanation
**Visual style:** Custom, with this description:

```
Clean technical schematic on a dark background. Types drawn as SHAPES that fit
into slots -- a value of the wrong shape visibly failing to fit. Type narrowing
drawn as a set of possible shapes SHRINKING as conditions are applied.
Static checking shown as a pass over the code BEFORE any execution, in a
different colour from runtime. Monospace type for all code. No characters.
```

**Steering prompt (paste this whole block):**

```
Audience: a Python programmer who has seen type hints, believes they are either
decorative or enforced, and is not sure which. Both beliefs are wrong in
different ways.

Thesis: hints do nothing at runtime and everything before it. They are a
separate, optional verification pass over your code, and their value is that
they find wrong-type bugs at the place the wrong type was INTRODUCED rather
than three modules later where it finally fails.

1. THE TWO TIMELINES. Draw two parallel timelines: "check time" and "run time".
   Show a hint being read by the checker on the first and IGNORED by the
   interpreter on the second -- run f(x="abc") where x: int and show it
   executing happily. Then show the checker flagging the same line before
   anything ran. State plainly: nothing is enforced, and that is why you must
   actually run the checker.

2. THE BUG TYPING EXISTS TO CATCH. Reuse Module 01's Case 4: a price arrives
   from a form as a string, is stored, passed through two modules, and finally
   fails inside a sum() with a message about multiplying a sequence. Animate the
   distance between the CAUSE (the form handler) and the SYMPTOM (a totals
   function). Then show the checker flagging it at the form handler, with the
   two locations highlighted and the distance annotated. That distance is the
   entire value proposition.

3. NARROWING. This is the most visual idea in the module and deserves the most
   time. Show `user: User | None` as a slot containing TWO possible shapes.
   Then apply `if user is None: return` and animate one shape being REMOVED, so
   that after the guard only User remains and `user.name` is legal. Run the same
   animation for isinstance, for assert, and for an early return. Then show the
   version WITHOUT the guard, where the None shape is still present and the
   attribute access is flagged.

4. WIDE IN, NARROW OUT. Show a function parameter typed as `list` with a
   generator, a tuple and a set all bouncing off it, then the same parameter as
   `Iterable` with all of them fitting. Then the return side: `-> list` telling
   the caller they may index and re-iterate, versus `-> Iterable` leaving them
   guessing. Then the caveat: a function that iterates twice, taking Iterable,
   with the second pass drawn as empty -- and the fix being Sequence in the
   signature.

5. VARIANCE. Show why list[Dog] cannot be passed where list[Animal] is wanted:
   animate the callee appending a Cat to the list, and the caller -- who still
   holds it and believes it contains only Dogs -- finding a Cat. Then show
   Sequence[Dog], which is read-only, being safely acceptable as
   Sequence[Animal]. One picture, and variance stops being abstract.

6. PROTOCOL AS A SHAPE. Reuse Module 10's image: an ABC as a contract the
   implementer must sign, a Protocol as a shape the caller describes. Show three
   unrelated classes -- one from the standard library, one from a third party,
   one of your own -- all fitting the same Protocol slot with no inheritance and
   no import.

7. ANY IS A HOLE. Draw Any as a hole in the checked region, and show the
   infection: every expression involving an Any value becomes Any, so the hole
   SPREADS along the data flow. Then show `object` instead: also permissive at
   the boundary, but requiring a narrowing check before use, so the checking
   resumes. The contrast between a hole that spreads and a gate you must pass is
   the point.

8. GRADUAL ADOPTION. Show a large untyped codebase, and the wrong approach:
   strict mode on everything, 4,000 errors, the checker disabled a week later.
   Then the right approach: a green baseline with everything off, then modules
   turned strict one at a time, with the error count staying manageable and CI
   staying green throughout.

Close on the division of labour: mypy checks the code you wrote, Pydantic
checks the data you received, and neither substitutes for the other.
```

---

## 2. Mind Map

**Prompt:**

```
Build a mind map titled "Typing Python".

Branch 1 "What hints are": not runtime-enforced, read by checkers and tools,
available at runtime via __annotations__, and used by Pydantic and FastAPI.

Branch 2 "Basic vocabulary": builtin generics, unions with |, Optional vs
omittable, Literal, Final, TypeAlias, NoReturn, Self.

Branch 3 "Wide in, narrow out": Iterable vs Sequence vs list, Mapping vs dict,
and the two-pass rule.

Branch 4 "Narrowing": is None, isinstance, assert, early return, TypeGuard, and
what the checker can and cannot follow.

Branch 5 "Generics": TypeVar, bound vs constrained, generic classes, PEP 695
syntax, and variance explained by the append-a-Cat example.

Branch 6 "Structural typing": Protocol, runtime_checkable and its name-only
limitation, and when a Protocol beats an ABC.

Branch 7 "Escape hatches": Any and its infectiousness, object as the safe
alternative, cast, type: ignore with an error code, and what each costs.

Branch 8 "Adoption": the five-step plan, per-module strictness, boundaries
first, and why big-bang conversions fail.

Branch 9 "Static vs runtime": what each catches, what neither catches, and the
validate-at-the-boundary rule.
```

---

## 3. Study Guide, Quiz, and Flashcards

**Study Guide prompt:**

```
Produce a study guide for someone adding types to an existing Python codebase.

Include an annotation reference: for twenty common situations (a list of
strings, a dict of lists, a function argument, a callback, a class that returns
itself, a value that may be absent, a fixed set of string options, an id type
distinct from int, a context manager, a generator, a decorator, JSON-shaped
data), the correct modern annotation and the outdated spelling to avoid.

Include a narrowing reference: which constructs the checker follows (is None,
isinstance, assert, early return, len() checks on tuples, TypeGuard functions)
and which it does not (a helper function that checks for you, without
TypeGuard).

Include an adoption playbook: the ordered steps, which mypy flags to enable
first, how to handle untyped third-party libraries, and how to keep CI green
throughout.

Include a table of static vs runtime validation: what each catches, examples of
bugs only one can find, and where the boundary between them belongs in a web
service.

End with ten untyped function signatures, each with the correct annotation and
the reasoning.
```

**Quiz prompt:**

```
Generate 16 questions.

At least six should show a function with hints plus a call, and ask (a) does it
run, and (b) does the checker complain. The point is separating those two
questions, and every answer must address both.

At least four narrowing puzzles: a None check in one branch only, an isinstance
check inside a helper function, an assert, and a narrowing that is lost after a
reassignment.

Include: list[Dog] passed where list[Animal] is expected, a function taking
Iterable that iterates twice, Any spreading through three expressions, and
Optional used where a default was intended.

For each answer, state what the checker reports AND what happens at runtime.
```

**Flashcards prompt:**

```
20 flashcards. Front: an annotation or term. Back: meaning and the mistake it
prevents.

Include: list[int], X | None, Optional vs default, Iterable, Sequence, Mapping,
Literal, Final, TypeAlias, NewType, Self, NoReturn, Protocol,
runtime_checkable, TypeVar, bound, covariance, invariance, Any, object, cast,
type: ignore[code], TypedDict, overload.
```

---

## The specific visuals to insist on

1. **Two timelines**, with the hint read on one and ignored on the other.
2. **The distance between cause and symptom** in the string-price bug,
   annotated, with the checker collapsing it to zero.
3. **The union slot losing a shape** as each narrowing construct is applied.
4. **A generator, tuple and set bouncing off `list` and fitting `Iterable`.**
5. **The callee appending a Cat** to a `list[Dog]` — variance made concrete.
6. **Three unrelated classes fitting one Protocol slot**, one of them from a
   third-party library.
7. **`Any` as a hole that spreads** along the data flow, versus `object` as a
   gate you must pass.
8. **4,000 errors and a disabled checker**, versus a green baseline with modules
   going strict one at a time.

---

## Analogies that work

- **A spell-checker, not a compiler.** It reads what you wrote, flags what looks
  wrong, changes nothing, and only helps if you actually run it.
- **A door frame.** `Iterable` is a wide doorway that anything walkable fits
  through; `list` is a doorway shaped like exactly one piece of furniture.
- **A safety inspection before opening, versus a fire alarm while open.** Static
  checking is the inspection; runtime validation is the alarm. A building needs
  both, and neither replaces the other.

## Analogies to refuse

- **"Type hints make Python statically typed."** Python remains dynamically
  typed. An optional external checker reads the hints. Blurring this produces
  the belief that `f(x: int)` will reject a string.
- **"Types make code faster."** CPython ignores them entirely. (Some JITs and
  Cython use them, but that is a different mechanism and not what hints are for.)
- **"`Any` means unknown."** `object` means unknown. `Any` means *unchecked*,
  and the difference is that `Any` spreads.

---

## Accuracy guardrails

```
Accuracy requirements:
- Type hints are NOT enforced by CPython at runtime. A wrong type does not
  raise. State this in the first thirty seconds and do not soften it.
- `X | None` describes the VALUE. Omissibility comes from having a DEFAULT.
  These are independent and are constantly conflated.
- list[T] is INVARIANT; Sequence[T] and Iterable[T] are COVARIANT. Explain via
  mutability, not by naming the terms alone.
- Any disables checking and propagates: any expression involving an Any is Any.
  `object` does not -- it requires narrowing before use.
- cast() has NO runtime effect. It is an assertion to the checker.
- isinstance against a @runtime_checkable Protocol checks attribute NAMES only,
  not signatures or types.
- NewType has no runtime cost and creates no new class; at runtime it is the
  underlying type.
- PEP 695 syntax (def f[T]() and class C[T]) requires 3.12+. The TypeVar form
  works everywhere and is what most codebases still use.
- `Optional[X]` and `X | None` are identical in meaning; the union form is the
  modern spelling.
- Do not claim mypy and pyright always agree. They differ on inference in real
  cases; pick one for CI.
```

---

## After watching, you should be able to

- [ ] Say what happens at runtime when a hint is violated, and what happens at
      check time.
- [ ] Explain the difference between `x: str | None` and `x: str = "a"`.
- [ ] Draw the narrowing of a union by `is None`, `isinstance`, and `assert`.
- [ ] Say why `list[Dog]` is not acceptable where `list[Animal]` is wanted.
- [ ] Explain why a two-pass function must take `Sequence`.
- [ ] Say what `Any` does to the expressions around it, and what to use instead.
- [ ] Give the ordered plan for adopting typing without abandoning it.
- [ ] State what Pydantic catches that mypy cannot.
