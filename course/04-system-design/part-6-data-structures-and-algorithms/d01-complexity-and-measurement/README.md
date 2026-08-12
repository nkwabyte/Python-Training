# Module D01 — Complexity and Measuring Cost

**Track:** System Design, Part 6 (Data Structures and Algorithms)  |  **Time:** L4 E5  |  **Prerequisite:** Advanced Module 23 (Performance and Profiling) is helpful but not required

> **Status: curriculum outline.** The full lesson, exercises, and solutions are
> written in a later build pass. This file specifies exactly what the module
> must contain, so the build can resume without re-deriving anything.

---

## Why this module

Big O is usually taught as a notation to memorise, which is why so many
engineers can recite it and still cannot use it. This module teaches it as a
decision tool: a way to predict which of two designs survives a hundredfold
growth, and a vocabulary for defending that prediction in a design review. It
pairs every complexity claim with a measurement, because in Python the constant
factors are large enough that theory alone will mislead you.

## What you will be able to do

- State the time and space complexity of code you have written, and justify it.
- Distinguish worst, average, and amortised cost, and say which one matters when.
- Predict how a workload scales, then confirm the prediction with a benchmark.
- Recognise when a lower complexity is the wrong choice at your actual input size.
- Read a complexity table for Python's built-in operations and use it.

## Concept sections

1. **Counting operations** — Growth as a function of input size. Why constants and lower order terms are dropped, and what that hides.
2. **The common classes** — Constant, logarithmic, linear, linearithmic, quadratic, exponential, with a real code example of each from earlier modules.
3. **Worst, average, and amortised** — Why list.append is constant time on average despite occasional resizing, and why a hash lookup is not always constant.
4. **Space complexity** — Auxiliary space versus total. The time and memory trade, made concrete with a memoisation example.
5. **Measuring instead of assuming** — timeit properly, scaling the input by ten, and plotting the curve. Confirming or refuting a complexity claim with evidence.
6. **When the theory misleads** — Cache behaviour, interpreter overhead, and small n. A quadratic algorithm on a hundred items beats a clever one you got wrong.
7. **Talking about cost in a design review** — Turning a complexity claim into a capacity statement: requests per second, memory per user, growth headroom.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_classify.py` | Assign complexity to fifteen functions and defend each answer. |
| `ex02_measure.py` | Benchmark four functions across growing inputs and identify the curve. |
| `ex03_amortised.py` | Demonstrate list growth and reproduce the amortised constant result. |
| `ex04_space_time.py` | Trade memory for speed with memoisation and measure both. |
| `ex05_small_n.py` | Find the input size where a quadratic version stops winning. |

## The Python angle

Python's built-in complexity table is the practical core of this module: list
indexing and append, list insert and delete at the front, dict and set lookup,
in on a list versus a set, and deque at both ends. Every later DSA module
refers back to this table, and intermediate Module 05 already introduced the
containers themselves.

## Common mistakes this module must address

- **Treating Big O as a score** — O(n log n) is not automatically better than O(n squared) at your input size.
- **Ignoring the constant in Python** — A pure Python O(n) loop can lose to an O(n log n) call into C.
- **Timing once** — Noise, warm caches, and the garbage collector. Use timeit and repeat.
- **Forgetting the space side** — An algorithm that is fast because it copies the whole input is a memory decision too.

## Self check questions

1. What is the complexity of x in items for a list and for a set?
2. Why is list.append amortised constant rather than constant?
3. When is an O(n squared) algorithm the correct choice?
4. What does dropping constants hide, and when does that matter?
5. How would you prove a function is linear rather than quadratic?

## Going deeper

- The Python wiki TimeComplexity page
- Skiena, The Algorithm Design Manual, chapter 2
