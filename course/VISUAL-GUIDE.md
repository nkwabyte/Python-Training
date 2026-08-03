# Visual Learning Guide — Using NotebookLM With This Course

Every module folder contains a `VISUALS.prompt.md`. It is a ready-to-paste set of
prompts that turns that module's lesson into visual explainers: a Cinematic Video
Overview, a Mind Map, and a Study Guide with a quiz and flashcards.

The goal is not decoration. Python's hardest ideas are hard for exactly one
reason: **the thing that matters is invisible in the source code.**

```python
b = a
```

Nothing in that line tells you whether you now have one object or two. The
answer determines whether your program is correct. A picture of two arrows
pointing at one box answers it permanently, and no amount of re-reading the line
will.

The same is true of the MRO, of what a closure captured, of where a generator is
suspended, of what the event loop is doing while your coroutine awaits, of which
rows a `groupby` collapsed. Those are the things to make visible.

---

## The workflow, per module

```
1. READ the module README once, straight through, no coding.
2. GENERATE the visuals from VISUALS.prompt.md. Watch or skim them.
3. RE-READ the README with a REPL open. Type every code block.
4. DO the exercises.
5. RE-WATCH the video at 1.5x as review before the self-check quiz.
```

Step 2 sits between the two readings deliberately. Generating visuals before you
have read anything gives you a pleasant film about a topic you cannot yet ask
questions about. Generating them after the first pass means you already have the
vocabulary, and the video fills in the mental model rather than introducing it.

**Never let a video replace step 3.** Watching is passive and produces a strong
feeling of understanding that does not survive contact with the interpreter.
This is a bigger risk in Python than in most languages, because Python *reads*
like it makes sense.

---

## Setting up a notebook

One notebook per **Part**, not per module. Six notebooks total. A notebook that
holds a whole Part's sources produces better cross-references ("this is the same
iterator protocol from Module 14, now driving the async for loop") than six
isolated ones.

### Sources to add for every notebook

Each `VISUALS.prompt.md` lists its own module-specific sources, but these belong
in all six:

| Source | Why |
|---|---|
| The module `README.md` files for that Part | The primary source; everything else is supporting |
| Your own `exercises/` files, after you attempt them | Lets you ask "why did my version differ?" |
| `course/appendix/glossary.md` | Keeps terminology consistent across videos |
| `course/appendix/idioms-and-pitfalls.md` | Makes the model warn you about the traps |
| 2-4 relevant docs.python.org pages (each prompt file names them) | Authoritative detail the model would otherwise approximate |

**Do not dump the entire course into one notebook.** With 36 modules of sources,
the model generalises and the videos become vague. Scoping to one Part is what
keeps them specific.

### Adding documentation pages

Use "Website" as the source type and paste the URL. Each prompt file names the
two or three pages that matter for that module. These are what stop the model
from confidently inventing a function signature or a complexity guarantee.

The four pages worth having in almost every notebook:

- https://docs.python.org/3/reference/datamodel.html — the single most important
  document in Python
- https://docs.python.org/3/glossary.html
- https://docs.python.org/3/library/stdtypes.html
- https://wiki.python.org/moin/TimeComplexity

---

## What each output is good for

| Output | Best for | Weakness |
|---|---|---|
| **Cinematic Video Overview** | Mechanisms in motion: name binding, generator suspension, MRO resolution, event loop scheduling, dataframe reshaping | It will not show you real interpreter behaviour; verify claims in a REPL |
| **Mind Map** | Seeing how a module's concepts connect; revision at a glance | Flat on detail, no sequencing |
| **Study Guide / Quiz / Flashcards** | Active recall before the module self-check | Questions go shallow unless you steer them |
| **Audio Overview** | Passive review on a walk, second or third pass | Useless for anything spatial, which is most of Parts 1, 2 and 4 |
| **Infographic / Slide Deck** | A single reference poster per module | Cramped beyond about six concepts |

The prompt files target the first three. If your NotebookLM offers Infographic,
the "visuals to insist on" section of each file doubles as an infographic brief.

---

## Video Overview settings that matter

**Format.** Use **Explanation**, not Brief, for every module in Parts 1 through
4. Brief is acceptable for the Part 5 applied modules where you want a fast
orientation before diving into docs.

**Visual style.** This affects comprehension more than it sounds like it should:

| Style | Use for |
|---|---|
| **Custom** with a technical-diagram description | Parts 1-4. Anything where the picture must be *accurate*. Each prompt file gives you the exact description to paste. |
| **Paper Craft** | Part 2 class hierarchies and Part 5 data reshaping. Layered physical objects read well for trees and for tables changing shape. |
| **Retro Print** | Part 6 architecture diagrams. Clean flat shapes, good for boxes and arrows. |
| **Anime / Heritage** | Avoid. They add motion and character that compete with the content. |

**Steering prompt.** This is the single highest-leverage field. The prompt files
give you a full paste-in block for it. Generic prompts produce generic videos,
and a generic video about Python is a video about syntax you already know.

---

## The visual vocabulary this course relies on

Several diagrams recur across modules. Ask for them consistently and they
compound; the picture from Module 02 should still be recognisable in Module 22.

| Diagram | First appears | Reused for |
|---|---|---|
| **Names as labels, objects as boxes** — arrows from names to heap objects, never names containing values | 02 | Mutability, function arguments, closures, copies, the ORM identity map |
| **The mutation-vs-rebinding split screen** — same code, two outcomes | 02 | Default args, class attributes, aliasing bugs |
| **The attribute-lookup ladder** — instance dict, then type, then MRO, then `__getattr__` | 08 | Properties, descriptors, inheritance, mixins |
| **The MRO as a single ordered line** derived from a diamond graph | 10 | `super()`, mixins, cooperative inheritance |
| **The suspended frame** — a generator paused mid-body, locals preserved, arrow pointing at the `yield` | 14 | Coroutines, `await`, context managers |
| **The pipeline of pipes** — lazy stages pulling one item at a time versus eager stages materialising full lists | 14 | itertools, streaming, pandas chunking |
| **The wrapper shell** — a function inside another function's returned closure | 15 | Decorators, partials, callbacks |
| **The scheduler board** — one worker, many tasks, each either running, ready, or waiting on I/O | 21, 22 | GIL, event loop, thread pools, queues |
| **Boxes and arrows with a load number on every edge** | 31 | All of Part 6 |

---

## The accuracy problem, and how to handle it

NotebookLM is grounded in your sources, which is why the module README is the
first source you add. It is still a language model. On Python specifically it
will reliably do the following unless told not to:

- **Say "pass by reference" or "pass by value".** Python is neither. It passes
  object references by value, which the course calls *call by object reference*
  or *call by sharing*. This mistake destroys the whole point of Module 02, and
  it is the single most common error in Python teaching material on the
  internet, so the model has seen it thousands of times.
- **Present CPython implementation details as language guarantees.** Small-int
  caching, string interning, dict ordering before 3.7, the exact 28 bytes of an
  int, `__slots__` savings — all implementation-specific.
- **State complexities without the amortized or average-case qualifier.** `list.append`
  is amortized O(1); `dict` lookup is average-case O(1).
- **Describe the GIL as "Python cannot do concurrency".** It cannot do parallel
  *CPU-bound pure-Python* work in threads. That is a much narrower claim.
- **Use pre-3.9 typing idioms** (`List[int]`, `Dict[str, int]`) because they
  appear in older sources, or `%` formatting instead of f-strings.
- **Blur `is` and `==`**, or explain `is` using an example that only works
  because of small-int caching.

Every prompt file has an **Accuracy guardrails** section listing the specific
errors likely for that module, phrased as instructions to paste into the prompt.
That is far more effective than fact-checking afterwards.

**The verification loop.** After watching, take the one claim that surprised you
most and verify it three ways:

```
1. docs.python.org  -- what does the language actually guarantee?
2. the REPL         -- id(), type(), dis.dis(), sys.getsizeof(): what is true here?
3. a 6-line script  -- does it behave that way when you run it?
```

A surprising claim that survives all three has taught you something. One that
does not has taught you more, because you now know where the model is weak and
you will not trust it there again.

---

## Asking the notebook questions

Beyond the generated outputs, the chat is useful in four specific ways.

**1. Explain my traceback.** Paste the whole thing, not just the last line.
Because the module README is a source, the explanation is anchored in the
vocabulary you are currently learning rather than generic forum phrasing.

**2. Compare my solution to the provided one.** Add both files as sources and
ask what differs and which of those differences actually matter. In Python,
where five correct solutions are normal, this is the closest thing to code
review available to a solo learner.

**3. Interrogate a claim.** "The video said dict lookup is O(1). Where in the
sources is that supported, and under what conditions is it not?" NotebookLM
cites sources; if it cannot point at one, treat the claim as unverified.

**4. Generate more exercises.** "Give me eight more problems at the same
difficulty as Exercise 14.3, each with a different failure mode, and do not give
me the answers." This works well and is the main way to extend the course.

Question that does **not** work well: "write the exercise solution for me". You
get something plausible, you learn nothing, and the answers are already sitting
in `solutions/`.

---

## Index of prompt files

### Part 1 — Foundations
- [01 The Runtime and the Toolchain](part-1-foundations/01-runtime-and-toolchain/VISUALS.prompt.md)
- [02 Objects, Names, and the Data Model](part-1-foundations/02-objects-names-data-model/VISUALS.prompt.md)
- [03 Core Types and Their Behaviour](part-1-foundations/03-core-types/VISUALS.prompt.md)
- [04 Control Flow, Functions, and Scope](part-1-foundations/04-control-flow-and-functions/VISUALS.prompt.md)
- [05 Collections and Comprehensions](part-1-foundations/05-collections-and-comprehensions/VISUALS.prompt.md)
- [06 Modules, Packages, and Project Layout](part-1-foundations/06-modules-packages-projects/VISUALS.prompt.md)
- [07 Project: Inventory CLI](part-1-foundations/07-project-inventory-cli/VISUALS.prompt.md)

### Part 2 — Object-Oriented Python
- [08 Classes and Encapsulation](part-2-oop/08-classes-and-encapsulation/VISUALS.prompt.md)
- [09 The Data Model: Dunder Methods](part-2-oop/09-dunder-and-data-model/VISUALS.prompt.md)
- [10 Inheritance, Composition, and the MRO](part-2-oop/10-inheritance-composition-mro/VISUALS.prompt.md)
- [11 Dataclasses, Enums, and Value Semantics](part-2-oop/11-dataclasses-and-value-semantics/VISUALS.prompt.md)
- [12 Design Principles in Python](part-2-oop/12-design-principles-in-python/VISUALS.prompt.md)
- [13 Project: Plugin Document Pipeline](part-2-oop/13-project-plugin-pipeline/VISUALS.prompt.md)

### Part 3 — Idiomatic and Advanced Python
- [14 Iterators, Generators, and Lazy Pipelines](part-3-advanced/14-iterators-and-generators/VISUALS.prompt.md)
- [15 Decorators, Closures, and functools](part-3-advanced/15-decorators-closures-functools/VISUALS.prompt.md)
- [16 Error Handling and Robustness](part-3-advanced/16-error-handling-and-robustness/VISUALS.prompt.md)
- [17 Typing and Static Analysis](part-3-advanced/17-typing-and-static-analysis/VISUALS.prompt.md)
- [18 Testing, Debugging, and Quality](part-3-advanced/18-testing-and-quality/VISUALS.prompt.md)
- [19 The Standard Library, Files, and Serialization](part-3-advanced/19-stdlib-files-serialization/VISUALS.prompt.md)
- [20 Project: A Packaged Library and CLI](part-3-advanced/20-project-library-and-cli/VISUALS.prompt.md)

### Part 4 — Concurrency, Performance, and Internals
- [21 The GIL, Threads, and Processes](part-4-concurrency/21-gil-threads-processes/VISUALS.prompt.md)
- [22 Asyncio](part-4-concurrency/22-asyncio/VISUALS.prompt.md)
- [23 Performance and Profiling](part-4-concurrency/23-performance-and-profiling/VISUALS.prompt.md)
- [24 CPython Internals](part-4-concurrency/24-cpython-internals/VISUALS.prompt.md)

### Part 5 — Applied Python
- [25 Automation, Scripting, and the OS](part-5-applied/25-automation-and-os/VISUALS.prompt.md)
- [26 HTTP, APIs, and Scraping](part-5-applied/26-http-and-scraping/VISUALS.prompt.md)
- [27 Databases and Persistence](part-5-applied/27-databases-and-persistence/VISUALS.prompt.md)
- [28 Building APIs with FastAPI](part-5-applied/28-apis-with-fastapi/VISUALS.prompt.md)
- [29 Data and ML Foundations](part-5-applied/29-data-and-ml-foundations/VISUALS.prompt.md)
- [30 Packaging, Deployment, and Ops](part-5-applied/30-packaging-and-deployment/VISUALS.prompt.md)

### Part 6 — System Design with Python
- [31 Design Fundamentals](part-6-system-design/31-design-fundamentals/VISUALS.prompt.md)
- [32 Service Architecture and Concurrency Models](part-6-system-design/32-service-architecture/VISUALS.prompt.md)
- [33 Caching, Queues, and Background Jobs](part-6-system-design/33-caching-queues-jobs/VISUALS.prompt.md)
- [34 Data at Scale](part-6-system-design/34-data-at-scale/VISUALS.prompt.md)
- [35 Reliability, Observability, and Security](part-6-system-design/35-reliability-observability-security/VISUALS.prompt.md)
- [36 Capstone](part-6-system-design/36-capstone/VISUALS.prompt.md)

---

## A note on effort

Generating a video takes four minutes of your time and produces something that
feels like progress. Debugging why your generator pipeline silently produced an
empty list takes ninety minutes and feels like failure until it works.

The second one is where the learning is. Use the visuals to make the models
stick, not to replace the hours at the keyboard.

Sources: [Generate Video Overviews](https://support.google.com/notebooklm/answer/16454555?hl=en) ·
[Cinematic Video Overviews](https://blog.google/innovation-and-ai/products/notebooklm/generate-your-own-cinematic-video-overviews-in-notebooklm/) ·
[Studio tools: quiz, flashcards, mind map, reports](https://notebooklm-guide.com/notebooklm-interactive-studio-tools)
