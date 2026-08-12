# Module D09 — Dynamic Programming and Greedy Algorithms

**Track:** System Design, Part 6 (Data Structures and Algorithms)  |  **Time:** L5 E7  |  **Prerequisite:** Module D08

> **Status: curriculum outline.** The full lesson, exercises, and solutions are
> written in a later build pass. This file specifies exactly what the module
> must contain, so the build can resume without re-deriving anything.

---

## Why this module

Dynamic programming has a reputation for difficulty that comes almost entirely
from being taught as a catalogue of solved problems. Taught as a procedure, it
is mechanical: find the state, find the recurrence, decide the order, then
optimise the space. Greedy sits next to it as the tempting alternative that is
right less often than it looks, and knowing how to tell them apart is the real
skill.

## What you will be able to do

- Identify optimal substructure and overlapping subproblems in a new problem.
- Turn a recurrence into memoised recursion and then into a bottom up table.
- Reduce the space of a DP solution when only the last row is needed.
- Recognise when a greedy choice is provably safe and when it is not.
- Reconstruct the solution, not just its cost.

## Concept sections

1. **The two conditions** — Optimal substructure and overlapping subproblems, tested on problems that have them and problems that do not.
2. **Memoisation** — Top down with a cache. functools.cache doing the work in one line, and what it costs in memory.
3. **Bottom up** — Tables, the order of filling, and why it removes the recursion depth problem.
4. **The classic set** — Fibonacci, climbing stairs, coin change, knapsack, longest common subsequence, and edit distance, each reduced to state and recurrence.
5. **Space optimisation** — Rolling arrays when the recurrence only looks back one or two rows.
6. **Reconstructing the answer** — Parent pointers and back-tracing the table to produce the actual solution.
7. **Greedy** — The exchange argument. Interval scheduling and Huffman coding as safe cases, coin change as the trap. Proving or disproving a greedy choice.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_memoise.py` | Take exponential recursion to linear with a cache and measure it. |
| `ex02_tabulate.py` | Convert three memoised solutions to bottom up tables. |
| `ex03_knapsack.py` | 0/1 knapsack with reconstruction of the chosen items. |
| `ex04_edit_distance.py` | Edit distance with the operation sequence, not just the cost. |
| `ex05_greedy_or_not.md` | Decide greedy or DP for eight problems and justify each. |

## The Python angle

functools.cache from advanced Module 15 makes the memoisation step trivial,
which is exactly why the module makes the learner write the cache by hand once
before allowing the decorator.

## Common mistakes this module must address

- **Jumping to code before defining the state** — Almost every failed DP attempt starts here.
- **Caching on mutable arguments** — Unhashable, or worse, subtly wrong.
- **Assuming greedy works because it worked on the examples** — Coin change with an unusual denomination set is the standard disproof.
- **Filling the table in the wrong order** — Reading a cell that has not been computed yet.

## Self check questions

1. What two properties must a problem have for DP to apply?
2. What is the difference between memoisation and tabulation?
3. How do you recover the chosen items, not just the optimal value?
4. When can a greedy algorithm be proved correct?
5. Why can a DP table often be reduced to two rows?

## Going deeper

- Erik Demaine, MIT 6.006 dynamic programming lectures
- CLRS, chapters 15 and 16
