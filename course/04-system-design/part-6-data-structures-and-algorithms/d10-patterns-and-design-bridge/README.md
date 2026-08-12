# Module D10 — Patterns, Drills, and the Bridge to System Design

**Track:** System Design, Part 6 (Data Structures and Algorithms)  |  **Time:** L3 E8  |  **Prerequisite:** Modules D01 to D09

> **Status: curriculum outline.** The full lesson, exercises, and solutions are
> written in a later build pass. This file specifies exactly what the module
> must contain, so the build can resume without re-deriving anything.

---

## Why this module

The last DSA module does two jobs. First it consolidates: the recurring problem
patterns are named and drilled until recognition becomes fast, which is what
technical interviews actually test. Second it turns outward, because every
structure in this track reappears in the system design modules at a different
scale, and making that link explicit is what stops data structures from feeling
like an academic detour.

## What you will be able to do

- Recognise which pattern a problem fits within a minute of reading it.
- Solve a timed problem under constraints, explaining your reasoning aloud.
- Choose a data structure for a system requirement, not just for a function.
- Name the structure behind a familiar piece of infrastructure.
- Assess an approximate structure by its error and memory trade.

## Concept sections

1. **The pattern catalogue** — Two pointers, sliding window, fast and slow pointers, binary search on the answer, top-k with a heap, interval merging, prefix sums, union find, and BFS on an implicit graph.
2. **Choosing a pattern** — A decision procedure from the problem statement: what is sorted, what is unique, what is ordered, what is being minimised.
3. **Communicating a solution** — State the approach, state the complexity, code it, then test it. The order that interviews and design reviews both reward.
4. **Structures behind real systems** — Hash rings for sharding, B-trees for indexes, LSM trees and skip lists for write-heavy stores, tries for autocomplete, inverted indexes for search.
5. **Probabilistic structures** — Bloom filters, HyperLogLog, count-min sketch. Trading exactness for memory, and where that is acceptable.
6. **Union find** — Disjoint sets with path compression, for connectivity, clustering, and cycle detection in undirected graphs.
7. **The bridge** — How Module D01's complexity vocabulary becomes Module 31's capacity estimation, and how D03 and D05 become Module 34's storage choices.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_recognise.md` | Twenty problems, name the pattern only, timed. |
| `ex02_drills.py` | Ten implementation drills across the catalogue with embedded tests. |
| `ex03_union_find.py` | Union find with path compression, applied to connectivity. |
| `ex04_bloom.py` | Implement a Bloom filter and measure the false positive rate against theory. |
| `ex05_design_link.md` | For six system requirements, choose the structure and defend the choice. |

## The Python angle

Every drill is written to run with plain python file.py and to state its own
complexity in a docstring, keeping the course convention that a claim is only
made when it has been measured.

## Common mistakes this module must address

- **Memorising solutions instead of patterns** — The next problem is always slightly different.
- **Coding before stating the approach** — In an interview this reads as guessing, and in a review it hides the trade.
- **Ignoring the constraints in the statement** — The input size usually tells you the intended complexity.
- **Using a probabilistic structure where exactness is required** — A Bloom filter never gives a false negative, but it does give false positives. Know which one your use case can tolerate.

## Self check questions

1. Which pattern fits: find the longest substring without repeating characters?
2. When does binary search apply to something that is not a sorted array?
3. What does union find make cheap?
4. What error does a Bloom filter allow and which does it never make?
5. Which data structure sits under a database index, and why that one?

## Going deeper

- Skiena, The Algorithm Design Manual, the catalogue half
- Designing Data-Intensive Applications, chapter 3
