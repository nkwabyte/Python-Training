# Module D02 — Arrays and Dynamic Arrays

**Track:** System Design, Part 6 (Data Structures and Algorithms)  |  **Time:** L3 E5  |  **Prerequisite:** Module D01

> **Status: curriculum outline.** The full lesson, exercises, and solutions are
> written in a later build pass. This file specifies exactly what the module
> must contain, so the build can resume without re-deriving anything.

---

## Why this module

The Python list is the container most code reaches for, and almost nobody knows
what it is: a dynamic array of pointers, with a growth policy and a very
expensive front end. Knowing the layout explains a whole family of performance
surprises, and it is the foundation for every technique in Module D10, since
two pointers and sliding windows are array techniques.

## What you will be able to do

- Describe what a Python list is in memory and why insert at the front is linear.
- Choose between list, deque, array, and a NumPy array with reasons.
- Implement a dynamic array with doubling growth and measure its amortised cost.
- Apply the two pointer and sliding window patterns to array problems.
- Explain why slicing copies and what that costs in a loop.

## Concept sections

1. **Contiguous memory** — What an array is at the hardware level, and why indexing is constant time.
2. **The Python list** — An array of pointers to objects, not the objects themselves. What that means for memory and for cache behaviour.
3. **Growth policy** — Over-allocation, the doubling idea, and why appending is cheap on average and occasionally expensive.
4. **The front end problem** — insert(0, x) and pop(0) are linear. collections.deque and when to reach for it.
5. **Slicing copies** — A slice is a new list. The cost of slicing inside a loop, measured.
6. **array and NumPy** — Homogeneous, unboxed storage. When leaving the list behind is worth it, with a memory comparison.
7. **Array techniques** — Two pointers, sliding window, prefix sums, and in-place partitioning, each with one worked problem.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_dynamic_array.py` | Implement a growable array on fixed blocks and count reallocations. |
| `ex02_front_vs_back.py` | Benchmark list versus deque for queue-shaped workloads. |
| `ex03_two_pointers.py` | Solve four classic problems with the two pointer pattern. |
| `ex04_sliding_window.py` | Fixed and variable window problems, including the longest substring case. |
| `ex05_prefix_sums.py` | Answer many range-sum queries after one linear pass. |

## The Python angle

Anchor everything to the containers from intermediate Module 05, and use
sys.getsizeof and the memory tooling from advanced Module 23 to show the
pointer overhead of a list of small integers versus an equivalent NumPy array.

## Common mistakes this module must address

- **Using a list as a queue** — pop(0) turns a linear job into a quadratic one. The most common of all.
- **Slicing in a loop** — Quietly quadratic. Show the profile.
- **Assuming a list of ints is compact** — Each element is a pointer to a boxed object.
- **Reaching for NumPy too early** — For a thousand items the conversion cost dominates.

## Self check questions

1. Why is indexing a list constant time?
2. What is the cost of inserting at position zero, and why?
3. When does append become expensive, and how often?
4. What does a slice cost in time and memory?
5. When is deque the right answer over list?

## Going deeper

- CPython source: Objects/listobject.c, the list_resize function
- The collections and array module documentation
