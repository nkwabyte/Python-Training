# NotebookLM Visual Prompts — Module 11: Dataclasses, Enums, Value Semantics

---

## Sources to add

| Source | Type |
|---|---|
| `11-dataclasses-and-value-semantics/README.md` | Upload |
| `02-objects-names-data-model/README.md` | Upload |
| `09-dunder-and-data-model/README.md` | Upload |
| https://docs.python.org/3/library/dataclasses.html | Website |
| https://docs.python.org/3/howto/enum.html | Website |

---

## 1. Cinematic Video Overview

**Format:** Explanation
**Visual style:** Paper Craft, or Custom:

```
Clean technical schematic on a dark background. Classes drawn as record cards
with a row per field. Generated methods shown MATERIALISING onto the card as
the decorator is applied. Immutability drawn as a physical seal on the card.
Monospace type for all code. No characters, no mascots.
```

**Steering prompt (paste this whole block):**

```
Audience: a programmer who writes classes by hand, including __init__, __repr__
and __eq__, and has been quietly getting the __eq__/__hash__ contract wrong.

Thesis: most classes are records, the boilerplate for a correct record is
error-prone, and generating it is not merely convenient -- it eliminates a
category of bug. Then: making records IMMUTABLE turns them from a convenience
into a design tool.

1. THE BOILERPLATE, MEASURED. Show a hand-written 30-line class with __init__,
   __repr__, __eq__ and __hash__, then the four-line dataclass that replaces
   it. Then -- and this is the important part -- show the SUBTLE BUG in the
   hand-written version: __eq__ comparing three fields while __hash__ hashes
   two. Reuse Module 09's bucket picture to show the unreachable dict entry
   this produces. State the point: the argument for dataclasses is not
   typing speed, it is that generated code cannot get this wrong.

2. ANNOTATIONS ARE THE MECHANISM. Show the decorator READING __annotations__ at
   class creation time and building the field list from it. Then show a field
   written without an annotation being silently skipped -- not appearing in
   __init__, __repr__ or __eq__ -- while looking completely normal in the
   source. This is the module's most common silent bug and it deserves its own
   frame.

3. default_factory. Reuse Module 02's diagram exactly. Show `= []` producing ONE
   list shared by every instance, then show @dataclass REFUSING to compile it
   at all, then show default_factory=list producing a fresh box per instance.
   Emphasise that a whole bug category became a startup error.

4. FROZEN. Draw a seal being applied to the record card. Show an assignment
   bouncing off. Then show the two things people get wrong:
     (a) frozen gives you __hash__, so the object can be a dict key -- draw it
         going into a bucket.
     (b) frozen does NOT protect a list field. Show the card sealed, with one
         field being an ARROW to a list box outside the seal, and that box being
         appended to. Then show the fix: the field is a tuple, and the tuple is
         inside the seal. This is Module 02's tuple trap and it is the single
         most common dataclass mistake.

5. replace(). Show a frozen record and replace(r, x=10) producing a NEW card
   with one field changed and the OTHER FIELDS' ARROWS POINTING AT THE SAME
   OBJECTS. For a fully immutable record that sharing is free and correct. For
   one with a mutable field it is the shallow-copy trap. Same picture, two
   readings.

6. THE RECORD-TYPE DECISION. Show one piece of data -- an incoming JSON payload
   -- passing through a program, and the right type at each stage: a dict at the
   wire, a Pydantic model at the boundary where validation happens, a frozen
   dataclass inside the domain logic, a NamedTuple returned from a small helper.
   Make the point that these are not competitors; they occupy different
   positions in a pipeline.

7. ENUMS. Show a string-typed status field with a typo ("activ") flowing
   silently through three functions and producing a wrong result at the far end.
   Then the same flow with an Enum, failing loudly at the boundary where the
   string was converted. Then show a match statement over the enum with a
   missing case, and the type checker flagging it -- exhaustiveness that a
   string can never give you.

8. ILLEGAL STATES. The closing idea, and the strongest one in Part 2. Show a
   record with `status: str` and `shipped_at: datetime | None`, and enumerate
   its four combinations -- including "shipped with no timestamp" and "pending
   with a timestamp", both nonsense, both constructible, both needing a check in
   every consumer. Then show the same thing as two separate frozen types where
   the nonsense combinations CANNOT BE BUILT. Show the checks disappearing from
   every consumer.

Do not cover: descriptors, metaclasses, or SOLID. Those are Module 12.
```

---

## 2. Mind Map

**Prompt:**

```
Build a mind map titled "Records and Values".

Branch 1 "@dataclass": what it generates, how it finds fields via annotations,
the annotation-less field trap, and __post_init__ for validation and computed
fields.

Branch 2 "Options": frozen, slots, order, kw_only, eq, repr -- each with what it
buys and what it costs, and a recommended default.

Branch 3 "field()": default_factory, compare=False, repr=False, init=False,
metadata -- each with the situation that calls for it.

Branch 4 "Choosing a record type": dict, TypedDict, NamedTuple, dataclass,
Pydantic -- as positions in a pipeline rather than competitors, with the
trust-boundary rule.

Branch 5 "Enum": Enum, IntEnum, StrEnum, Flag, auto, lookup by value and by
name, iteration, enums with methods, exhaustiveness in match, and the
interoperability trade-off of IntEnum/StrEnum.

Branch 6 "Value objects": definition, value vs entity, the four benefits
(no aliasing, hashable, thread-safe, trivially testable), and the allocation
objection.

Branch 7 "Illegal states": the technique, the two-type refactoring, the
connection to match exhaustiveness, and why it removes checks from consumers.

Branch 8 "Copying": replace() as a shallow copy, why immutable fields make that
safe, and the frozen-with-a-list trap.
```

---

## 3. Study Guide, Quiz, and Flashcards

**Study Guide prompt:**

```
Produce a study guide for someone modelling the data types of a new service.

Include a decision table for record types: given a requirement (arrives as
untrusted JSON, needs to be a dict for an existing API, needs to be a dict key,
needs methods, needs unpacking, is internal domain data, needs runtime
coercion), which type and why.

Include a dataclass options reference: every parameter, what it generates, and
the situation where you would NOT want it.

Include a "dataclass smells" checklist: a field with no annotation, a mutable
default, frozen with a list or dict field, order=True where the field order is
not the sort order, a secret without repr=False, a derived field without
compare=False, and a validation that lives in the caller instead of
__post_init__.

Include an enum section: when a string is fine, when an enum earns its place,
and the specific interoperability cases that justify IntEnum and StrEnum.

End with five data models described in prose, each followed by the types you
would choose and why.
```

**Quiz prompt:**

```
Generate 16 questions on dataclasses, enums and value semantics.

Required predict-the-output cases: a field with no annotation, a mutable default
raising at class creation, a frozen dataclass with a list field being mutated
through that list, replace() sharing a mutable field between two instances,
order=True sorting by an unexpected field, an Enum member compared to its own
value string, json.dumps of a plain Enum versus a StrEnum, a dataclass
constructed with a wrong-typed argument (and the observation that it runs), and
asdict() on a nested structure.

The rest should be "which record type would you choose and why", each with a
concrete scenario and a wrong-but-tempting alternative to rule out.
```

**Flashcards prompt:**

```
20 flashcards. Front: a term or fragment. Back: meaning and the one thing that
goes wrong.

Include: @dataclass, __annotations__ as the field source, field(),
default_factory, __post_init__, frozen, slots, order, kw_only, compare=False,
repr=False, replace(), asdict(), NamedTuple, TypedDict, Pydantic, Enum,
IntEnum, StrEnum, Flag, value object vs entity, illegal states
unrepresentable.
```

---

## The specific visuals to insist on

1. **The 30-line class beside the 4-line dataclass**, with the `__eq__`/
   `__hash__` mismatch highlighted in the hand-written one and its unreachable
   dict entry drawn.
2. **The annotation-less field being skipped** — visibly present in the source,
   absent from the generated `__init__`.
3. **`= []` shared across instances**, then the `ValueError` at class creation,
   then `default_factory` giving fresh boxes.
4. **The sealed card with an arrow escaping to a mutable list** — frozen not
   being enough — and the tuple version with everything inside the seal.
5. **`replace()` sharing the untouched fields' arrows.**
6. **One JSON payload moving through a pipeline**, changing type at each stage:
   dict at the wire, Pydantic at the boundary, frozen dataclass in the domain.
7. **A typo'd status string flowing silently through three functions**, versus
   the same flow failing at the enum boundary.
8. **The four combinations of `status` and `shipped_at`**, two of them nonsense,
   then the two-type version where the nonsense cannot be constructed.

---

## Analogies that work

- **A form with printed fields** for a dataclass: the fields are fixed, every
  copy has the same shape, and two filled-in forms with identical contents are
  the same form.
- **A sealed envelope** for `frozen`, with the crucial refinement: sealing the
  envelope does not stop someone editing a document the envelope merely *points
  at*. That is exactly the list-field trap.
- **A dropdown versus a free-text box** for enum versus string. The dropdown
  cannot contain a typo, and you can enumerate its options.

## Analogies to refuse

- **"Dataclasses are just less typing."** The generated code being *correct* is
  the point; the typing saved is a side effect.
- **"frozen means immutable."** It means the attributes cannot be rebound.
  Saying "immutable" without the qualification produces the list-field bug.
- **"An enum is a set of constants."** It is a type with identity, iteration and
  exhaustiveness checking. The constants framing loses everything that makes it
  worth using.

---

## Accuracy guardrails

```
Accuracy requirements:
- @dataclass finds fields via __annotations__. A class-level assignment WITHOUT
  an annotation is not a field and is silently ignored. State this explicitly.
- frozen=True prevents attribute ASSIGNMENT. It does not deep-freeze. A frozen
  dataclass holding a list is still mutable through that list. Show it.
- Type hints on dataclass fields are NOT enforced at runtime.
  Point(x="not a number") constructs successfully. Say this plainly, because
  the annotation syntax strongly implies otherwise.
- @dataclass raises ValueError at CLASS CREATION for a mutable default. It is
  not a runtime check.
- slots=True on @dataclass requires Python 3.10+. kw_only=True likewise.
  StrEnum requires 3.11+. Name the versions.
- dataclasses.replace() performs a SHALLOW copy.
- Enum members are singletons; compare with `is` or `==` between members, but a
  plain Enum member is NOT equal to its own value. IntEnum and StrEnum are,
  because they subclass int and str.
- asdict() recurses and deep-copies. It is not free on large structures.
- Do not present Pydantic as a replacement for dataclasses generally. It is for
  validating data crossing a trust boundary; inside the program a dataclass is
  lighter.
- __post_init__ on a frozen dataclass must use object.__setattr__ to set
  computed fields.
```

---

## After watching, you should be able to

- [ ] Say what `@dataclass` generates and how it decides what the fields are.
- [ ] Explain why a field without an annotation disappears.
- [ ] Say what `frozen=True` does and, precisely, what it does not.
- [ ] Explain why a frozen dataclass with a `list` field is still mutable, and
      give the fix.
- [ ] Choose between dict, TypedDict, NamedTuple, dataclass and Pydantic for a
      given scenario, and name the trust-boundary rule.
- [ ] Give three things an `Enum` provides that a string constant does not.
- [ ] Define a value object and name four benefits.
- [ ] Take a type with a nonsense field combination and refactor it so the
      nonsense cannot be constructed.
