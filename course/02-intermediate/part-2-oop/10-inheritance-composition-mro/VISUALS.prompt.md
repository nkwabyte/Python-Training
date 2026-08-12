# NotebookLM Visual Prompts — Module 10: Inheritance, Composition, and the MRO

---

## Sources to add

| Source | Type |
|---|---|
| `10-inheritance-composition-mro/README.md` | Upload |
| `08-classes-and-encapsulation/README.md` | Upload |
| https://docs.python.org/3/howto/mro.html | Website |
| https://peps.python.org/pep-0544/ | Website |
| https://docs.python.org/3/library/abc.html | Website |

---

## 1. Cinematic Video Overview

**Format:** Explanation
**Visual style:** Custom, with this description:

```
Clean technical schematic on a dark background. Class hierarchies drawn as
graphs with arrows pointing from subclass to base. The MRO drawn as a SINGLE
ORDERED HORIZONTAL LINE beneath the graph, so the flattening of a graph into a
sequence is visible. Method calls traced as a token moving along that line.
Monospace type for all code. No characters, no mascots.
```

**Steering prompt (paste this whole block):**

```
Audience: a programmer who uses inheritance and super() daily and believes
super() means "the parent class". That belief is wrong and this video exists to
replace it.

Thesis: Python flattens a class GRAPH into a single ordered LINE -- the method
resolution order -- and super() means "the next class on that line", where the
line is determined by the type of the INSTANCE, not by where the code is
written.

1. THE FOUNDING DEMONSTRATION. Set up the classic diamond: A at the top, B and
   C both inheriting A, D inheriting B and C. Put a greet() method in each that
   calls super().greet(). Draw the graph. Then draw the MRO beneath it as one
   line: D, B, C, A, object.

   Now run D().greet() and animate the token moving along the LINE: D, then B,
   then C, then A. STOP on the B-to-C step and hold it. B's only base is A. C
   appears nowhere in B's definition. And yet B's super() went to C.

   Say plainly: this is why "super means my parent" is not merely imprecise, it
   is wrong. super() is a position on the instance's line, not an edge in the
   class graph.

2. C3 LINEARISATION. Show the three guarantees as constraints on the line:
   a class before its bases; bases in written order; monotonicity across
   subclasses. Then show a hierarchy where no line can satisfy all three --
   class Z(X, Y) where Y already inherits X -- and show Python REFUSING at class
   definition time with a TypeError. Emphasise that failing at definition is far
   better than resolving arbitrarily at call time.

3. COOPERATIVE __init__. Draw the MRO line with kwargs as a PARCEL being passed
   along it. Each class opens the parcel, takes its own keyword out, and passes
   the rest on. Then show ONE class forgetting to call super().__init__() and
   the parcel simply stopping -- with every class after it on the line silently
   never initialised. Highlight that the broken class cannot see who comes after
   it, which is why this failure is so hard to diagnose and why multiple
   inheritance should be limited to stateless mixins.

4. MIXIN ORDER. Show the same class with the mixin listed before and after the
   concrete base, and the MRO line changing accordingly. Show the mixin's
   override winning in one case and being unreachable in the other. This is the
   whole reason for the "mixins first" rule and it should be one image, not a
   sentence.

5. LISKOV. Dramatise Square/Rectangle. Show a function that sets width to 10 and
   height to 5 and asserts the area is 50. Show it passing with a Rectangle and
   failing with a Square. State the conclusion directly: mathematics is not the
   criterion, behaviour under substitution is. A subclass that surprises a
   function written against the base is not a subtype, whatever the taxonomy
   says.

6. INHERITANCE VERSUS COMPOSITION. Side by side: a Car INHERITING from Engine
   (inheriting the entire Engine API, including things a Car should not expose)
   versus a Car HOLDING an Engine and delegating one method. Show the public
   surface of each as a list, and how much larger the inherited one is. Then
   show a change to Engine propagating into the inheriting Car's API silently,
   and being contained by the composing Car.

7. ABC VERSUS PROTOCOL. Show an ABC as a CONTRACT THE IMPLEMENTER MUST SIGN --
   an arrow from implementation up to the base, and the implementer having to
   import and inherit. Then show a Protocol as a SHAPE THE CALLER DESCRIBES --
   no arrow at all, with a third-party class satisfying it without knowing it
   exists. Show a class from a library you do not control satisfying the
   Protocol and being unable to satisfy the ABC. That is the whole trade-off.

Do not cover: dataclasses, descriptors, or metaclasses. Those are Modules 11
and 12.
```

---

## 2. Mind Map

**Prompt:**

```
Build a mind map titled "Inheritance, Composition, and Interfaces".

Branch 1 "Is-a vs has-a": the Liskov test, what inheritance commits you to
(public API, base __init__ contract, coupling), what composition costs
(delegation), and the default recommendation.

Branch 2 "The MRO": C3's three guarantees, __mro__, super() as a position on
the line rather than a parent edge, and what happens when linearisation fails.

Branch 3 "Cooperative inheritance": every class calls super(), **kwargs
threading, what breaks when one class forgets, and why this argues for
stateless mixins.

Branch 4 "Mixins": the five rules (first in bases, stateless, named -Mixin,
never instantiated, documented required interface) with the reason for each.

Branch 5 "ABCs": abstractmethod, refusal to instantiate, concrete helpers,
isinstance, and the inheritance requirement as the cost.

Branch 6 "Protocols": structural typing, no inheritance, third-party types,
static checking, runtime_checkable and its name-only limitation.

Branch 7 "Duck typing": when to stop using isinstance, capability checks via
collections.abc, and the three places isinstance is genuinely correct.
```

---

## 3. Study Guide, Quiz, and Flashcards

**Study Guide prompt:**

```
Produce a study guide for someone about to review a codebase with a deep class
hierarchy.

Include a decision table: given a relationship between two types (shares code,
is substitutable, needs a shared vocabulary, must work with third-party types,
needs enforcement at instantiation), which tool -- inheritance, composition,
ABC, Protocol, or a plain function -- and why.

Include an MRO worked-example section: four hierarchies of increasing
complexity, each with its MRO derived step by step, and for each a super()
chain traced through it.

Include an LSP violation checklist: a subclass that raises NotImplementedError,
narrows a parameter type, widens a return type, strengthens a precondition,
weakens a postcondition, or adds a required setup step. For each, the symptom a
caller sees.

End with five hierarchies described by symptom, each with the diagnosis and the
refactoring.
```

**Quiz prompt:**

```
Generate 16 questions on inheritance and the MRO.

At least six must give a class hierarchy and ask for the MRO or the output of a
super() chain. Include one hierarchy that cannot be linearised and ask what
happens and when.

Include: a mixin listed after the concrete base, a class that forgets
super().__init__() in a cooperative chain, a Square/Rectangle style LSP
violation, an isinstance check against a runtime_checkable Protocol where the
signature differs but the name matches, and a subclass calling an abstract
method from __init__.

For each answer, state the mechanism -- the MRO position, the missing super
call, the substitution that failed -- and not merely the result.
```

**Flashcards prompt:**

```
20 flashcards. Front: a term or a question. Back: the precise answer.

Include: MRO, C3 linearisation, super(), monotonicity, cooperative
inheritance, mixin, mixin ordering rule, ABC, abstractmethod, Protocol,
structural typing, nominal typing, runtime_checkable, Liskov substitution,
is-a vs has-a, delegation, __mro__, TypeError on inconsistent MRO, duck typing,
when isinstance is correct.
```

---

## The specific visuals to insist on

1. **The graph flattening into a line.** Diamond above, MRO below. Every other
   idea in the module refers back to this image.
2. **The B-to-C step, held on screen.** B's super() reaching a class that is not
   its base. Ask for this explicitly; it is the single most important frame.
3. **The kwargs parcel travelling the line**, and stopping dead when one class
   forgets to pass it on — with the uninitialised classes after it greyed out.
4. **The same class with mixin before and after the base**, and the resulting
   two different MROs side by side.
5. **The Square failing the stretch function** that the Rectangle passes.
6. **Two public-API lists side by side** — the inherited Car versus the
   composing Car — showing how much larger the inherited surface is.
7. **ABC as a signed contract (arrow upward), Protocol as a described shape (no
   arrow)**, with a third-party class satisfying the second and unable to
   satisfy the first.

---

## Analogies that work

- **A queue, not a family tree.** The MRO is a line people stand in.
  `super()` means "hand this to the next person in the queue", and the queue is
  assembled per instance type. This immediately explains why B's `super()` can
  reach C.
- **A relay baton** for cooperative `__init__`. Each runner takes their leg and
  passes the baton; one runner stopping means nobody after them runs, and they
  cannot see who was behind them.
- **A job description versus a certificate.** A Protocol is a job description —
  anyone who can do the work qualifies, whether or not they have heard of you.
  An ABC is a certificate you must go and obtain from a specific institution.

## Analogies to refuse

- **"`super()` calls the parent class."** The core misconception. Do not use the
  word "parent" for `super()` at all.
- **"Inheritance is code reuse."** It is subtyping. Framing it as reuse is
  exactly what produces the hierarchies this module exists to untangle.
- **A biological taxonomy** (Animal → Dog → Poodle). It teaches the syntax and
  the wrong instinct: real inheritance decisions are about substitutability
  under a caller's assumptions, and taxonomy examples never surface that.

---

## Accuracy guardrails

```
Accuracy requirements:
- super() returns a proxy that dispatches to the next class in the MRO OF THE
  INSTANCE'S TYPE. It is not "the parent class" and it is not resolved
  statically from the class definition. Say this explicitly and more than once.
- The MRO is computed by C3 linearisation at CLASS CREATION time. If no
  consistent order exists, the class statement itself raises TypeError.
- Multiple inheritance requires EVERY class in the chain to call super(), and
  compatible signatures. One class omitting it silently skips all classes after
  it in the MRO.
- isinstance against a @runtime_checkable Protocol checks only for the EXISTENCE
  of the named attributes, not their signatures or types. It is a weak check.
- Protocols are checked STATICALLY by a type checker; they impose no runtime
  cost and require no inheritance or registration.
- Abstract methods prevent INSTANTIATION, not definition. A subclass missing one
  is defined fine and fails when constructed.
- Do not claim Python "does not support interfaces". It has two mechanisms, ABC
  and Protocol, with different trade-offs.
- The Liskov substitution principle is about BEHAVIOUR under substitution, not
  about real-world taxonomy. Do not use the word "is-a" without that caveat.
- Do not present mixins as requiring a special language feature. A mixin is an
  ordinary class used in a particular way.
```

---

## After watching, you should be able to

- [ ] Derive the MRO of a diamond and say what happens at each `super()` step.
- [ ] Explain why `B.greet`'s `super()` reaches `C`, in one sentence, without
      the word "parent".
- [ ] Say what breaks when one class in a cooperative chain omits `super()`.
- [ ] Explain why mixins go first, using the MRO.
- [ ] Give the substitution test for whether inheritance is appropriate, and
      apply it to Square/Rectangle.
- [ ] State two things an ABC gives you that a Protocol does not, and vice
      versa.
- [ ] Say exactly what `isinstance` verifies against a runtime-checkable
      Protocol.
