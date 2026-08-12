# Module D08 — Recursion, Backtracking, and Divide and Conquer

**Track:** System Design, Part 6 (Data Structures and Algorithms)  |  **Time:** L4 E6  |  **Prerequisite:** Module D07

> **Status: curriculum outline.** The full lesson, exercises, and solutions are
> written in a later build pass. This file specifies exactly what the module
> must contain, so the build can resume without re-deriving anything.

---

## Why this module

Recursion is a way of thinking before it is a technique, and the block for most
learners is trust: believing the recursive call works before it has been
written. This module builds that trust deliberately, then converts it into the
two patterns that pay off in real work, which are divide and conquer and
backtracking. It is also honest about Python's recursion limit and the absence
of tail call optimisation.

## What you will be able to do

- Write a recursive function by stating its base case and its shrinking step.
- Trace a recursion by its call tree rather than line by line.
- Convert a recursive solution to an iterative one with an explicit stack.
- Solve constraint problems with backtracking and prune the search.
- Say when recursion is the wrong tool in Python, and why.

## Concept sections

1. **The recursive contract** — Base case, progress toward it, and trusting the smaller call. The three questions to ask before writing a line.
2. **The call stack** — Frames, depth, and what RecursionError means. sys.setrecursionlimit and why raising it is usually the wrong fix.
3. **Divide and conquer** — Split, solve, combine. Merge sort revisited, binary search revisited, and a matrix example.
4. **Recursion on trees and graphs** — Where recursion is genuinely the clearest form, connecting to Modules D05 and D06.
5. **Backtracking** — Choose, explore, un-choose. N queens, sudoku, permutations, and subsets, with pruning as the difference between feasible and not.
6. **Converting to iteration** — An explicit stack, and why Python has no tail call optimisation.
7. **Memoisation preview** — The overlapping subproblem that makes naive recursion exponential, setting up Module D09.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_basics.py` | Six recursive functions with base cases stated first. |
| `ex02_call_tree.md` | Draw the call tree for three recursions and count the calls. |
| `ex03_backtracking.py` | N queens and subset sum with and without pruning. |
| `ex04_to_iterative.py` | Convert three recursive functions to explicit stack versions. |
| `ex05_depth_limit.py` | Hit the recursion limit deliberately and choose the right fix. |

## The Python angle

Connect to advanced Module 14: a generator based recursive traversal with yield
from is often the most readable form in Python, and it composes with the lazy
pipelines built there.

## Common mistakes this module must address

- **No base case, or an unreachable one** — Infinite recursion and a wall of traceback.
- **Recomputing the same subproblem** — Exponential time from a linear looking function. Module D09 fixes it.
- **Raising the recursion limit to fix a design problem** — A segfault instead of an exception.
- **Mutating shared state without undoing it** — The classic backtracking bug. Un-choose is not optional.

## Self check questions

1. What three things must every recursive function have?
2. Why does Python raise RecursionError rather than growing the stack?
3. What does the un-choose step in backtracking restore?
4. When is an explicit stack better than recursion?
5. How does pruning change the cost of a backtracking search?

## Going deeper

- The Python Tutorial on generators, plus yield from
- Skiena, chapter 9 on combinatorial search
