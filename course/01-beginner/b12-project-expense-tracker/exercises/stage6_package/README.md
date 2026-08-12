# B12 Milestone Project: Expense Tracker CLI
## Project exercise: stage6_package/

**The task**

Split into modules with a main guard and a project README.

---

## How to work in here

This exercise is a small project rather than a single file, because the point is
the structure as much as the behaviour. Build it in stages and run it after every
one; a project that has never run is not partly finished, it is unstarted.

Suggested starting layout, to change once you know better:

```
stage6_package/
├── README.md          what this does and how to run it
├── main.py            the entry point, with a __main__ guard
├── <module>.py        one file per responsibility, named for what it does
└── tests/             at least one test per behaviour you care about
```

---

## Before you call it done

- [ ] It runs from a clean checkout with documented steps.
- [ ] Every file has one responsibility you can name in a sentence.
- [ ] Bad input produces a useful message, not a traceback.
- [ ] Someone else could run it from this README alone.
