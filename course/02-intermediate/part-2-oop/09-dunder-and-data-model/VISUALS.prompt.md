# NotebookLM Visual Prompts — Module 09: The Data Model

---

## Sources to add

| Source | Type |
|---|---|
| `09-dunder-and-data-model/README.md` | Upload |
| `08-classes-and-encapsulation/README.md` | Upload |
| `course/appendix/cheatsheets.md` | Upload |
| https://docs.python.org/3/reference/datamodel.html | Website |
| https://docs.python.org/3/library/collections.abc.html | Website |

---

## 1. Cinematic Video Overview

**Format:** Explanation
**Visual style:** Custom, with this description:

```
Clean technical schematic on a dark background. Syntax shown on the left as
ordinary Python source, and the dunder call it becomes shown on the right,
connected by a transformation arrow. Protocol dispatch drawn as a flowchart
with explicit fallback branches. Monospace type throughout. No characters, no
mascots.
```

**Steering prompt (paste this whole block):**

```
Audience: a programmer who writes Python classes and treats built-in syntax as
special. They have never seen that len(), +, in, for, with and [] are all
ordinary method calls under a naming convention.

Thesis: Python has almost no special syntax. It has PROTOCOLS. Every operator
and every built-in function is a call to a dunder method, which is why a class
you write can participate in the language on exactly the same terms as a list
or a dict.

1. THE TRANSLATION TABLE, ANIMATED. Show eight pieces of syntax on the left
   TRANSFORMING into their dunder calls on the right, one at a time:
   len(x), x[k], x + y, x == y, for i in x, k in x, with x, x(). Establish the
   pattern before explaining any single method. The viewer should end this
   section thinking "syntax is a call".

2. __repr__ VERSUS __str__. Show one object printed four ways: at the REPL,
   through print(), inside a list, and in an f-string. Highlight that the LIST
   case uses repr on its elements, so a class with only __str__ shows as
   <object at 0x...> in exactly the place you most need to read it -- a
   debugger, a log line, a collection. Then show the same object with a good
   __repr__ and the difference in a realistic traceback.

3. __eq__ AND __hash__ AS A PAIR. This is the most important section and needs
   the most time. Reuse Module 03's bucket picture:
     - two equal objects with EQUAL hashes: both land in the same bucket, and
       lookup finds the entry.
     - two equal objects with DIFFERENT hashes: they land in different buckets,
       and a lookup with an equal key arrives at an empty bucket. Show the
       stored entry sitting there, present in memory and permanently
       unreachable. That image is the whole rule.
     - a hashed attribute being MUTATED after insertion: the same failure,
       arriving a different way.
   Then show why Python sets __hash__ to None when you define __eq__: it is the
   language refusing to let you create the first situation by accident.

4. NotImplemented DISPATCH. Draw the full resolution of a + b as a flowchart:
   try type(a).__add__, if NotImplemented try type(b).__radd__, if still
   NotImplemented raise TypeError. Then run two examples through it: Vector +
   Vector succeeding on the first branch, and 3 * Vector succeeding only via
   __rmul__ on the second. Note the refinement that a subclass's reflected
   method is tried first. Then warn, on screen, that NotImplemented is TRUTHY,
   so returning it from __eq__ and using the result in an if gives a silently
   wrong answer.

5. ITERABLE VERSUS ITERATOR. Draw an iterable as a FACTORY that produces a
   fresh iterator on each __iter__ call, and an iterator as a CURSOR with a
   position. Then run two consecutive for loops over each:
     - over the iterable: two fresh cursors, both loops work.
     - over an object that returned SELF from __iter__: one cursor, already at
       the end, and the second loop silently does nothing.
   That silent second loop is the bug this section exists to prevent.

6. CONTEXT MANAGERS. Show __enter__ and __exit__ around a block, then show the
   SAME diagram with an exception thrown mid-block: __exit__ still runs, and it
   receives the exception type, value and traceback. Show returning False
   letting the exception continue, and returning True swallowing it -- with the
   swallowed exception drawn as visibly discarded, because that is what makes
   it dangerous.

7. THE PROTOCOL PAYOFF. Close by showing one user-defined class that implements
   __len__, __getitem__, __iter__ and __contains__, and then showing it being
   used by len(), a for loop, `in`, slicing, reversed(), sorted(), random.choice
   and list() -- none of which know anything about the class. State the point
   directly: this is what "Pythonic" means. Not clever syntax; participating in
   the same protocols the built-in types use.

Do not cover: inheritance, the MRO, or dataclasses. Those are Modules 10 and 11.
```

---

## 2. Mind Map

**Prompt:**

```
Build a mind map titled "The Python Data Model", organised by WHAT YOU WANT
YOUR OBJECT TO DO rather than by method name.

Branch 1 "I want it to print well": __repr__, __str__, __format__, and the rule
that containers use repr on their elements.

Branch 2 "I want to compare it": __eq__, __hash__ and their two contracts,
NotImplemented, __lt__ and total_ordering, and which methods sorted/max/min
actually require.

Branch 3 "I want it to hold things": __len__, __getitem__, __setitem__,
__delitem__, __contains__, __reversed__, slice handling, and the __getitem__
iteration fallback.

Branch 4 "I want to loop over it": __iter__ vs __next__, iterable vs iterator,
the return-self trap, and __iter__ as a generator.

Branch 5 "I want operators": arithmetic dunders, the reflected __r*__ forms, the
in-place __i*__ forms and their relationship to Module 02's += distinction, the
NotImplemented dispatch chain, and when NOT to overload.

Branch 6 "I want it in a with block": __enter__, __exit__, the three arguments,
the suppression rule, and @contextmanager.

Branch 7 "I want it callable": __call__, and when it beats a closure.

Branch 8 "Everything else": a catalogue by group -- conversion, attribute
access, descriptors, copying, class machinery, pattern matching -- as a lookup
table rather than something to memorise.
```

---

## 3. Study Guide, Quiz, and Flashcards

**Study Guide prompt:**

```
Produce a study guide for someone designing a class that must feel like a
built-in type.

Include a "syntax to dunder" reference table with at least twenty rows, and a
column for the fallback when the primary method is absent (for example: no
__contains__ falls back to iteration; no __str__ falls back to __repr__; no
__bool__ falls back to __len__ then to True; no __iter__ falls back to
__getitem__ from index 0).

Include the __eq__/__hash__ contract as a numbered set of rules, each followed
by a concrete demonstration of what breaks when it is violated.

Include an operator dispatch reference: the full order for a binary operator,
including the subclass refinement, and what NotImplemented does.

Include a checklist for implementing a container type: which methods, in which
order of priority, and what each unlocks.

End with five class designs described only by their requirements ("must be
usable as a dict key", "must support v * 3 and 3 * v", "must be usable in a
with block", "must print usefully inside a list", "must support two independent
for loops"), each followed by the minimal set of dunders needed.
```

**Quiz prompt:**

```
Generate 18 questions on the data model.

At least ten must be "which dunder does this call, and what happens if it is
missing". Include the fallback cases specifically: `in` without __contains__,
print without __str__, bool() without __bool__, iteration without __iter__.

The remaining questions should be predict-the-output. Required: a class with
__eq__ but no __hash__ being put in a set, an object whose hashed attribute is
mutated after insertion into a dict, __eq__ returning False instead of
NotImplemented breaking a comparison with a compatible type, two consecutive
for loops over an object whose __iter__ returns self, __exit__ returning True
while an exception is raised in the block, and 3 * v where only __mul__ is
defined.

For each answer, name the mechanism, not just the result.
```

**Flashcards prompt:**

```
24 flashcards. Front: a piece of syntax or a term. Back: the dunder it calls,
its fallback, and the one thing that commonly goes wrong.

Include: len(), x[k], x[1:3], k in x, for x, reversed(), print(), repr(), f"{}",
==, <, sorted, +, 3 * v, +=, with, calling an instance, bool(), hash(),
NotImplemented, StopIteration, iterable vs iterator, __exit__ return value,
total_ordering, __match_args__.
```

---

## The specific visuals to insist on

1. **Syntax transforming into a method call**, eight times, before any
   explanation. Establish the pattern first.
2. **The same object printed four ways**, with the list case using `repr`.
3. **The unreachable dict entry** — equal objects with unequal hashes landing in
   different buckets, with the stored entry visibly stranded.
4. **The `a + b` flowchart** with both fallback branches drawn, and two examples
   traced through it.
5. **Iterable as a factory, iterator as a cursor**, and the two-consecutive-loops
   test run against both.
6. **`__exit__` running with an exception in flight**, receiving the three
   arguments, and the difference between returning False and True — with the
   swallowed exception drawn as visibly discarded.
7. **One user class used by eight built-in functions** that know nothing about
   it. This is the closing image and the definition of "Pythonic".

---

## Analogies that work

- **An electrical socket standard.** Your class does not need to inherit from
  anything to work with `for` or `len()` — it needs the right shaped pins. The
  protocols are the socket standard; the dunders are the pins.
- **A cursor versus a bookshelf** for iterator versus iterable. A bookshelf can
  be walked many times; a bookmark is at one position and, once at the end,
  stays there.

## Analogies to refuse

- **"Dunder methods are operator overloading."** Overloading is one small part.
  Framing the whole data model that way hides iteration, context management,
  attribute access and descriptors.
- **"Magic methods."** The name suggests something opaque. They are ordinary
  methods with a naming convention, looked up on the type. Use "special methods"
  or "dunder methods" and say that the lookup is completely ordinary.
- **Describing `__eq__`/`__hash__` as "a rule you must remember".** It is a
  consequence of how hash tables work. Show the buckets; the rule then needs no
  memorising.

---

## Accuracy guardrails

```
Accuracy requirements:
- Special methods are looked up on the TYPE, not the instance. Setting
  instance.__len__ does not make len() work. This trips people up and should be
  stated.
- Defining __eq__ sets __hash__ to None automatically. State this as language
  behaviour, not as advice.
- __eq__ should return NotImplemented, not False, for types it does not
  understand. Also state that NotImplemented is TRUTHY, so using a returned
  NotImplemented in a boolean context is a silent bug.
- The operator fallback order is: type(a).__op__, then type(b).__rop__, then
  TypeError -- EXCEPT that if type(b) is a proper subclass of type(a), the
  reflected method is tried first.
- A class defining only __getitem__ IS iterable, via the legacy protocol that
  calls it with 0, 1, 2 ... until IndexError. Do not claim __iter__ is required.
- __exit__ returning a truthy value SUPPRESSES the exception. Returning None
  (the default for a function with no return) does not.
- @total_ordering generates the missing comparisons but they are slower than
  hand-written ones, because each derived operator calls two others.
- __del__ is not a destructor with guaranteed timing. Do not present it as one.
- Do not claim implementing __iter__ requires inheriting from anything.
  collections.abc classes are convenient, not required; the protocol is
  structural.
```

---

## After watching, you should be able to

- [ ] Name the dunder behind ten pieces of syntax without looking.
- [ ] Explain the `__eq__`/`__hash__` contract using buckets rather than a rule.
- [ ] Say why `__eq__` should return `NotImplemented`, and the extra hazard.
- [ ] Trace `3 * v` through the operator dispatch chain.
- [ ] State the difference between an iterable and an iterator, and why it
      matters for a second `for` loop.
- [ ] Say what `__exit__` receives and what its return value controls.
- [ ] List the minimum dunders to make a class usable as a dict key, in a `with`
      block, and in a `for` loop.
