# Module D03 — Hash Tables

**Track:** System Design, Part 6 (Data Structures and Algorithms)  |  **Time:** L4 E6  |  **Prerequisite:** Module D02

> **Status: curriculum outline.** The full lesson, exercises, and solutions are
> written in a later build pass. This file specifies exactly what the module
> must contain, so the build can resume without re-deriving anything.

---

## Why this module

The dictionary is the most used data structure in Python and the one whose
failure modes are least understood. This module opens it up: hashing, collision
handling, load factor, and resizing, plus the two rules that break real systems,
which are that a mutable key is a bug waiting to happen and that hash equality
and object equality must agree. It closes the loop with intermediate Module 09,
where __eq__ and __hash__ were introduced as a pair.

## What you will be able to do

- Explain how a key becomes a slot, and what happens on collision.
- Say why average lookup is constant and what makes the worst case linear.
- Implement a working hash map with open addressing and resizing.
- Design a correct __hash__ and __eq__ pair for your own type.
- Choose between a dict, a set, and a sorted structure for a given access pattern.

## Concept sections

1. **Hashing** — A hash function maps a key to an integer. What Python's hash does for the common types, and why strings are randomised per process.
2. **Collisions** — Chaining versus open addressing. What CPython actually does, including the compact layout that preserves insertion order.
3. **Load factor and resizing** — Why a dict grows before it is full, and what the resize costs.
4. **Hashability** — Immutability as the requirement. What happens when you mutate a key after insertion, demonstrated.
5. **The eq and hash contract** — Equal objects must hash equal. The bug that appears when they do not, shown with a set that contains a duplicate.
6. **Sets** — The same machinery without values. Set algebra and its complexity.
7. **Where dicts are the wrong answer** — Ordered range queries, memory pressure, and the case for a sorted list with bisect.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_hash_map.py` | Implement a hash map with open addressing, deletion, and resizing. |
| `ex02_collisions.py` | Force collisions and measure the degradation. |
| `ex03_broken_key.py` | Mutate a key after insertion and explain the resulting orphan. |
| `ex04_eq_hash.py` | Fix three types whose eq and hash disagree. |
| `ex05_bisect.py` | Replace a dict with a sorted list and bisect for range queries, and compare. |

## The Python angle

This module pairs directly with intermediate Module 09 on the data model and
advanced Module 24 on CPython internals. Use dis and sys.getsizeof to show the
dict layout, and reference the key-sharing optimisation for instance
dictionaries.

## Common mistakes this module must address

- **Using a mutable object as a key** — Only possible if it is hashable, but a hashable object that mutates is worse.
- **Defining eq without hash** — Python makes the class unhashable, which surprises people at set insertion.
- **Assuming dict order is sorted order** — It is insertion order, guaranteed since 3.7, and that is not the same thing.
- **Relying on hash values across runs** — String hashing is randomised per process by default.

## Self check questions

1. How does a key become a slot index?
2. What is the worst case lookup complexity and how do you reach it?
3. Why must equal objects hash equal?
4. What happens if you mutate an object after using it as a dict key?
5. When would a sorted structure beat a dict?

## Going deeper

- CPython source: Objects/dictobject.c header comments
- Raymond Hettinger, Modern Dictionaries, talk
