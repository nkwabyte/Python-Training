# Module B12 — Milestone Project: Expense Tracker CLI

**Level:** Beginner  |  **Time:** P10  |  **Prerequisite:** Modules B01 to B11

> **Status: curriculum outline.** The full lesson, exercises, and solutions are
> written in a later build pass. This file specifies exactly what the module
> must contain, so the build can resume without re-deriving anything.

---

## Why this module

Everything in the beginner track fuses here into one program that a learner can
show someone. It is deliberately unglamorous and completely real: input,
validation, storage, reporting, and a command line interface. Finishing it is
the honest test of whether the beginner track worked, and it is also the exact
level of program that intermediate Module 07 then rebuilds with proper
structure, so the learner can feel the difference the intermediate track makes.

## What you will be able to do

- Design a small program before writing it, as data plus operations.
- Persist data between runs and survive a corrupted or missing file.
- Validate every piece of user input and give a useful message when it is wrong.
- Produce a formatted summary report from stored records.
- Organise the finished program across several modules with a main guard.

## Concept sections

1. **The brief** — Add, list, filter, and summarise expenses. Categories, dates, and amounts. Written as a specification the learner must read carefully.
2. **Designing before coding** — What is the data, what are the operations, what can go wrong. One page on paper before any typing.
3. **Building it in stages** — Six checkpoints, each a working program: store in memory, then save, then load, then validate, then report, then split into modules.
4. **The command interface** — A simple menu loop first, then an argparse version, so the learner sees why argparse exists.
5. **Storage** — JSON file, atomic write, and recovery when the file is missing or damaged.
6. **Reporting** — Totals by category and by month, printed as an aligned table.
7. **Finishing touches** — A README for the project, a requirements file, and a manual test checklist.

## Exercises to build

| File | What it drills |
|---|---|
| `stage1_memory.py` | In-memory add and list. |
| `stage2_persist.py` | Save and load to JSON. |
| `stage3_validate.py` | Reject bad amounts, dates, and categories with clear messages. |
| `stage4_report.py` | Totals by category and month. |
| `stage5_cli.py` | Replace the menu loop with argparse subcommands. |
| `stage6_package/` | Split into modules with a main guard and a project README. |

## Common mistakes this module must address

- **Writing all six stages before running anything** — Run after every stage. This is the habit the project exists to build.
- **Trusting input** — Every value from a user is a string and may be nonsense.
- **Losing the data file on a crash** — Write to a temporary file and replace, as taught in Module B08.
- **One 300 line file** — Stage six exists precisely to fix this.

## Self check questions

1. What is the data model of your tracker, in one sentence?
2. What happens on the very first run when no data file exists?
3. How does your program behave if the JSON file is corrupt?
4. Which parts of your code would break if you added a new field?
5. What would you do differently if the file grew to a million records?

## Going deeper

- The argparse tutorial in the standard library documentation
- Intermediate Module 07, which rebuilds this program with production structure
