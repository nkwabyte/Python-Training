# NotebookLM Visual Prompts — Module 13: Plugin Pipeline Project

A build, not a lesson. Generate the architecture video **before** Stage 1 and
the review guide **after** Stage 8.

---

## Sources to add

| Source | Type |
|---|---|
| `13-project-plugin-pipeline/README.md` | Upload |
| The Part 2 module READMEs (08-12) | Upload |
| Your own `src/docpipe/` files, once written | Upload |
| https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/ | Website |

---

## 1. Cinematic Video Overview — architecture, before you build

**Format:** Explanation
**Visual style:** Retro Print, or Custom:

```
Flat architectural schematic on a dark background. The pipeline drawn as a
horizontal series of stages with documents flowing through as small cards.
Immutability shown by each stage EMITTING A NEW CARD rather than altering the
one it received, with the old card remaining visible. Monospace type for code.
No characters, no mascots.
```

**Steering prompt:**

```
Audience: a developer about to build an extensible plugin system, who has built
plugin systems before by defining a base class and asking plugin authors to
subclass it.

Thesis: an extension point defined by INHERITANCE couples every plugin author
to your code. An extension point defined by a PROTOCOL plus a registry couples
nobody to anything, and it is the difference between a plugin system and a
fork.

1. THE TWO EXTENSION MODELS. Draw plugin authors as separate boxes outside your
   package boundary. In the inheritance model, draw an arrow from each plugin
   INTO your package -- they must import your BaseStage. Show what that means
   when you rename a method: every plugin breaks. In the protocol model, draw NO
   arrow: the plugin defines a class with the right shape, the registry records
   a name, and your code never appears in theirs. Show the same rename affecting
   nobody.

2. DOCUMENTS AS IMMUTABLE CARDS. Show a document entering a stage and a NEW card
   emerging, with the original still intact beside it. Then show the provenance
   list growing by one entry per stage, and at the end a completed document
   whose full history is readable off the card itself. Make the point that the
   audit trail was not implemented -- it fell out of immutability.

3. THE MUTABLE-METADATA BUG. Show the alternative: a shared metadata dict, one
   stage writing into it, and every earlier document's card visibly changing
   too. Reuse Module 02's arrows-to-one-box grammar exactly. This is the trap
   most builds hit.

4. LAZY VERSUS EAGER. Show two pipelines side by side over 100,000 documents.
   The eager one materialises a full list between every stage -- draw the memory
   bar filling up. The lazy one pulls ONE document through the whole chain at a
   time -- the memory bar stays flat. Animate a single card travelling the whole
   pipeline before the second card starts. This is the shape that makes the
   memory question disappear, and it previews Module 14.

5. ERROR ISOLATION. Show 100,000 cards entering, and card 5000 catching fire in
   stage 3. Show three designs: the whole run aborting; the failure being
   swallowed silently; and the correct one -- that card diverted to an error
   collection with its stage and cause attached, while cards 5001 onward
   continue. Then show the error BUDGET: after N failures the run stops,
   because 40,000 failures usually means the config is wrong rather than the
   data.

6. VALIDATE BEFORE RUNNING. Show a config with a typo'd option, and two
   timelines: one where it is discovered after 40 minutes of processing, and one
   where it is rejected at second zero with a "did you mean" suggestion. Show
   ALL errors being reported together rather than one per run.

7. WHAT --EXPLAIN IS FOR. Show a short config expanding into the fully resolved
   plan, with every default made explicit. State that in any config-driven tool,
   the gap between what the user wrote and what will actually happen is where
   support tickets come from, and --explain closes it.

Do not cover: argparse specifics, TOML syntax, or how to write tests. Cover the
SHAPE.
```

---

## 2. Mind Map — the plan

**Prompt:**

```
Build a mind map for designing an extensible processing pipeline.

Branch 1 "The extension point": Protocol vs base class, registry, entry points,
duplicate-name handling, and what "adding a stage touches one file" requires.

Branch 2 "The data": immutable documents, derive() rather than mutate,
provenance as a free audit trail, the metadata representation decision, and why
tuple rather than list.

Branch 3 "Execution": one document in, an ITERABLE of documents out (covering
filter, transform and split with one signature), laziness, constant memory, and
what materialising costs.

Branch 4 "Failure": per-document isolation, error budgets, attribution, what
happens when a generator stage raises mid-iteration, and the difference between
a data error and a config error.

Branch 5 "Config": validate before running, report all errors at once, typo
suggestions, resolved plans, and --dry-run guarantees.

Branch 6 "Testability": which dependencies are injected (filesystem, clock, id
generator), what a fake looks like for each, and what "the core runs with zero
filesystem access" requires structurally.

Branch 7 "The six traps": each with its symptom and the design that avoids it.
```

---

## 3. Study Guide — the design review

Generate **after** Stage 8, with your own source files added as sources.

**Prompt:**

```
Act as a senior engineer reviewing this plugin pipeline. The source files are
provided.

SECTION 1 -- COUPLING. Find every place a plugin author would have to import
something from the core package, and every place the core imports a specific
stage. Quote the lines. State what would break if a plugin were written against
version 1.0 and run against 1.1.

SECTION 2 -- MUTABILITY. Find every mutable object that crosses a stage
boundary: a list or dict on a Document, a shared config object, a registry
handed out by a getter. For each, construct the specific two-document sequence
that would corrupt data, and say whether the code currently prevents it.

SECTION 3 -- LAZINESS. Trace the execution path and identify every point where
an iterable is materialised into a list. For each, say whether it is necessary
and what it costs at 100,000 documents. Flag any stage that cannot be lazy and
explain why.

SECTION 4 -- FAILURE. Work through this list and state what actually happens:
a stage raises on document 1; a stage raises on document 50,000; a stage's
generator raises mid-iteration; a stage returns None instead of an iterable; a
stage returns the same Document object it received; two plugins register the
same name; a config references an unregistered stage; the output directory is
read-only; a document's content is 2 GB.

SECTION 5 -- TESTABILITY. List every function that cannot be tested without the
filesystem, the clock, or the network, and give the minimal change for each.

Do not rewrite the code. Ask the questions a reviewer would ask.
```

---

## The specific visuals to insist on

1. **Arrows crossing the package boundary in the inheritance model, and no
   arrows in the protocol model.** This one image is the whole architectural
   argument.
2. **A card's provenance list growing by one per stage**, readable at the end.
3. **The shared metadata dict with several arrows pointing at it**, and one
   write changing everything.
4. **Two memory bars over 100,000 documents** — eager filling, lazy flat.
5. **One card travelling the entire pipeline before the second card starts.**
6. **Card 5000 diverted to an error collection** while 5001 onward continue.
7. **A short config expanding into the fully resolved plan.**

---

## Accuracy guardrails

```
Accuracy requirements:
- Entry points are discovered via importlib.metadata across INSTALLED
  distributions. A decorator or __init_subclass__ registry only sees plugins
  whose module has actually been imported -- state this difference explicitly,
  it is the reason entry points exist.
- A frozen dataclass holding a list or dict is NOT immutable through that
  field. Use tuples and frozen metadata.
- A generator pipeline is lazy: nothing executes until something consumes it.
  A stage that needs ALL documents (sort, dedupe) breaks laziness and must
  buffer -- say so rather than implying everything can stream.
- An exception inside a generator terminates that generator permanently. You
  cannot resume it. Isolation therefore has to happen per document, INSIDE the
  loop, not around the whole pipeline.
- isinstance against a runtime_checkable Protocol checks attribute names only,
  not signatures.
- Timings must use time.perf_counter, not time.time.
- --dry-run must be verified by making side effects impossible (a read-only
  directory), not by trusting a flag.
```

---

## After building, you should be able to

- [ ] Explain why the stage interface is a Protocol and not a base class, in
      terms of who imports whom.
- [ ] Say what provenance cost you to implement, and why.
- [ ] Draw the memory profile of a lazy pipeline versus an eager one.
- [ ] Say exactly what happens when a stage raises on document 50,000.
- [ ] Explain why config validation happens before execution, with a number
      attached.
- [ ] Demonstrate a third-party plugin working with zero changes to your code.
