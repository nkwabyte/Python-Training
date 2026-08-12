# Module D07 — Sorting and Searching

**Track:** System Design, Part 6 (Data Structures and Algorithms)  |  **Time:** L4 E5  |  **Prerequisite:** Module D06

> **Status: curriculum outline.** The full lesson, exercises, and solutions are
> written in a later build pass. This file specifies exactly what the module
> must contain, so the build can resume without re-deriving anything.

---

## Why this module

You will almost never write a sort. You will constantly make decisions that
depend on understanding one: what stability means for a multi-key sort, why
sorting a stream is impossible, what an index really is, and why sorted data
unlocks binary search. This module treats sorting as a lens on algorithm design
rather than as a set of implementations to memorise.

## What you will be able to do

- Explain what Timsort does and why Python chose it.
- Say what stability means and produce a correct multi-key sort.
- Implement merge sort and quicksort and account for their behaviour.
- Use bisect for search and for insertion into a sorted list.
- Sort data that does not fit in memory, in outline.

## Concept sections

1. **Sorting as a design lens** — Comparison based lower bound of n log n, and what non-comparison sorts do to escape it.
2. **The classics** — Merge sort, quicksort, and heap sort. Divide and conquer, pivot choice, in place versus stable, worst cases.
3. **Timsort** — Runs, galloping, and why real data is partly ordered. What Python actually runs when you call sorted.
4. **Sorting in Python** — key functions, reverse, stability, sorting by multiple fields, and operator.itemgetter. Cross reference to intermediate Module 05.
5. **Binary search** — The invariant, the off-by-one traps, and bisect_left versus bisect_right with a concrete difference.
6. **Non-comparison sorts** — Counting and radix, and the narrow conditions under which they are worth it.
7. **External and distributed sorting** — Chunk, sort, merge. heapq.merge. Where this reappears as a map-reduce shuffle in Module 34.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_implement.py` | Merge sort and quicksort with instrumented comparison counts. |
| `ex02_stability.py` | A multi-key sort that is correct only because the sort is stable. |
| `ex03_bisect.py` | Insertion points, range queries, and a leaderboard. |
| `ex04_binary_search.py` | Write binary search correctly, then break it four ways deliberately. |
| `ex05_external_sort.py` | Sort a file larger than the memory you allow yourself. |

## The Python angle

The key function is the practical heart: it computes once per element, unlike a
comparator. Benchmark sorted with a key against a cmp_to_key version to show the
difference, tying back to advanced Module 23 on measurement.

## Common mistakes this module must address

- **Assuming sort returns a value** — list.sort returns None. sorted returns the new list.
- **Sorting inside a loop** — Quadratic or worse. Sort once, then use bisect.
- **Getting binary search bounds wrong** — The classic infinite loop. Practise the invariant.
- **Ignoring stability when it matters** — A second sort quietly destroys the first ordering if the sort is unstable.

## Self check questions

1. What does it mean for a sort to be stable, and when do you need it?
2. Why does Python use Timsort rather than quicksort?
3. What is the difference between bisect_left and bisect_right?
4. How do you sort by one field ascending and another descending?
5. How would you sort a file that does not fit in memory?

## Going deeper

- The listsort.txt design note in the CPython source
- The bisect module documentation
