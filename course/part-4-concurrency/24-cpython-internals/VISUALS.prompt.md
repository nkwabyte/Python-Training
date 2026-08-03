# NotebookLM Visual Prompts — Module 24: CPython Internals

---

## Sources to add

| Source | Type |
|---|---|
| `24-cpython-internals/README.md` | Upload |
| `02-objects-names-data-model/README.md` | Upload |
| `08-classes-and-encapsulation/README.md` (the lookup ladder) | Upload |
| https://docs.python.org/3/library/dis.html | Website |
| https://devguide.python.org/internals/ | Website |

---

## 1. Cinematic Video Overview

**Format:** Explanation
**Visual style:** Custom, with this description:

```
Clean technical schematic on a dark background. The value stack drawn as a
literal vertical stack of plates that instructions push onto and pop from.
Objects drawn as memory blocks with labelled header fields (refcount, type
pointer) followed by their payload. Bytecode listed in monospace beside the
animation, with the current instruction highlighted. No characters, no mascots.
```

**Steering prompt (paste this whole block):**

```
Audience: a competent Python programmer who has been told there is bytecode and
has never looked at it. They have unanswered questions from earlier modules:
why an int is 28 bytes, why += is not atomic, why a comprehension has its own
scope.

Thesis: every surprising behaviour in this course has a mechanical explanation
one level down, and dis() plus sys.getsizeof() are enough to see most of them.
The goal is not to memorise opcodes; it is to stop guessing.

1. THE STACK MACHINE. Disassemble `return a + b` and animate the value stack:
   LOAD_FAST a pushes a plate, LOAD_FAST b pushes another, BINARY_OP pops two
   and pushes one, RETURN_VALUE takes the top. Four instructions, one picture.
   Then show a slightly larger expression -- (a + b) * c -- and let the viewer
   watch the stack rise and fall.

2. SETTLING OLD ARGUMENTS. Rapid-fire, one disassembly each, each answering a
   question from an earlier module:
     - `x = 1 + 2` shows LOAD_CONST 3. Constant folding, from Module 01.
     - `a += 1` shows LOAD, ADD, STORE -- THREE instructions, which is exactly
       why it races in Module 21. Overlay the two-thread interleaving from that
       module on top of these three instructions.
     - A comprehension shows its own code object in co_consts, which is why the
       loop variable does not leak (Module 04).
     - A local shows LOAD_FAST (an array index) and a global shows LOAD_GLOBAL
       (a dict lookup, then builtins). That is the speed difference from
       Module 23, made visible.
   Each of these should take fifteen seconds. The cumulative effect -- that the
   mysteries were all mechanical -- is the point.

3. WHY AN INT IS 28 BYTES. Draw the memory block: refcount, type pointer, size,
   then the digits. Beside it, an 8-byte machine integer. Then scale to a
   million: a million separate 28-byte blocks scattered in memory, plus a
   million 8-byte pointers in the list -- versus a NumPy array as one contiguous
   8 MB block. Show a cache line reading eight useful values from the NumPy
   array and one useful value from the pointer chase. This single image
   justifies Module 23's vectorisation section and Module 08's __slots__
   section at once.

4. getsizeof LIES. Show sys.getsizeof on a list of a million ints reporting
   about 8 MB, then the real cost being nearer 36 MB once the int objects are
   counted. Draw the boundary getsizeof stops at.

5. THE ATTRIBUTE LADDER, COSTED. Reuse Module 08's five-rung ladder, now with a
   cost beside each rung: a data-descriptor check walking the MRO, an instance
   dict lookup, another MRO walk, a bound-method allocation. Then show the type
   cache short-circuiting the MRO walks -- and a monkeypatch INVALIDATING that
   cache for every instance of the type. That is the concrete reason not to
   patch a class in a hot path.

6. SPECIALISATION. The most current and least-known idea in the module. Show a
   loop running with a generic BINARY_OP: check both types, dispatch, maybe call
   __add__. Then, after a few iterations where both operands were always ints,
   show the instruction REWRITING ITSELF IN PLACE into BINARY_OP_ADD_INT, with a
   guard that falls back if a non-int ever appears. Then run a polymorphic loop
   -- sometimes int, sometimes str -- and show the specialisation failing and
   de-optimising.
   Draw the consequence explicitly: benchmarks need a warm-up, and pre-3.11
   performance folklore may simply be wrong now.

7. REFCOUNTS AND GENERATIONS. Reuse Module 02's counter-on-the-box image, then
   go one level down: Py_INCREF and Py_DECREF as macros the interpreter executes
   constantly. Then the three GC generations as three trays, with objects
   promoted from tray 0 upward as they survive. Then gc.freeze() moving
   everything to a permanent tray -- and the pre-fork server case, where it also
   stops the collector from touching (and thereby copy-on-write un-sharing)
   every page the parent shared with its children. Draw the shared pages turning
   private as the collector walks them.

8. CLOSING. Show Lib/dataclasses.py generating __init__ by BUILDING A STRING and
   calling exec on it. Module 11's decorator, completely demystified in one
   frame. End on the point: this is all ordinary code, it is readable, and the
   answer to "why does Python do that" is usually forty lines away.
```

---

## 2. Mind Map

**Prompt:**

```
Build a mind map titled "Under CPython".

Branch 1 "Bytecode": the stack machine, the fifteen opcodes worth knowing,
LOAD_FAST vs LOAD_GLOBAL, and dis() as an argument-settling tool.

Branch 2 "Code objects and frames": co_varnames, co_consts, co_freevars,
co_cellvars and its link to closures, frames, the frame chain and tracebacks.

Branch 3 "Object memory": the PyObject header, why an int is 28 bytes, PEP 393
string storage, getsizeof not following references, small-object caching.

Branch 4 "Attribute lookup, costed": the five rungs, MRO walks, the type cache,
and monkeypatching as cache invalidation.

Branch 5 "Specialisation (3.11+)": adaptive rewriting, monomorphic vs
polymorphic, warm-up, and why old benchmarks mislead.

Branch 6 "Memory management": refcount macros, immediate deallocation, three
generations, thresholds, gc.freeze and copy-on-write in pre-fork servers.

Branch 7 "Reading the source": which files answer which question, starting with
Lib/dataclasses.py and Lib/functools.py.

Branch 8 "What NOT to depend on": bytecode stability, small-int caching, exact
sizes, dict layout -- all implementation details.
```

---

## 3. Study Guide, Quiz, and Flashcards

**Study Guide prompt:**

```
Produce a study guide for someone who wants to answer "why does Python do
that?" without asking anyone.

Include a dis() cookbook: for fifteen constructs (augmented assignment, a
comprehension, an f-string, a with block, a try block, a generator, a
decorator, a method call, a chained comparison, a walrus, a match statement,
a lambda, a global write, a closure, a starred call), the disassembly and the
one thing it explains.

Include a memory reference: the true size of a dozen structures, what
getsizeof includes and excludes, and how to measure the real cost.

Include a "which internal explains this symptom" table: slow attribute access,
memory larger than expected, a benchmark that changes on the second run, a race
on a single statement, a closure capturing the wrong value, an object not being
freed. Each with the mechanism and how to observe it.

Include a specialisation section: what specialises, what prevents it, how to
tell, and what it means for benchmarking.

End with five questions from earlier modules answered purely by disassembly.
```

**Quiz prompt:**

```
Generate 14 questions.

At least six should give a disassembly and ask what the source was, or give
source and ask what the disassembly proves. Include augmented assignment,
constant folding, a comprehension's separate code object, and LOAD_FAST versus
LOAD_GLOBAL.

At least three on memory: the size of an int, the true cost of a list of a
million ints, and what getsizeof omits.

Include: why a monomorphic loop is faster than a polymorphic one in 3.11+, why
a benchmark's first iterations are unrepresentative, and what gc.freeze() does
for a pre-fork server.

For each answer, connect it back to the earlier module whose behaviour it
explains.
```

**Flashcards prompt:**

```
20 flashcards. Front: an opcode, term, or measurement. Back: what it means and
which earlier behaviour it explains.

Include: LOAD_FAST, LOAD_GLOBAL, LOAD_CONST, BINARY_OP, FOR_ITER, MAKE_FUNCTION,
co_cellvars, co_freevars, code object, frame, PyObject header, 28-byte int,
PEP 393, getsizeof limitation, type cache, specialising interpreter,
monomorphic, Py_INCREF, GC generations, gc.freeze, copy-on-write.
```

---

## The specific visuals to insist on

1. **The value stack rising and falling** for `(a + b) * c`.
2. **`a += 1` as three instructions**, with Module 21's thread interleaving
   overlaid on them.
3. **The 28-byte int block beside an 8-byte machine int**, scaled to a million,
   next to a contiguous NumPy array — with a cache line reading eight values
   versus one.
4. **The boundary `getsizeof` stops at.**
5. **The lookup ladder with costs**, and a monkeypatch invalidating the type
   cache for every instance.
6. **An instruction rewriting itself** into a specialised form, then
   de-optimising when a `str` appears.
7. **Three GC trays with promotion**, then `gc.freeze()`, then shared pages
   turning private as the collector walks them.
8. **`dataclasses.py` building `__init__` as a string and calling `exec`.**

---

## Analogies that work

- **A pile of plates** for the value stack: instructions only ever touch the
  top, which is why the bytecode has no register names.
- **A parcel with a shipping label** for the object header: every object carries
  a refcount and a type pointer before its contents, and that overhead is why a
  small number costs 28 bytes.
- **A worn path through a field** for specialisation: the interpreter notices
  which route is always taken and paves it, with a barrier that redirects
  traffic if anything unusual arrives.

## Analogies to refuse

- **"Bytecode is machine code."** It targets a virtual stack machine, not a CPU,
  and it is not stable between versions.
- **"Python compiles to bytecode, so it is compiled."** True and misleading
  without Module 01's framing: it compiles ahead of execution but targets a VM,
  and only syntax is checked statically.
- **Describing the GC as "what frees your objects".** Refcounting frees almost
  everything, immediately. The collector exists only for cycles.

---

## Accuracy guardrails

```
Accuracy requirements:
- Bytecode is an implementation detail and CHANGES between minor versions. Never
  present it as stable API.
- CPython's VM is a stack machine. 3.11+ has an adaptive specialising
  interpreter; 3.13 shipped an experimental JIT. State versions.
- sys.getsizeof does NOT follow references. A container's reported size excludes
  its contents.
- The 28-byte int, 49-byte empty string and similar figures are CPython on
  64-bit builds. Label them.
- Small-integer caching (-5..256) and string interning are implementation
  details, not language guarantees.
- Reference counting frees objects immediately at zero. The generational
  collector exists ONLY to break cycles.
- gc.freeze() moves current objects to a permanent generation; its main benefit
  in pre-fork servers is avoiding copy-on-write page faults caused by the
  collector touching refcount fields.
- Specialisation requires warm-up and is defeated by polymorphic call sites.
  Benchmarks that do not warm up measure unspecialised code.
- Lib/dataclasses.py really does generate __init__ by building source and
  exec'ing it. This is worth showing because it demystifies the decorator.
- Do not claim reading bytecode is necessary for good Python. Frame it as a
  diagnostic tool.
```

---

## After watching, you should be able to

- [ ] Read a four-instruction disassembly and describe the stack at each step.
- [ ] Prove `a += 1` is three operations and connect it to the Module 21 race.
- [ ] Explain why an `int` is 28 bytes and what that means at a million.
- [ ] Say what `sys.getsizeof` omits.
- [ ] Explain what specialisation does and what defeats it.
- [ ] Say why a benchmark needs a warm-up on 3.11+.
- [ ] Explain what `gc.freeze()` does and why a pre-fork server cares.
- [ ] Name a `Lib/` file that answers a question you had earlier in the course.
