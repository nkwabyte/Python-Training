# Python Mastery: From the Data Model to System Design

A complete, self-paced training course built for one student: you.

This course takes you from what actually happens when you type `python app.py`
all the way to designing, building, and load-testing a production service. It is
calibrated for someone who already programs comfortably in another language, so
it does not spend a chapter explaining what a `for` loop is. It spends that
chapter explaining why Python's `for` loop is a protocol, not a construct, and
what you can build once you know that.

---

## Who this is calibrated for

| Dimension | Setting |
|---|---|
| Prior experience | Comfortable coder. You have shipped something in some language. |
| Python experience | Anywhere from none to "I can write a script" |
| Time budget | 10 to 15 hours per week |
| Duration | 20 weeks (5 months) |
| End goals | Backend/API engineering, data and ML foundations, automation and tooling, then system design |
| Python version | 3.12+ (3.13 features flagged where used; 3.10 fallbacks noted) |

---

## The shape of the course

```
Part 1  Foundations                   Weeks 1-4      Modules 01-07
Part 2  Object-Oriented Python        Weeks 5-8      Modules 08-13
Part 3  Idiomatic and Advanced        Weeks 9-13     Modules 14-20
Part 4  Concurrency and Internals     Weeks 14-15    Modules 21-24
Part 5  Applied Python                Weeks 16-18    Modules 25-30
Part 6  System Design with Python     Weeks 19-20    Modules 31-36
Appendix  Reference material          Ongoing
```

Every one of the 36 modules has the same layout:

```
NN-module-name/
├── README.md            The lesson: concepts, annotated code, mental models,
│                        common mistakes, and a self-check quiz
├── VISUALS.prompt.md    Paste-ready NotebookLM prompts: video explainer,
│                        mind map, study guide, the specific diagrams to
│                        demand, and the accuracy traps to guard against
├── exercises/           Stub .py files with TODOs. Do these.
└── solutions/           Complete, running reference answers. Read these AFTER.
```

---

## How to actually use this

**The 60/40 rule.** Spend at most 40 percent of your time reading and 60 percent
writing code. Python reads like pseudocode, which makes it uniquely good at
producing the *illusion* of understanding. Only the interpreter tells the truth.

**The loop for each module:**

1. Read the README once, straight through, without coding. Get the shape.
2. Generate the visuals from `VISUALS.prompt.md` and watch them. See
   [`course/VISUAL-GUIDE.md`](course/VISUAL-GUIDE.md) for why this step sits
   between the two readings.
3. Re-read it with a REPL open. Type every code block by hand. Do not paste.
   In Python especially, the REPL is a laboratory: `id()`, `type()`, `dir()`,
   and `help()` will answer most of your questions faster than a search engine.
4. Break each example deliberately. Mutate the default argument. Delete the
   `self`. Shadow a builtin. Read the traceback. Read it bottom-up: the last
   line is what went wrong, the lines above are how you got there.
5. Do the exercises without looking at the solutions.
6. Compare against the solutions. Where yours differs, ask: is mine wrong, or
   just different? Both answers are common, and in Python "just different" is
   more common than in most languages.
7. Take the self-check quiz at the bottom of the README. If you cannot answer a
   question in one or two sentences, go back to that section.

**Do not skip the milestone projects** (modules 07, 13, 20, 36). They are where
isolated concepts fuse into working knowledge. A module you can pass a quiz on
but cannot use in a project, you do not know.

**Keep a mistakes log.** Every time a traceback or a silent wrong answer
surprises you, write one line in [`PROGRESS.md`](PROGRESS.md) about what
surprised you. After three months this file will be the most valuable document
in the repo, because it is a map of your own blind spots.

---

## Getting started

1. Read [`SETUP.md`](SETUP.md) and get your environment working. Do not skip the
   linter and type-checker setup. In a dynamically typed language, tooling is
   the safety net that the compiler gives other languages.
2. Skim [`CURRICULUM.md`](CURRICULUM.md) so you know where you are headed.
3. Skim [`course/VISUAL-GUIDE.md`](course/VISUAL-GUIDE.md). Every module ships a
   `VISUALS.prompt.md` you can paste into NotebookLM to generate a video
   explainer, a mind map, and a study guide for that module.
4. Open [`course/part-1-foundations/01-runtime-and-toolchain/README.md`](course/part-1-foundations/01-runtime-and-toolchain/README.md)
   and begin.
5. Track yourself in [`PROGRESS.md`](PROGRESS.md).

---

## Ground rules

These are the habits that separate people who write Python from people who are
trusted with Python.

- **One virtual environment per project. Always.** Never `pip install` into your
  system Python. Module 01 sets this up and Module 30 explains the packaging
  model underneath it.
- **Type-hint every function you write in this course.** Not because Python
  needs it, but because writing the type forces you to decide what the function
  actually accepts and returns. Run the type checker.
- **Never catch bare `except:`.** Catch the exception you expect. Module 16
  explains exactly what a bare except swallows and why it will cost you an
  afternoon eventually.
- **Never use a mutable default argument.** `def f(items=[])` is the single most
  common Python bug in the world. Module 04 shows you why it happens.
- **Read the traceback from the bottom.** The last line names the error, the
  line above it names the place, the lines above that are the story.
- **When in doubt, check the [official docs](https://docs.python.org/3/).** The
  Python standard library documentation is unusually good, and the "Data Model"
  chapter of the language reference is the single most valuable thing you can
  read after Part 2.
- **Prefer the standard library** over a dependency, and prefer a dependency
  over hand-rolled code, except when the whole point of the exercise is to
  hand-roll it.

---

## What "knowing Python" means here

By the end of this course you should be able to do all of the following without
looking anything up:

- Explain why `a = [1,2]; b = a; b.append(3)` changes `a`, in terms of names and
  objects rather than "pass by reference".
- Write a class that behaves correctly under `==`, `in`, `len()`, iteration,
  `with`, and printing, and say which dunder method powers each.
- Write a generator pipeline that processes a file larger than RAM.
- Write a decorator that preserves the wrapped function's signature and
  metadata, and say why `functools.wraps` matters.
- Choose correctly between threads, processes, and `asyncio` for a given
  workload, and defend the choice with the GIL.
- Profile a slow program and produce evidence for what is slow before changing
  anything.
- Build, test, package, containerise and deploy a FastAPI service.
- Take an open-ended design prompt, estimate its load, sketch the architecture,
  name the failure modes, and say what you would build first.
