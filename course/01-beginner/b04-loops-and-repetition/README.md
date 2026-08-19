# Module B04 — Repeating Work: Loops and Repetition

**Level:** Beginner  |  **Time:** L3 E6  |  **Prerequisite:** Module B03

---

## Why this module

Computers excel at doing repetitive work quickly and without fatigue. Loops are
how you instruct Python to perform a task many times. In Python, iteration is
fundamentally about looping over items directly rather than managing array
index counters. This module teaches you how to use `for` loops, `range()`,
`while` loops, the accumulator pattern, loop control statements (`break`,
`continue`), and built-in helpers (`enumerate`, `zip`).

## What you will be able to do

- Iterate over items in sequences (strings, lists, ranges) directly using `for`.
- Generate numeric sequences with `range(start, stop, step)`.
- Use `while` loops for condition-based repetition and guard against infinite loops.
- Build totals, filters, and collections using the accumulator pattern.
- Control loop flow intentionally using `break` and `continue`.
- Pair items and track indexes cleanly with `enumerate` and `zip`.
- Write and understand nested loops.

## Concept sections

1. **`for` loops iterate over items** — Looping directly over contents rather than counting indexes (`for item in items:`).
2. **Generating ranges with `range()`** — `range(stop)`, `range(start, stop)`, and `range(start, stop, step)`; why ranges are lazy.
3. **`while` loops** — Repeating until a condition changes; loop initialization, condition update, and loop termination.
4. **The accumulator pattern** — Starting with a zero/empty state and accumulating results inside the loop body.
5. **Loop control: `break` and `continue`** — Exiting early with `break`, skipping the remainder of an iteration with `continue`.
6. **Iteration helpers: `enumerate()` and `zip()`** — Getting `(index, item)` pairs without manual counters; iterating multiple sequences in lockstep.
7. **Nested loops and complexity** — Loops inside loops, matrix grids, and when nesting starts to hurt readability and performance.

## Worked example

```python
transactions = [120.50, -45.00, 300.00, -12.99, 85.20]

# Accumulator pattern: calculate total deposits and count withdrawals
total_deposits = 0.0
withdrawal_count = 0

for i, amount in enumerate(transactions, start=1):
    if amount > 0:
        total_deposits += amount
        print(f"Transaction {i}: Deposit of ${amount:.2f}")
    else:
        withdrawal_count += 1
        print(f"Transaction {i}: Withdrawal of ${abs(amount):.2f}")

print(f"\nSummary: ${total_deposits:.2f} deposited across {len(transactions)} transactions ({withdrawal_count} withdrawals).")
```

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_countdown.ipynb` | Practice `while` loops with decrementing counters and launch sequences. |
| `ex02_accumulate.ipynb` | Implement running sums, averages, and string concatenation accumulators. |
| `ex03_guessing_game.ipynb` | Build a number guessing game using `while True`, `break`, and user input. |
| `ex04_times_table.ipynb` | Generate multiplication tables with formatted nested `for` loops. |
| `ex05_enumerate.ipynb` | Refactor manual index counter loops into clean `enumerate()` calls. |
| `ex06_infinite.ipynb` | Identify, debug, and fix infinite loops and off-by-one boundary bugs. |

## Common mistakes this module must address

- **Iterating with `range(len(items))`** — In Python, write `for item in items:`, or `for i, item in enumerate(items):` if index is needed.
- **Off-by-one errors in `range()`** — `range(1, 10)` stops at 9, not 10.
- **Forgetting to update the `while` condition variable** — Creates an accidental infinite loop that freezes execution.
- **Modifying a list while iterating over it** — Modifying a list during a `for x in my_list:` causes skipped items; iterate over a copy or build a new list.
- **Overusing `while True` without clear exit criteria** — Always ensure a reachable `break` or return condition.

## Self check questions

1. What sequence of numbers does `range(2, 10, 3)` produce?
2. Why is `for item in items:` preferred over `for i in range(len(items)): items[i]`?
3. What is the difference between `break` and `continue`?
4. What does `enumerate(["a", "b", "c"], start=1)` yield on each iteration?
5. Why should you avoid appending or removing elements from a list while looping over it?

## Going deeper

- Python Documentation: Control Flow Tools (`for`, `range`, `break`, `continue`)
- Ned Batchelder: Loop Like a Native (PyCon Talk & Essay)
- Real Python: Python "for" Loops (Definite Iteration)
