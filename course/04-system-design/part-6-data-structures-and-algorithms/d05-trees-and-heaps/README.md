# Module D05 — Trees and Heaps

**Track:** System Design, Part 6 (Data Structures and Algorithms)  |  **Time:** L4 E6  |  **Prerequisite:** Module D04

> **Status: curriculum outline.** The full lesson, exercises, and solutions are
> written in a later build pass. This file specifies exactly what the module
> must contain, so the build can resume without re-deriving anything.

---

## Why this module

Trees are where hierarchy, ordering, and logarithmic thinking meet. This module
covers the tree shapes that actually appear in engineering work: the binary
search tree as an idea, the heap as a working tool you will reach for, and the
B-tree as the reason a database index behaves the way it does. That last link
is what makes this module a system design prerequisite rather than an interview
exercise.

## What you will be able to do

- Implement a binary search tree with insert, search, and delete.
- Perform all four traversals and say which one each problem needs.
- Explain why balance matters and what a self balancing tree guarantees.
- Use heapq for priority queues, top-k, and merging sorted streams.
- Connect B-tree structure to database index behaviour and disk pages.

## Concept sections

1. **Tree vocabulary** — Root, leaf, depth, height, and the recursive definition that makes tree code short.
2. **Binary search trees** — The ordering invariant. Insert, search, and the three delete cases. Why a sorted insertion sequence degrades it to a linked list.
3. **Traversals** — In order, pre order, post order, and level order, each with the kind of problem it solves.
4. **Balance** — What an unbalanced tree costs. AVL and red-black at the level of guarantees rather than rotations.
5. **Heaps** — The complete binary tree in an array, the heap property, sift up and sift down, and heapify in linear time.
6. **heapq in practice** — Priority queues, nlargest and nsmallest, merging sorted iterables, and the min-heap-only workaround for max behaviour.
7. **Trees on disk** — B-trees and B+ trees, page size, fan out, and why a database index is shallow and wide. The bridge to Module 34.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_bst.py` | Implement a BST including the three delete cases. |
| `ex02_traversals.py` | All four traversals, iterative and recursive. |
| `ex03_validate.py` | Check the BST invariant and find where a tree violates it. |
| `ex04_heapq.py` | Top-k over a stream too large to sort, plus a k-way merge. |
| `ex05_scheduler.py` | A priority based task scheduler with tie breaking. |

## The Python angle

Python ships no balanced tree in the standard library, which is itself a lesson:
show the sortedcontainers package, bisect on a sorted list, and heapq, then
discuss the trade that made the standard library choose those instead.

## Common mistakes this module must address

- **Assuming a BST is balanced** — Sorted input builds a linked list with extra steps.
- **Recursive traversal on a deep tree** — RecursionError. Show the iterative form and Python's recursion limit.
- **Trying to use heapq as a max-heap** — Negate the key or wrap it, and know why.
- **Confusing a heap with a sorted structure** — A heap only promises the smallest element at the root.

## Self check questions

1. What invariant defines a binary search tree?
2. Which traversal produces sorted output, and why?
3. What does heapify cost, and why is it not n log n?
4. Why are database index trees wide rather than deep?
5. What does heapq guarantee about the second smallest element?

## Going deeper

- The heapq module documentation, including the theory section
- Use The Index, Luke, on B-tree indexes
