# Module B04 — Repeating Work: Loops

**Level:** Beginner  |  **Time:** L3 E6  |  **Prerequisite:** Module B03

> **Status: curriculum outline.** The full lesson, exercises, and solutions are
> written in a later build pass. This file specifies exactly what the module
> must contain, so the build can resume without re-deriving anything.

---

## Why this module

Loops are where beginners either learn to think in terms of collections or
learn to fight the language for years. Python's for loop iterates over items,
not indexes, and internalising that early makes every later topic easier, from
comprehensions to generators. This module also covers the accumulator pattern,
which is the shape of most real programs a beginner will write.

## What you will be able to do

- Loop over items directly rather than over index numbers.
- Use range correctly, including its exclusive end.
- Choose between for and while by asking whether the count is known.
- Build up a result with the accumulator pattern.
- Use break, continue, and enumerate deliberately.

## Concept sections

1. **for loops over items** — Iterating a string, a list, and a range. Why for item in items beats indexing.
2. **range** — Start, stop, step. The exclusive end and the off-by-one errors it prevents.
3. **while loops** — Looping until a condition changes. The three parts of a correct while loop, and how to avoid an infinite one.
4. **The accumulator pattern** — Start with an empty total or list, add to it in the loop, use it after. The single most reusable shape in beginner code.
5. **break and continue** — Leaving early and skipping an item. When an early break is clearer than a compound condition.
6. **enumerate and zip** — Getting an index when you truly need one, and walking two sequences together.
7. **Nested loops** — Grids and tables, with an honest note that two nested loops over the same data is a cost you should notice.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_countdown.py` | Practise range boundaries with three countdown variants. |
| `ex02_accumulate.py` | Sum, count, and collect from a list of readings. |
| `ex03_guessing_game.py` | A while loop with input validation and a retry limit. |
| `ex04_times_table.py` | Nested loops producing a formatted grid. |
| `ex05_enumerate.py` | Rewrite four index-based loops using enumerate and zip. |
| `ex06_infinite.py` | Diagnose and fix three loops that never terminate. |

## Common mistakes this module must address

- **Looping over range(len(items))** — Works, but hides the intent. Show the direct form side by side.
- **Forgetting to change the while condition** — Infinite loop. Teach ctrl-c and the three-part checklist.
- **Modifying a list while looping over it** — Items get skipped. Show the surprising output, then the fix.
- **Rebuilding the accumulator inside the loop** — The total resets every pass. A classic indentation bug.

## Self check questions

1. How many numbers does range(1, 10, 2) produce?
2. When is while the right choice over for?
3. What does enumerate give you on each pass?
4. Why is modifying a list while iterating it dangerous?
5. Describe the accumulator pattern in one sentence.

## Going deeper

- The Python Tutorial, section 4.2 and 4.3
- Ned Batchelder, Loop Like A Native, talk
