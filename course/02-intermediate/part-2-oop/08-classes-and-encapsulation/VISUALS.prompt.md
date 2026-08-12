# NotebookLM Visual Prompts — Module 08: Classes and Encapsulation

---

## Sources to add

| Source | Type |
|---|---|
| `08-classes-and-encapsulation/README.md` | Upload |
| `02-objects-names-data-model/README.md` | Upload |
| `course/appendix/glossary.md` | Upload |
| https://docs.python.org/3/reference/datamodel.html#customizing-attribute-access | Website |
| https://docs.python.org/3/library/functions.html#property | Website |

---

## 1. Cinematic Video Overview

**Format:** Explanation
**Visual style:** Custom, with this description:

```
Clean technical schematic on a dark background. Objects drawn as boxes
containing a visible __dict__ table of name-to-value rows. Classes drawn as
boxes above their instances, connected by a type arrow. Attribute lookup drawn
as a numbered search token descending a LADDER of numbered rungs. Monospace
type for all code and attribute names. No characters, no mascots.
```

**Steering prompt (paste this whole block):**

```
Audience: a programmer who has written classes in Java, C#, TypeScript or C++
and is now writing them in Python, where several familiar assumptions are
false. Do not explain what a class is.

Thesis: attribute access in Python is a defined search over dictionaries, and
almost everything surprising about Python classes -- properties, shared class
attributes, bound methods, cached_property, __slots__ -- follows from that one
search order.

1. A CLASS BODY IS CODE. Show `class C:` executing its body top to bottom in a
   fresh namespace -- including a print statement that really runs, and a
   comprehension that really evaluates -- and then that namespace being handed
   to type() to build the class object. End on `type(C) is type`, so the viewer
   sees that a class is an ordinary object bound to a name.

2. THE LOOKUP LADDER. This is the centre of the video. Draw five numbered rungs
   and animate a search token descending them for `obj.x`:
     rung 1: data descriptors on the type (things with __get__ AND __set__)
     rung 2: the instance's own __dict__
     rung 3: the type and its bases, in MRO order
     rung 4: __getattr__
     rung 5: AttributeError
   Then run the SAME animation four times with different setups so the viewer
   sees the token stop at a different rung each time:
     - a plain instance attribute -> stops at 2
     - a class attribute with no instance attribute -> stops at 3
     - a @property -> stops at 1, BEATING the instance dict
     - a missing name -> falls to 4, then 5
   The property overtaking the instance dictionary is the frame that explains
   why @property can intercept an attribute that used to be plain data.

3. BOUND METHODS. Show one function object living in the class, and two
   instances. Show `d.speak` producing a BOUND METHOD -- draw it as the function
   plus a captured reference to d, created at lookup time and thrown away after
   the call. Then show `Dog.speak(d)` being the same call written differently.
   This is what makes `self` explicit rather than magic.

4. THE SHARED CLASS ATTRIBUTE. Reuse Module 02's name-and-object grammar
   exactly. Draw a mutable list as ONE box, with the class holding the only
   reference and two instances finding it at rung 3. Then:
     - a.contents.append("x") -> the shared box changes; b sees it
     - a.contents = ["x"]     -> a NEW box, and a NEW ROW IN a's __dict__,
                                 which now shadows the class attribute at rung 2
   Show the row physically appearing in the instance dictionary. That is the
   whole explanation.

5. PROPERTY AS A LATER DECISION. Show a plain attribute being read and written
   by three call sites. Then replace the attribute with a property, WITHOUT
   changing any call site, and show validation running on the write. State the
   consequence directly: this is why Python code does not need getters written
   in advance, and why writing them anyway is importing a habit that solves a
   problem Python does not have.

6. CACHED_PROPERTY. Show the first access running the function and WRITING THE
   RESULT INTO THE INSTANCE __dict__, then the second access being found at
   rung 2 and never reaching the descriptor at all. Then note that this is
   exactly why it cannot work with __slots__ -- there is no __dict__ to write
   into.

7. __SLOTS__. Show two instances side by side: one with a __dict__ (a hash
   table with spare capacity) and one with a fixed array of named slots. Make
   the memory difference physical, then scale it to a million instances. Then
   show the trade: a new attribute assignment succeeding on the left and
   raising AttributeError on the right.

Do not cover: inheritance, the MRO, or dunder methods. Those are Modules 09
and 10.
```

---

## 2. Mind Map

**Prompt:**

```
Build a mind map titled "Python Classes".

Branch 1 "What a class is": an executable body, a namespace handed to type(),
a class object bound to a name, __dict__.

Branch 2 "Attribute lookup": the five rungs in order, with a leaf under each
saying what stops the search there, plus the two consequences (instance beats
class, but data descriptor beats instance).

Branch 3 "Methods": functions on the class, bound at lookup, self as the first
parameter, classmethod with cls, staticmethod and when it should have been a
module function.

Branch 4 "Class vs instance attributes": what belongs in each, the shared
mutable trap, and the mutation-versus-rebinding distinction from Module 02.

Branch 5 "Privacy": public, _internal as a convention that tools respect,
__mangled and the collision problem it actually solves, and why Python declines
to enforce.

Branch 6 "property": read-only computed attributes, setters with validation,
promoting a plain attribute later without breaking callers, the recursion trap,
the cheapness expectation, and cached_property.

Branch 7 "__slots__": what it removes, what it saves, when the trade is worth
it, and what breaks.

Branch 8 "Real encapsulation": copy on the way in, immutable view on the way
out, and a table of the five ways to expose an internal collection.
```

---

## 3. Study Guide, Quiz, and Flashcards

**Study Guide prompt:**

```
Produce a study guide for someone about to design a class that other people
will use.

Include the attribute lookup ladder as a numbered reference, with a worked
trace for four cases: a plain instance attribute, a class attribute, a
property, and a missing attribute.

Include a decision table: given a need (a value, a computed value, a validated
value, an expensive computed value, an alternative constructor, a helper that
uses no state), which construct to use and why.

Include an "encapsulation audit" checklist: does the constructor copy its
mutable inputs, does any method return an internal mutable object, is any
mutable object a class attribute, does any property do expensive work, is
anything named __x that should be _x.

End with five before/after class rewrites: a class with getters and setters, a
class with a mutable class attribute, a class leaking its internal list, a
class with an expensive property, and a class of staticmethods that should have
been a module.
```

**Quiz prompt:**

```
Generate 16 predict-the-output questions on classes and attribute access.

Required: a mutable class attribute mutated through one instance and read
through another, the same class attribute REBOUND through one instance, a
property shadowed by an attempted instance attribute assignment, a bound method
stored in a variable and called later, a classmethod called on a subclass, a
property that recurses, cached_property accessed twice with a print inside,
__slots__ rejecting a new attribute, and reading a __mangled name from outside
the class.

For each answer, name the lookup rung involved and the mechanism, not just the
output.
```

**Flashcards prompt:**

```
20 flashcards. Front: a term or fragment. Back: meaning and the rung or
mechanism involved.

Include: class body execution, __dict__, bound method, unbound function, self,
cls, classmethod, staticmethod, data descriptor, non-data descriptor, property,
property setter, cached_property, __slots__, name mangling, _single_underscore,
attribute shadowing, __getattr__, MappingProxyType, defensive copy.
```

---

## The specific visuals to insist on

1. **The five-rung ladder**, animated four times with the token stopping at a
   different rung each time.
2. **The property overtaking the instance dictionary** — rung 1 beating rung 2.
   Ask for this explicitly; it is the least intuitive rule in the module.
3. **A row appearing in the instance `__dict__`** at the moment of
   `a.contents = [...]`, next to nothing appearing on `a.contents.append(...)`.
4. **The bound method being constructed at lookup time** and discarded after
   the call.
5. **`cached_property` writing into the instance dict**, and the second access
   never reaching the descriptor.
6. **Two instances side by side**, one with a hash table and one with a fixed
   slot array, scaled to a million.
7. **The leaking getter**: an internal list handed out, and an external caller
   mutating it, next to the tuple-returning version where the same call fails.

---

## Analogies that work

- **A hotel front desk with a hierarchy of lookups.** Ask for a guest's mail:
  the desk checks the special-handling list first (data descriptors), then the
  guest's own pigeonhole (instance dict), then the house standard for all rooms
  (class attributes). The special-handling list beating the pigeonhole is
  exactly why properties win.
- **`self` as a signed-for delivery.** The function exists once in the building;
  looking it up through a specific guest attaches that guest's name to it before
  it is handed over.

## Analogies to refuse

- **"Private means nobody can access it."** Nothing in Python is inaccessible.
  Do not describe `_x` or `__x` as private without immediately saying what they
  actually do.
- **"`__x` is Python's private keyword."** It is name mangling, and its purpose
  is subclass collision avoidance, not access control. This misconception is
  extremely common and must be corrected explicitly.
- **"A property is a getter."** A property is an interception point. Framing it
  as a getter reintroduces the Java habit the module exists to remove.

---

## Accuracy guardrails

```
Accuracy requirements:
- Python has no private access modifier. _name is a convention that tooling
  respects and the interpreter ignores. __name is NAME MANGLING to
  _ClassName__name, whose purpose is avoiding subclass collisions, not access
  control. State both precisely.
- Data descriptors (both __get__ and __set__) are found BEFORE the instance
  dictionary. Non-data descriptors (only __get__, e.g. plain functions and
  cached_property) are found AFTER it. This asymmetry is the mechanism behind
  cached_property and must not be simplified away.
- Mutating an object referenced by a class attribute affects every instance;
  assigning to the attribute through an instance creates an instance attribute
  and affects only that one. Show both.
- __slots__ savings are implementation-specific figures. Give approximate
  ranges and label them as CPython behaviour, not guarantees.
- __slots__ does not make attribute access dramatically faster. The main benefit
  is memory. Do not oversell the speed.
- cached_property stores its result in the instance __dict__, and therefore does
  not work on a class using __slots__ without an explicit __dict__ slot.
- A staticmethod receives neither self nor cls. It is not "a method that can be
  called on the class" -- classmethods can too.
- Type hints on attributes are not enforced at runtime.
```

---

## After watching, you should be able to

- [ ] Recite the five lookup rungs in order and say what stops the search at
      each.
- [ ] Explain why `@property` can intercept an attribute that used to be plain
      data.
- [ ] Predict the outcome of mutating versus rebinding a mutable class
      attribute through an instance.
- [ ] Say what `self` is, mechanically, in one sentence.
- [ ] Explain what `__name` does and what it does not do.
- [ ] Say why Python code rarely has getters and what to do instead.
- [ ] Explain how `cached_property` avoids recomputing, and why `__slots__`
      breaks it.
- [ ] Give three ways to expose an internal list, with the trade-off of each.
