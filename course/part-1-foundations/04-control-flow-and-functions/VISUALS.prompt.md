# NotebookLM Visual Prompts — Module 04: Control Flow, Functions, and Scope

---

## Sources to add

| Source | Type |
|---|---|
| `04-control-flow-and-functions/README.md` | Upload |
| `course/appendix/idioms-and-pitfalls.md` | Upload |
| https://docs.python.org/3/reference/executionmodel.html | Website |
| https://peps.python.org/pep-0636/ | Website |
| https://peps.python.org/pep-0570/ | Website |

---

## 1. Cinematic Video Overview

**Format:** Explanation
**Visual style:** Custom, with this description:

```
Clean technical schematic on a dark background. Scopes drawn as NESTED
TRANSLUCENT FRAMES, innermost on top, so that a name lookup can be animated as
a search moving outward through the layers. Functions drawn as boxes with a
visible parameter slot row. Monospace type for all code. No characters, no
mascots.
```

**Steering prompt (paste this whole block):**

```
Audience: a programmer fluent in another language who can write Python
functions but has been surprised by UnboundLocalError and by closures capturing
the wrong value.

Thesis: Python resolves names by searching four nested scopes at RUNTIME, but
decides which scope a name BELONGS to at COMPILE time, by scanning the function
body for assignments. Every scope surprise in Python falls out of that split.

1. THE LEGB LADDER. Draw four nested translucent frames: Builtins outermost,
   then Global, then Enclosing, then Local. Animate `print(x)` as a search
   starting in the innermost frame and moving outward until it finds a match.
   Run it three times with x defined at different levels so the viewer sees the
   search stop at different depths.

2. UNBOUNDLOCALERROR. This deserves the most time in the video. Show the
   compiler SCANNING the whole function body before execution, finding
   `counter += 1`, and stamping `counter` as LOCAL for the entire function --
   including on lines above the assignment. Then run the function and show the
   read hitting an empty local slot. Crucially, show the CONTRAST in the same
   frame: a function that only READS the global works fine, and a function that
   MUTATES a global list works fine, because neither is an assignment. Three
   near-identical functions, two working, one failing, with the compile-time
   scan as the only difference.

3. CLOSURES AND CELLS. Show an inner function being returned while its
   enclosing function's frame is destroyed. The captured variable must be drawn
   as a CELL that survives -- a small box that the frame let go of and the inner
   function still holds. Then show two closures made from the same factory with
   different arguments, each holding its own cell.

4. THE LATE-BINDING TRAP. This is the highest-value 60 seconds. Build three
   lambdas in a loop, and draw ALL THREE ARROWS POINTING AT THE SAME CELL. Then
   run the loop to completion so the cell's value becomes 2, and then call the
   lambdas -- all three read the same cell and all three return 2. Then show the
   default-argument fix creating a SEPARATE snapshot value at definition time,
   drawn as three distinct boxes.

5. PARAMETER KINDS. Draw a function signature as a row of labelled slots with
   the / and * markers as physical BARRIERS. Animate several call sites: some
   arguments allowed through a barrier, others bouncing off with a TypeError.
   Show *args sweeping up leftover positionals into a tuple and **kwargs
   sweeping up leftover keywords into a dict.

6. FOR-ELSE. Draw the loop with two exits: a break exit and a natural-
   completion exit. Show the else block attached ONLY to the natural-completion
   exit. Say out loud that reading `else` as `nobreak` makes it obvious, and
   show the flag-variable version it replaces.

7. MATCH. Show a value being matched against patterns as SHAPE FITTING -- a
   nested data structure dropping into a template with holes that capture. Then
   show the capture-versus-compare trap: a bare name pattern accepting anything
   and binding it, versus a dotted name being compared. Make the difference
   visually obvious, because this is the single most common match bug.

Do not cover: classes, decorators, or generators. Those are Modules 08, 15, 14.
```

---

## 2. Mind Map

**Prompt:**

```
Build a mind map titled "Control Flow, Functions, and Scope".

Branch 1 "Statements vs expressions": what each is, why assignment is a
statement, the walrus operator and its legitimate uses, the conditional
expression.

Branch 2 "Loops": for over any iterable, enumerate, zip and strict=True,
for-else and while-else with the "nobreak" reading, break/continue, no labelled
break and the three workarounds, and the never-mutate-while-iterating rule.

Branch 3 "match": literal patterns, capture patterns, sequence patterns, mapping
patterns, class patterns, guards, alternatives with |, the capture-vs-compare
trap, and when a dict dispatch is better.

Branch 4 "Parameters": the six kinds, the / and * markers, what each marker buys
you, the mutable default trap, and the rule that booleans should be keyword-only.

Branch 5 "Scope": the LEGB order, the compile-time local decision,
UnboundLocalError, global, nonlocal, why comprehensions do not leak, and why
global is a design smell.

Branch 6 "Closures": cells, free variables, __closure__, the late-binding trap
and its three fixes, and the connection forward to decorators.

Branch 7 "Type hints": builtin generics, unions, Optional vs omittable, accept
wide return narrow, and the fact that they are not enforced at runtime.
```

---

## 3. Study Guide, Quiz, and Flashcards

**Study Guide prompt:**

```
Produce a study guide for someone about to design a function API that other
people will call.

Include a table of the six parameter kinds with a one-line "use this when".

Include a scope-diagnosis table: given an error or a surprising behaviour
(UnboundLocalError, a closure returning the wrong value, a change not visible
outside a function, a loop variable that unexpectedly still exists), give the
mechanism and the fix.

Include a "signature smells" checklist: boolean positional arguments, more than
about four positional parameters, mutable defaults, parameters that are only
used in one branch, and functions that return different types on different
paths. For each, state the fix.

End with five before/after signature rewrites.
```

**Quiz prompt:**

```
Generate 16 predict-the-output questions on scope, closures, parameters, and
control flow.

Required: an UnboundLocalError case next to a working read-only case, a list
mutation inside a function versus a rebinding, [lambda: i for i in range(3)],
the default-argument fix for it, a for-else that does break and one that does
not, zip with unequal lengths, a mutable default accumulating across calls, a
match with a bare-name pattern, a comprehension loop variable after the
comprehension, and nonlocal versus global.

For each answer, give the mechanism in one sentence and name the wrong mental
model that produces the tempting answer.
```

**Flashcards prompt:**

```
20 flashcards. Front: a term or fragment. Back: meaning and consequence.

Include: LEGB, UnboundLocalError, global, nonlocal, closure, cell,
free variable, late binding, walrus operator, for-else, positional-only /,
keyword-only *, *args, **kwargs, __defaults__, __closure__, match capture vs
compare, guard clause, zip strict, comprehension scope.
```

---

## The specific visuals to insist on

1. **Three near-identical functions**: read a global (works), mutate a global
   list (works), rebind a global int (UnboundLocalError). Same frame, with the
   compile-time scan highlighted as the only difference.
2. **The surviving cell**: an enclosing frame being destroyed while a small box
   it contained floats free, still held by the returned function.
3. **Three arrows into one cell** for the late-binding trap, then three separate
   boxes after the default-argument fix.
4. **The / and \* markers as physical barriers** in a signature, with arguments
   bouncing off them.
5. **For-else as a two-exit diagram**, with the else attached to only one exit.
6. **A match pattern as a template with holes**, and the capture-vs-compare
   difference drawn as "hole that accepts anything" versus "socket that only
   accepts one shape".
7. **A comprehension drawn with its own frame**, so that non-leakage is
   structural rather than a rule to memorise.

---

## Analogies that work

- **A nested set of rooms** for LEGB: you look for a tool in the room you are
  in, then the room outside it, then the building's store, then the street. You
  stop at the first one that has it.
- **The compiler as a surveyor walking the function before anyone moves in**,
  marking every name that gets assigned as "belongs to this room". That is why
  reading before writing fails: the room has the slot, it is just empty.
- **A closure as a backpack**, not a photograph. It holds a reference to the
  variable, so if the variable changes later, the backpack's contents change
  too. This is exactly why late binding surprises people, and the photograph
  intuition is the wrong one.

## Analogies to refuse

- **"A closure captures the value of the variable."** It captures the variable.
  The whole late-binding trap is invisible under the value intuition.
- **"match is a switch statement."** It destructures. Presenting it as switch
  makes every interesting feature look like decoration.
- **Describing `global` as "making a variable visible".** It is visible already;
  `global` permits REBINDING it.

---

## Accuracy guardrails

```
Accuracy requirements:
- The decision that a name is local is made at COMPILE time, from a scan of the
  whole function body, not at the moment of assignment. State this precisely;
  it is the entire explanation of UnboundLocalError.
- Mutating an object referenced by a global name does NOT require the global
  keyword. Only rebinding the name does. Show both.
- for-else runs when the loop completes WITHOUT break, including when the
  iterable was empty. Do not say "when the loop finds nothing".
- Comprehensions have had their own scope since Python 3. Do not repeat the
  Python 2 behaviour.
- Type hints are NOT enforced at runtime by the interpreter. A wrong type does
  not raise. Say so explicitly.
- In match, a bare identifier is a CAPTURE pattern that always matches. Only
  dotted names, literals, and class patterns compare. This must be stated
  explicitly, not implied.
- zip() without strict=True truncates silently to the shortest input. Do not
  present truncation as an error.
- `nonlocal` cannot reach the global scope and cannot reach a class body. Do not
  present it as interchangeable with `global`.
```

---

## After watching, you should be able to

- [ ] Explain UnboundLocalError to someone else in two sentences, mentioning
      compile time.
- [ ] Say why mutating a global list needs no `global` but incrementing a global
      int does.
- [ ] Predict `[lambda: i for i in range(3)]` and give two fixes.
- [ ] Say what `/` and `*` do in a signature and give a reason to use each.
- [ ] State exactly when a `for ... else` clause runs.
- [ ] Explain why `case OK:` always matches and what to write instead.
- [ ] Draw the LEGB search for a name that resolves in the enclosing scope.
