# NotebookLM Visual Prompts — Module 02: Objects, Names, and the Data Model

**This is the highest-value visual set in Part 1.** The entire subject is
invisible in source code, which is exactly the condition under which a diagram
outperforms a paragraph.

Generate after your first read, before the exercises.

---

## Sources to add

| Source | Type |
|---|---|
| `02-objects-names-data-model/README.md` | Upload |
| `course/appendix/glossary.md` | Upload |
| `course/appendix/idioms-and-pitfalls.md` | Upload |
| https://docs.python.org/3/reference/datamodel.html | Website |
| https://docs.python.org/3/library/copy.html | Website |
| https://docs.python.org/3/reference/executionmodel.html | Website |

---

## 1. Cinematic Video Overview

**Format:** Explanation
**Visual style:** Custom, with this description:

```
Clean technical schematic on a dark background. The central visual grammar,
used consistently for the entire video: NAMES are small flat labels or tags,
drawn OUTSIDE any box. OBJECTS are boxes drawn in a separate region
representing the heap. An arrow always goes from a name to an object. A name
NEVER contains a value and is NEVER drawn as a container. Monospace type for
all code. No characters, no mascots, no offices.
```

**Steering prompt (paste this whole block):**

```
Audience: a programmer fluent in another language who has been quietly assuming
that a Python variable is a box holding a value. Every bug in this video comes
from that assumption.

Thesis: a name is a label tied to an object, not a box containing a value.
Assignment never copies. Mutation changes an object; rebinding changes a name.
Those two operations look almost identical in source code and have opposite
consequences.

Establish the visual grammar in the first twenty seconds and never break it:
names are tags OUTSIDE the heap, objects are boxes INSIDE it, and an arrow goes
from tag to box.

1. THE FOUNDING CONTRAST. Show the wrong model and the right model side by
   side, then delete the wrong one permanently. Show `a = [1,2,3]` as one box
   and one tag. Then `b = a` as a SECOND TAG POINTING AT THE SAME BOX. Do not
   draw a second box. The absence of the second box is the whole lesson.

2. MUTATION VERSUS REBINDING. This is the core of the video and deserves the
   most time. Run the same two-line setup twice as a split screen:
     left:  b = a ; b.append(4)   -> the BOX changes, both tags see it
     right: b = a ; b = [9,9,9]   -> a NEW box appears, only b's arrow moves
   Animate the arrow physically detaching and re-attaching in the rebinding
   case, and the box's contents changing while both arrows stay put in the
   mutation case. Then show that `b += [9]` behaves like the LEFT case for a
   list and like the RIGHT case for a tuple, and explain that the difference is
   whether the type implements in-place addition.

3. FUNCTION ARGUMENTS. Show a call as: a new tag created inside the function's
   frame, pointing at the SAME object the caller's tag points at. Then run the
   same two contrasting bodies: one that rebinds the parameter (caller
   unaffected, show the arrow moving inside the frame only) and one that
   mutates it (caller affected). State clearly that Python is neither pass by
   value nor pass by reference; it passes object references by value.

4. THE MUTABLE DEFAULT ARGUMENT. Show the `def` statement EXECUTING and, at
   that moment, creating one list object and storing it on the function object
   itself. Then show three separate calls all pointing at that same single box,
   accumulating. Show the function's __defaults__ tuple visibly containing the
   growing list. Then show the None-sentinel fix creating a fresh box per call.

5. COPIES. Draw the three-layer diagram: alias, shallow copy, deep copy, over a
   nested list of lists. Mutate an inner list and show which of the three
   observers see the change. The shared inner boxes in the shallow case must be
   visually unmistakable.

6. THE [[0]*3]*3 TRAP. Show the multiplication producing THREE ARROWS TO ONE
   BOX, then a single assignment to grid[0][0] visibly changing what all three
   rows display. Then the comprehension version producing three separate boxes.

7. IS VERSUS EQUALS. Two boxes with identical contents: `==` compares contents,
   `is` compares which box. Then show small-integer caching as a pre-allocated
   shelf of boxes for -5 to 256 that names get pointed at, and show 257 getting
   a fresh box each time. Label this explicitly as a CPython implementation
   detail that must never be depended on.

8. REFERENCE COUNTING AND CYCLES. Put a visible counter on each box. Show it
   incrementing on each new arrow and decrementing on del, and the box being
   freed at zero. Then show two boxes pointing at each other, both counters
   stuck at 1 with no arrows from any name -- unreachable but not freed -- and
   the cycle collector sweeping in to find them.

Close on the sentence: mutation changes the object, rebinding changes the name.

Do not cover: classes, inheritance, or the dunder methods. Those are Part 2.
```

---

## 2. Mind Map

**Prompt:**

```
Build a mind map titled "Names and Objects".

Primary branch 1: "Every object has". Sub-branches: identity (id, never
changes), type (type(), effectively fixed), value (mutable or not).

Primary branch 2: "Assignment". Sub-branches: binds a name, never copies,
rebinding vs mutation, augmented assignment and how += differs between list and
tuple.

Primary branch 3: "Mutability". Two sub-trees listing the immutable and mutable
built-in types, plus a leaf for the tuple-containing-a-list case and what it
implies for hashability.

Primary branch 4: "Copying". Sub-branches: alias, shallow, deep, when each is
correct, and the cost of each.

Primary branch 5: "is vs ==". Sub-branches: what each compares, the correct
uses of is (None, sentinels), small-int caching and string interning as CPython
details, and the sentinel pattern for distinguishing "not provided" from None.

Primary branch 6: "Memory". Sub-branches: reference counting, cycles, the
generational collector, weakref, and why __del__ is not a destructor you can
rely on.

Primary branch 7: "Truthiness". Sub-branches: what bool() actually calls, the
falsy values, and the "not provided vs empty" ambiguity.
```

---

## 3. Study Guide, Quiz, and Flashcards

**Study Guide prompt:**

```
Produce a study guide for name-and-object semantics, aimed at someone who will
be debugging an aliasing bug tomorrow.

Include a two-column table: for each of about twelve operations (b = a,
b = a[:], b.append(x), b += [x], b = b + [x], b[0] = x, del b, b = a.copy(),
copy.deepcopy(a), a * 3, dict.update, sorted vs sort) state whether it mutates
the object or rebinds the name, and whether other names observe the change.

Include a diagnosis section: given a symptom ("my second list changed too",
"my function remembered the previous call", "every row of my grid is
identical", "my dict key vanished"), give the mechanism and the fix.

End with a decision procedure for choosing between alias, shallow copy, deep
copy, and restructuring to avoid the copy entirely.
```

**Quiz prompt:**

```
Generate 18 predict-the-output questions on names, objects, mutability, and
copying. Every question must show a short code fragment and ask what it prints.

At least eight must be cases where the intuitive answer is wrong. Required
inclusions: the mutable default argument, [[0]*3]*3, a tuple containing a list
being mutated, += on a list inside a function, a shallow copy of nested data,
`is` comparing two equal 257s versus two equal 5s, sorted() versus .sort()
return values, and mutating a list while iterating over it.

For each answer, state the mechanism in one sentence, not just the output. Then
state what the tempting wrong answer was and which false mental model produces
it.
```

**Flashcards prompt:**

```
20 flashcards. Front: a code fragment or a term. Back: the outcome and the
one-sentence mechanism.

Include: id(), is vs ==, mutable vs immutable, rebinding vs mutation,
__defaults__, the None-sentinel idiom, shallow vs deep copy, small-int caching,
string interning, refcount, reference cycle, weakref, truthiness of empty
containers, why sort() returns None, unhashable type, call by object reference.
```

---

## The specific visuals to insist on

1. **The founding contrast**: two-boxes-two-names versus one-box-two-names, with
   the wrong model visibly crossed out and removed.
2. **The split-screen mutation/rebinding animation.** Same setup, one line
   different, opposite outcomes. Ask for this explicitly; it is the single most
   valuable frame in the module.
3. **`__defaults__` holding the growing list.** Show the function object itself
   as a box with a `__defaults__` slot, and the list inside it accumulating
   across three calls.
4. **The three-layer copy diagram** with shared inner boxes highlighted in a
   different colour from owned ones.
5. **`[[0]*3]*3` as three arrows into one box**, then one assignment visibly
   changing all three displayed rows.
6. **The small-integer shelf**: a pre-allocated rack of boxes labelled -5 to
   256, with names pointing into it, and 257 spawning a fresh box each time.
   Label the rack "CPython implementation detail".
7. **A refcount as a visible number on each box**, incrementing and
   decrementing, then a two-box cycle with both counters stuck at 1 and no
   incoming name arrows.
8. **The tuple that cannot be changed but contains something that can**: a
   sealed outer container with an unsealed inner one.

---

## Analogies that work

- **Luggage tags, not suitcases.** A name is a tag you tie onto a bag. Two tags
  on one bag is normal. Cutting a tag off and tying it to another bag is
  rebinding; putting something into the bag is mutation. Everyone immediately
  understands that adding a shirt to the bag is visible to whoever holds the
  other tag.
- **A shared document link versus a downloaded file.** `b = a` is sending
  someone the link. `copy.deepcopy(a)` is sending a downloaded copy. A shallow
  copy is a new folder containing links to the same files — which is exactly why
  it surprises people.

## Analogies to refuse

- **"A variable is a box that holds a value."** This is the mental model the
  module exists to destroy. Instruct the model explicitly never to use box-as-
  container imagery for names.
- **"Python passes by reference."** It does not, and this phrasing cannot
  explain why rebinding a parameter leaves the caller unaffected. Insist on
  "passes object references by value", also called call by object reference or
  call by sharing.
- **"Immutable means constant."** It means the object cannot change. The name
  can always be rebound. Conflating them makes `s = s.upper()` look illegal.

---

## Accuracy guardrails

Paste into the steering prompt:

```
Accuracy requirements:
- Never say Python is "pass by reference" or "pass by value". It passes object
  references by value. Use the phrase "call by object reference".
- Small-integer caching (-5 to 256) and string interning are CPython
  implementation details, not language guarantees. Label them as such every
  time they appear, and state that code must never depend on them.
- id() returning a memory address is CPython-specific. The language guarantees
  only a unique integer, constant for the object's lifetime, and reusable after
  the object is destroyed.
- Reference counting is CPython-specific. PyPy and GraalPy do not refcount.
  Therefore do not claim that an object is "destroyed immediately" when the last
  name goes away as if it were a language rule.
- Do not describe __del__ as a destructor that reliably runs at a known time. It
  does not. Context managers are the correct cleanup mechanism.
- Immutability applies to the object, not the name. Say so explicitly, because
  the word "constant" is the wrong translation.
- A tuple is immutable but may contain mutable objects. Show this rather than
  saying "tuples cannot change".
- Do not say `is` is "faster ==" or a shortcut for it. They ask different
  questions.
```

---

## After watching, you should be able to

- [ ] Draw the name-and-object diagram for `a = [1]; b = a` without hesitating.
- [ ] State the difference between mutation and rebinding in one sentence and
      give the two-line demonstration from memory.
- [ ] Explain the mutable default argument bug in terms of when `def` runs.
- [ ] Predict the output of `[[0]*3]*3` followed by `grid[0][0] = 1`.
- [ ] Say exactly when `is` is correct, and why `is` with an integer literal is
      not.
- [ ] Explain why `t = ([1],)` allows `t[0].append(2)` but not `t[0] = [2]`.
- [ ] Describe what a shallow copy shares with the original, and name a case
      where that is fine and one where it is a bug.
- [ ] Explain why reference counting alone leaks cycles, and what handles them.
