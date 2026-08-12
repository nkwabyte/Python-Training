# Progress Log

Two jobs: track where you are, and record what surprised you.

The second one matters more. A mistakes log is a map of your own blind spots,
and after three months it will be the most useful file in this repository.

---

## Module tracker

Mark each cell when done. "Quiz" means you answered every self-check question in
one or two sentences without looking.

### Level 01 — Beginner

| # | Module | Read | Exercises | Project | Quiz | Date |
|---|---|---|---|---|---|---|
| B01 | First Program and the Interpreter | | | | | |
| B02 | Data, Names, and Types | | | | | |
| B03 | Making Decisions | | | | | |
| B04 | Loops and Repetition | | | | | |
| B05 | Collections | | | | | |
| B06 | Functions | | | | | |
| B07 | Working with Text | | | | | |
| B08 | Files and Folders | | | | | |
| B09 | Errors and Debugging | | | | | |
| B10 | Organising Code | | | | | |
| B11 | A First Look at Classes | | | | | |
| B12 | **Project: Expense Tracker CLI** | | | | | |

## Level 02 — Intermediate

### Part 1 — Foundations

| # | Module | Read | Visuals | Exercises | Quiz | Date |
|---|---|---|---|---|---|---|
| 01 | Runtime and Toolchain | | | | | |
| 02 | Objects, Names, Data Model | | | | | |
| 03 | Core Types | | | | | |
| 04 | Control Flow and Functions | | | | | |
| 05 | Collections and Comprehensions | | | | | |
| 06 | Modules, Packages, Projects | | | | | |
| 07 | **Project: Inventory CLI** | | | | | |

### Part 2 — Object-Oriented Python

| # | Module | Read | Visuals | Exercises | Quiz | Date |
|---|---|---|---|---|---|---|
| 08 | Classes and Encapsulation | | | | | |
| 09 | Dunder Methods | | | | | |
| 10 | Inheritance, Composition, MRO | | | | | |
| 11 | Dataclasses and Value Semantics | | | | | |
| 12 | Design Principles | | | | | |
| 13 | **Project: Plugin Pipeline** | | | | | |

## Level 03 — Advanced

### Part 3 — Idiomatic and Advanced

| # | Module | Read | Visuals | Exercises | Quiz | Date |
|---|---|---|---|---|---|---|
| 14 | Iterators and Generators | | | | | |
| 15 | Decorators and functools | | | | | |
| 16 | Error Handling | | | | | |
| 17 | Typing | | | | | |
| 18 | Testing and Quality | | | | | |
| 19 | Stdlib, Files, Serialization | | | | | |
| 20 | **Project: Library and CLI** | | | | | |

### Part 4 — Concurrency and Internals

| # | Module | Read | Visuals | Exercises | Quiz | Date |
|---|---|---|---|---|---|---|
| 21 | GIL, Threads, Processes | | | | | |
| 22 | Asyncio | | | | | |
| 23 | Performance and Profiling | | | | | |
| 24 | CPython Internals | | | | | |

### Part 5 — Applied Python

| # | Module | Read | Visuals | Exercises | Quiz | Date |
|---|---|---|---|---|---|---|
| 25 | Automation and the OS | | | | | |
| 26 | HTTP and Scraping | | | | | |
| 27 | Databases | | | | | |
| 28 | FastAPI | | | | | |
| 29 | Data and ML Foundations | | | | | |
| 30 | Packaging and Deployment | | | | | |

## Level 04 — System Design

### Part 6 — Data Structures and Algorithms

| # | Module | Read | Exercises | Drills | Quiz | Date |
|---|---|---|---|---|---|---|
| D01 | Complexity and Measurement | | | | | |
| D02 | Arrays and Dynamic Arrays | | | | | |
| D03 | Hash Tables | | | | | |
| D04 | Linked Structures | | | | | |
| D05 | Trees and Heaps | | | | | |
| D06 | Graphs | | | | | |
| D07 | Sorting and Searching | | | | | |
| D08 | Recursion and Divide and Conquer | | | | | |
| D09 | Dynamic Programming and Greedy | | | | | |
| D10 | Patterns and the Design Bridge | | | | | |

### Part 7 — System Design

| # | Module | Read | Visuals | Exercises | Quiz | Date |
|---|---|---|---|---|---|---|
| 31 | Design Fundamentals | | | | | |
| 32 | Service Architecture | | | | | |
| 33 | Caching, Queues, Jobs | | | | | |
| 34 | Data at Scale | | | | | |
| 35 | Reliability and Security | | | | | |
| 36 | **Capstone** | | | | | |

---

## Checkpoint gates

| Gate | Requirement | Passed |
|---|---|---|
| End of Level 01 | A program of your own that reads input, stores it in a file, survives a restart, validates everything, and prints a report | |
| End of Part 1 | Multi-module CLI, runs with `python -m`, validates input, meaningful exit codes | |
| End of Part 2 | A class supporting `==`, `hash()`, ordering, iteration, `len()`, `in`, `with`, good `repr`, every dunder justified | |
| End of Part 3 | Typed, tested, packaged library. mypy clean, 90 percent coverage | |
| End of Part 4 | Profiled a slow program, fixed it, proved the fix with a benchmark | |
| End of Part 5 | FastAPI service with DB, migrations, tests, Dockerfile, CI + a reproducible analysis notebook | |
| End of Part 6 | For a given system requirement, choose the data structure, state its complexity, and defend the choice | |
| End of Part 7 | Design doc with load target, storage justification, three failure modes, and your own load-test numbers | |

---

## Mistakes log

One line per surprise. Date, what you expected, what happened, what you now
know. Do not curate it. The embarrassing entries are the valuable ones.

| Date | Module | What surprised me | What I now understand |
|---|---|---|---|
| | | | |

<!--
Example entries, delete these once you have your own:

| 2026-08-04 | 02 | Appending to one list changed another one | They were two names bound to the SAME list object. `is` and `id()` prove it; `=` never copies. |
| 2026-08-06 | 04 | A default argument kept its value between calls | Defaults are evaluated once, at def time, not per call. Use `None` as the sentinel. |
| 2026-08-11 | 09 | Adding `__eq__` made my object unusable as a dict key | Defining `__eq__` sets `__hash__` to None. Define both, or use `frozen=True`. |
-->

---

## Open questions

Things you did not understand and moved past anyway. Revisit these; a question
that stays open for two weeks is usually a gap that will bite you.

| Date raised | Question | Resolved on | Answer |
|---|---|---|---|
| | | | |

---

## Time log (optional but recommended)

Tracking actual hours against the curriculum's estimates tells you whether you
are moving too fast to retain anything.

| Week | Planned modules | Actual hours | Notes |
|---|---|---|---|
| 1 | B01, B02 (or 01, 02 if starting at Intermediate) | | |
