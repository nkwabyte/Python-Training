# Module B05 — Collections: Lists, Dictionaries, Sets, and Tuples

**Level:** Beginner  |  **Time:** L4 E6  |  **Prerequisite:** Module B04

> **Status: curriculum outline.** The full lesson, exercises, and solutions are
> written in a later build pass. This file specifies exactly what the module
> must contain, so the build can resume without re-deriving anything.

---

## Why this module

Choosing the right container is the highest-leverage decision a beginner makes,
and the one they are least often taught to make consciously. This module gives
each of the four core containers a job description, so that by the end the
learner picks a dict because the data is a lookup, not because a dict is the
one they remember. It stays practical; the performance reasoning lives in
intermediate Module 05 and DSA Modules D02 and D03.

## What you will be able to do

- Choose between list, dict, set, and tuple by the shape of the problem.
- Add, read, update, and remove items in each container.
- Loop over a dictionary's keys, values, and items.
- Use a set to remove duplicates and test membership.
- Nest containers to model simple real data, such as a list of records.

## Concept sections

1. **Lists** — Ordered, changeable, allows duplicates. Indexing, negative indexing, slicing, append, insert, remove, pop, sort, and reverse.
2. **Dictionaries** — Key to value lookup. Adding and updating, get with a default, keys, values, items, and the KeyError you will meet.
3. **Sets** — Unique membership. Fast in tests, union, intersection, difference, and the classic deduplication one-liner.
4. **Tuples** — Fixed groups of related values. Unpacking, returning several values, and why immutability is sometimes exactly what you want.
5. **Choosing a container** — A decision table: ordered, unique, keyed, fixed. Work through five realistic problems out loud.
6. **Nesting** — A list of dicts as the standard shape of records. Reaching into nested data and printing it readably.
7. **Copying** — Assigning a list does not copy it. A gentle first encounter with aliasing, with a pointer to intermediate Module 02.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_shopping_list.py` | Full list lifecycle: build, edit, sort, report. |
| `ex02_phonebook.py` | Dictionary CRUD with safe lookups using get. |
| `ex03_dedupe.py` | Remove duplicates three ways and compare the results. |
| `ex04_records.py` | Filter and summarise a list of dictionaries. |
| `ex05_choose.md` | Pick the right container for twelve scenarios and justify each. |
| `ex06_aliasing.py` | Observe a shared list being changed through two names. |

## Common mistakes this module must address

- **Using a list where a dict belongs** — Repeated linear searching for a matching field. Show the rewrite.
- **Assuming dict lookup failure returns None** — It raises KeyError. Teach get and the in test.
- **Copying with b = a** — Both names see the same list. Show list(a) and copy.
- **Expecting sets to keep order** — They do not. Say so plainly and early.

## Self check questions

1. Which container would you use for unique tags on a post?
2. What does items() give you when looping a dict?
3. How do you safely read a key that may be missing?
4. When is a tuple a better choice than a list?
5. What does b = a do when a is a list?

## Going deeper

- The Python Tutorial, section 5: Data Structures
- The standard library reference on built-in types
