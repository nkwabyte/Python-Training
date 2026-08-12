# Module B10 — Organising Code: Modules, Packages, and Installing Things

**Level:** Beginner  |  **Time:** L3 E5  |  **Prerequisite:** Module B09

> **Status: curriculum outline.** The full lesson, exercises, and solutions are
> written in a later build pass. This file specifies exactly what the module
> must contain, so the build can resume without re-deriving anything.

---

## Why this module

This is the bridge module. Everything before it fits in one file; everything
after it does not. It teaches the learner to split code across files, to use
the standard library instead of writing what already exists, and to create a
virtual environment before installing anything. Getting the environment habit
right here is what prevents the broken-system-Python problem that derails so
many beginners.

## What you will be able to do

- Split a program across several files and import between them.
- Explain what import actually does the first time it runs.
- Use the if __name__ == '__main__' guard and say why it exists.
- Create and activate a virtual environment, and install a package into it.
- Find and use a standard library module rather than reinventing it.

## Concept sections

1. **Why one file stops working** — A concrete script that has outgrown itself, split into three files in front of the learner.
2. **import** — Importing a module, importing a name from it, and aliasing. What runs at import time.
3. **Your own modules** — A file is a module. Importing from a sibling file. The most common beginner import error and how the folder you run from causes it.
4. **The main guard** — if __name__ == '__main__'. Why importing a file should not run its script body.
5. **A tour of the standard library** — datetime, random, math, statistics, collections, pathlib, json. Enough to know what to reach for.
6. **Virtual environments** — Creating one, activating it, and what isolation buys you. Never installing into the system Python.
7. **Installing packages** — pip install inside the environment, requirements.txt, and reading a package's own documentation.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_split.py` | Split a single file program into a package with three modules. |
| `ex02_main_guard.py` | Observe what happens when a module without a guard is imported. |
| `ex03_stdlib_tour.py` | Solve five small problems using only the standard library. |
| `ex04_venv.md` | Create an environment, install one package, freeze the requirements. |
| `ex05_import_errors.md` | Diagnose four ModuleNotFoundError situations by folder layout. |

## Common mistakes this module must address

- **Installing into system Python** — Breaks other tools eventually. Establish the environment habit permanently.
- **Naming a file after a stdlib module** — A file called random.py shadows the real one. Intermediate Module 01 has a full exercise on this.
- **No main guard** — Importing the file runs the whole program unexpectedly.
- **Circular imports** — Two files importing each other. Name it, show the simplest fix, defer depth to intermediate Module 06.

## Self check questions

1. What does import mymodule actually do the first time?
2. Why does if __name__ == '__main__' exist?
3. What problem does a virtual environment solve?
4. Where should you look before writing a date parsing function yourself?
5. Why is naming your file json.py a bad idea?

## Going deeper

- The Python Tutorial, section 6: Modules
- The Python Packaging User Guide, installing packages
