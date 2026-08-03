# NotebookLM Visual Prompts — Module 12: Design Principles in Python

---

## Sources to add

| Source | Type |
|---|---|
| `12-design-principles-in-python/README.md` | Upload |
| `10-inheritance-composition-mro/README.md` | Upload |
| https://python-patterns.guide/ | Website |
| https://docs.python.org/3/howto/descriptor.html | Website |
| https://peps.python.org/pep-0487/ | Website |

---

## 1. Cinematic Video Overview

**Format:** Explanation
**Visual style:** Custom, with this description:

```
Clean architectural schematic on a dark background. Class-based designs drawn
as stacks of boxes with inheritance arrows; function-based designs drawn as
small labelled tokens being passed along a pipeline. Line counts shown as a
literal bar beside each design so the size difference is visible rather than
asserted. Monospace type for all code. No characters, no mascots.
```

**Steering prompt (paste this whole block):**

```
Audience: a programmer who learned object-oriented design from Java or C# and
is now applying it to Python, producing AbstractFactoryStrategyBuilder
hierarchies that a Python reviewer would replace with a dict and a function.

Thesis: about half the classic design patterns exist to work around the absence
of first-class functions. Python has them, so those patterns collapse into a
few lines. The principles behind the patterns survive; the machinery does not.

1. THE COLLAPSE. Show four patterns side by side, each as the Java-style class
   diagram and then as the Python equivalent, with a line-count bar beside
   each:
     Strategy      : an interface + 3 implementing classes  ->  pass a function
     Command       : an interface + N classes               ->  a function or partial
     Observer      : listener interfaces + registration     ->  a list of callables
     Template Method: abstract base + hook overrides        ->  a function taking hooks
   Do not narrate this as "Python is better". Narrate it as: the pattern was a
   workaround for a missing feature, and the feature is present.

2. SINGLETON. Show the Java singleton with its private constructor,
   double-checked locking and static instance, and the thread-safety hazards
   annotated on it. Then show a Python MODULE, imported once, cached in
   sys.modules, and state that this IS a singleton -- with no locking problem
   and no hidden construction. Reuse the sys.modules cache picture from
   Module 06.

3. THE COMBINATORIAL ARGUMENT. This is the most persuasive image in the module.
   Show a logger with three optional features -- timestamps, JSON, compression.
   Draw the inheritance version as a lattice: with 3 features it needs up to 8
   classes, and animate a FOURTH feature being added so the lattice visibly
   doubles to 16. Then show the composition version: 4 small functions and one
   Logger that takes a tuple of them. Adding the fourth feature adds one
   function and no classes. The two growth curves should be drawn side by side.

4. DEPENDENCY INVERSION WITHOUT A FRAMEWORK. Show a service class constructing
   its own database connection and calling datetime.now() internally -- and a
   test trying to exercise it, blocked by a real database and a moving clock.
   Then show the same class taking both as constructor parameters with
   defaults, and the test passing a dict and a lambda. Say explicitly that this
   IS dependency injection, complete, and required no container, no decorator
   and no library.

5. DESCRIPTORS. Show three properties written out longhand -- thirty lines of
   near-identical validation -- then one descriptor class used three times.
   Then reuse Module 08's lookup ladder: show a DATA descriptor (both __get__
   and __set__) sitting at rung 1, above the instance dictionary, and a
   NON-DATA descriptor (only __get__) sitting below it at rung 3. Show
   cached_property exploiting exactly that gap: first access runs, writes into
   the instance dict, and every later access is caught at rung 2.

6. THE METACLASS LADDER. Present four tools in increasing order of power and
   decreasing order of readability: a descriptor, a class decorator,
   __init_subclass__, a metaclass. For each, show the single thing it can do
   that the previous cannot. Then state the rule: use the LEAST powerful tool
   that solves the problem, and name the three real library uses of metaclasses
   (ABCs, enums, ORM declarative bases) so the viewer knows they are not
   forbidden, only rarely warranted.

7. WHEN NOT TO WRITE A CLASS. Close on a class with one public method and an
   __init__ that only stores its arguments, next to the function it should
   have been. Then list the five diagnostic signs on screen. End on the point
   that a module full of functions is a complete and respectable design, and
   that Python has no requirement for everything to live in a class.

Do not cover: decorators in detail (Module 15) or typing (Module 17).
```

---

## 2. Mind Map

**Prompt:**

```
Build a mind map titled "Design in Python".

Branch 1 "SOLID translated": each letter with its Java expression and its
Python expression, and the practical test for each.

Branch 2 "Patterns that dissolve": a table-style branch of at least ten
patterns, each with the Python one-liner that replaces it.

Branch 3 "Patterns that survive": Adapter, Facade, Proxy, Repository, Unit of
Work -- with the structural problem each actually solves.

Branch 4 "Composition": the 2^n versus n argument, delegation, the logger
example, and what composition costs.

Branch 5 "Dependency injection": constructing vs receiving dependencies,
default arguments as the mechanism, injecting the clock, and why no framework
is needed.

Branch 6 "Descriptors": __get__/__set__/__set_name__, data vs non-data and the
lookup priority consequence, what property/classmethod/cached_property really
are, and when a descriptor beats a property.

Branch 7 "Metaprogramming ladder": descriptor, class decorator,
__init_subclass__, metaclass -- ordered by power, with what each unlocks and
the real-world uses of the last one.

Branch 8 "Not a class": the five signs, and the five situations where a class
genuinely earns its place.
```

---

## 3. Study Guide, Quiz, and Flashcards

**Study Guide prompt:**

```
Produce a study guide for someone reviewing an over-engineered Python codebase.

Include a translation table: for each of twelve classic design patterns, the
Java structure, the Python equivalent, and the approximate line-count
difference.

Include an over-engineering checklist with the symptom and the refactoring for
each: a class with a single public method, a class of only staticmethods, an
abstract base with one implementation, an interface with more than four
methods, a factory class, a singleton class, a DI container, a metaclass, and
inheritance used purely for code reuse.

Include a "least powerful tool" decision procedure: given a requirement
(validate an attribute, react to subclass creation, modify a class after
definition, control class construction itself, share behaviour across unrelated
types), which of descriptor / class decorator / __init_subclass__ / metaclass /
Protocol to use.

End with five over-engineered designs described in prose, each with the
idiomatic Python rewrite and the number of classes eliminated.
```

**Quiz prompt:**

```
Generate 14 questions.

Six should present a small Java-style design and ask for the Python equivalent
and the number of classes it eliminates. Cover Strategy, Singleton, Factory,
Observer, Template Method and Visitor.

Four should present a requirement and ask which metaprogramming tool is the
least powerful one that solves it.

Two should be predict-the-output on descriptors, specifically the data versus
non-data priority: a data descriptor and an instance attribute of the same
name, and cached_property being accessed twice.

Two should present a class and ask whether it should be a class at all, with
reasons.

For each answer, name the language feature that makes the simpler version
possible.
```

**Flashcards prompt:**

```
20 flashcards. Front: a pattern name, principle, or tool. Back: the Python
answer in one line.

Include: Strategy, Command, Singleton, Factory, Observer, Template Method,
Visitor, Builder, Adapter, dependency injection, descriptor, data descriptor,
non-data descriptor, __set_name__, __init_subclass__, class decorator,
metaclass, when a metaclass is warranted, Protocol vs ABC, signs a class should
be a function.
```

---

## The specific visuals to insist on

1. **Four patterns side by side**, class diagram versus Python, with a
   line-count bar making the difference physical.
2. **The Java singleton's locking hazards annotated**, next to a module in
   `sys.modules`.
3. **The 2ⁿ lattice doubling** when a fourth feature is added, next to the
   composition version growing by one function. Both growth curves on one axis.
4. **A test blocked by a real database and a moving clock**, then the same test
   passing a dict and a lambda.
5. **Thirty lines of three properties, versus one descriptor used three times.**
6. **The lookup ladder again**, with a data descriptor at rung 1 and a non-data
   descriptor at rung 3, and `cached_property` writing into rung 2.
7. **The four-rung power ladder** — descriptor, decorator, `__init_subclass__`,
   metaclass — with what each unlocks.
8. **A one-method class beside the function it should have been.**

---

## Analogies that work

- **A pattern as a prosthetic.** Design patterns are prosthetics for missing
  language features. Strategy is a prosthetic for "cannot pass a function". When
  the limb is present, the prosthetic is not an improvement.
- **A power tool rack** for the metaprogramming ladder: you reach for the
  smallest tool that does the job, not because the large one fails but because
  the next person to open the toolbox has to understand what you used.
- **Ingredients versus recipes** for composition versus inheritance: with
  ingredients, a new dish is a new combination; with pre-made dishes, a new
  dish is a new dish.

## Analogies to refuse

- **"Design patterns are best practices."** They are solutions to specific
  problems in specific languages. Presenting them as universally good is what
  produces the codebases this module exists to fix.
- **"Python is not really object-oriented."** It is thoroughly object-oriented
  and also has first-class functions. The point is having both, not lacking one.
- **Describing metaclasses as "advanced" in a way that implies aspirational.**
  Using one is usually a sign of a wrong turn, not of expertise.

---

## Accuracy guardrails

```
Accuracy requirements:
- Do not claim design patterns are useless in Python. Some (Adapter, Facade,
  Proxy, Repository, Unit of Work) solve real structural problems and survive
  intact. Be specific about which dissolve and which do not.
- A module IS a singleton because sys.modules caches it, one per process, per
  interpreter. Note the caveats: subinterpreters and multiprocessing each get
  their own.
- Data descriptors define __get__ AND __set__ (or __delete__) and take priority
  over the instance __dict__. Non-data descriptors define only __get__ and are
  beaten by it. Get this ordering right; cached_property depends on it.
- __init_subclass__ is an implicit classmethod. It runs when a SUBCLASS is
  created, not when the defining class is.
- __set_name__ is called at CLASS creation time with the owner and the
  attribute name. It is what lets a descriptor know its own name.
- Metaclass conflicts are real: a class cannot inherit from two classes with
  unrelated metaclasses. Mention this as a practical cost.
- @dataclass is a class decorator, NOT a metaclass. Say so explicitly, because
  people assume otherwise.
- Dependency injection does not require a framework or a container in Python.
  Constructor parameters with defaults are sufficient and are the idiomatic
  approach.
- Do not present "everything should be a function" either. State the five
  situations where a class genuinely earns its place.
```

---

## After watching, you should be able to

- [ ] Name four patterns that collapse into a function, and write the
      replacement.
- [ ] Explain why a module is a better singleton than a singleton class.
- [ ] Draw the 2ⁿ-versus-n growth argument for composition.
- [ ] Write dependency injection in Python without naming a framework.
- [ ] Say what makes a descriptor a *data* descriptor and why it matters.
- [ ] Choose the least powerful metaprogramming tool for a given requirement.
- [ ] Name two legitimate library uses of metaclasses.
- [ ] Look at a class and say, with reasons, whether it should be a function.
