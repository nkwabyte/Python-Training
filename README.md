# Python Mastery: From Your First Program to System Design

A complete, self-paced Python course in four levels, from someone who has never
written a line of code to someone who can design, build, instrument, and defend
a production service.

It began as one course for one student, calibrated for an experienced
programmer. By request it is now four, so that a beginner, an improver, an
experienced engineer, and someone brushing up before an interview can each
start in the right place and take the same path from there.

---

## The four levels

```
course/
├── 01-beginner/        12 modules   B01-B12          10 weeks   6-8 h/week
├── 02-intermediate/    13 modules   01-13            8 weeks    10-15 h/week
├── 03-advanced/        17 modules   14-30            12 weeks   10-15 h/week
└── 04-system-design/   16 modules   D01-D10, 31-36   10 weeks   10-15 h/week
```

| Level | What it is for |
|---|---|
| **[01 Beginner](course/01-beginner/README.md)** | Programming from zero. What a program is, data, decisions, loops, collections, functions, text, files, errors, modules, a first class, and a finished CLI project. |
| **[02 Intermediate](course/02-intermediate/README.md)** | What the interpreter is actually doing, and how to model problems with types the Python way. Foundations and object-oriented Python. |
| **[03 Advanced](course/03-advanced/README.md)** | Code that survives review and load. Generators, decorators, typing, testing, concurrency, profiling, CPython internals, then applied work: automation, HTTP, databases, FastAPI, data, deployment. |
| **[04 System Design](course/04-system-design/README.md)** | Data structures and algorithms first, then architecture: estimation, service models, caching and queues, data at scale, reliability, and a capstone. |

Full detail, week by week, is in [`CURRICULUM.md`](CURRICULUM.md).

---

## Where should you start?

| If this describes you | Start at |
|---|---|
| You have never written code | [Module B01](course/01-beginner/b01-first-program-and-the-interpreter/README.md) |
| You program in another language, but not Python | [Module 01](course/02-intermediate/part-1-foundations/01-runtime-and-toolchain/README.md) |
| You write Python scripts but could not explain what `b = a` does to the object | [Module 02](course/02-intermediate/part-1-foundations/02-objects-names-data-model/README.md) |
| You are fluent with classes, generators, and decorators | [Module 14](course/03-advanced/part-3-advanced/14-iterators-and-generators/README.md) |
| You ship production Python and want scale and interview readiness | [Module D01](course/04-system-design/part-6-data-structures-and-algorithms/d01-complexity-and-measurement/README.md) |

Two honest self-tests before skipping a level. If you cannot explain why
`a = [1,2]; b = a; b.append(3)` changes `a` in terms of names and objects, do
not skip Intermediate. If you cannot say what `functools.wraps` protects, do not
skip Advanced.

---

## What every module looks like

```
module-name/
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

**Do not skip the milestone projects** (B12, 07, 13, 20, 36). They are where
isolated concepts fuse into working knowledge. A module you can pass a quiz on
but cannot use in a project, you do not know.

**Keep a mistakes log.** Every time a traceback or a silent wrong answer
surprises you, write one line in [`PROGRESS.md`](PROGRESS.md) about what
surprised you. After three months this file will be the most valuable document
in the repo, because it is a map of your own blind spots.

---

## Getting started

1. Read [`SETUP.md`](SETUP.md) and get your environment working. Beginners can
   stop after the first two sections; everyone else should also set up the
   linter and type checker. In a dynamically typed language, tooling is the
   safety net that the compiler gives other languages.
2. Skim [`CURRICULUM.md`](CURRICULUM.md) so you know where you are headed.
3. Skim [`course/VISUAL-GUIDE.md`](course/VISUAL-GUIDE.md). Every module ships a
   `VISUALS.prompt.md` you can paste into NotebookLM to generate a video
   explainer, a mind map, and a study guide for that module.
4. Open the level README for wherever you are starting, and begin.
5. Track yourself in [`PROGRESS.md`](PROGRESS.md).

---

## Ground rules

These are the habits that separate people who write Python from people who are
trusted with Python.

- **One virtual environment per project. Always.** Never `pip install` into your
  system Python. Modules B10 and 01 set this up, and Module 30 explains the
  packaging model underneath it.
- **Type-hint every function you write in this course.** Not because Python
  needs it, but because writing the type forces you to decide what the function
  actually accepts and returns. Run the type checker.
- **Never catch bare `except:`.** Catch the exception you expect. Modules B09
  and 16 explain exactly what a bare except swallows and why it will cost you an
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

By the end of the full path you should be able to do all of the following
without looking anything up:

- Write, run, debug, and finish a small program on your own, from a blank file.
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
- State the complexity of your own code, and prove it with a measurement.
- Take an open-ended design prompt, estimate its load, sketch the architecture,
  name the failure modes, and say what you would build first.
