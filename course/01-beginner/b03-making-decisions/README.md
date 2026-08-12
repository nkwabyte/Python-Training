# Module B03 — Making Decisions

**Level:** Beginner  |  **Time:** L3 E5  |  **Prerequisite:** Module B02

> **Status: curriculum outline.** The full lesson, exercises, and solutions are
> written in a later build pass. This file specifies exactly what the module
> must contain, so the build can resume without re-deriving anything.

---

## Why this module

Conditionals are where a program stops being a calculator and starts being
software. The syntax is small; the difficulty is entirely in thinking clearly
about conditions, and in Python's specific idea of what counts as true. This
module also introduces indentation as meaning, which is the single biggest
structural difference between Python and the C-family languages.

## What you will be able to do

- Write if, elif, and else chains that cover every case exactly once.
- Combine conditions with and, or, and not without ambiguity.
- Predict which values are truthy and which are falsy.
- Use indentation deliberately, and read an IndentationError.
- Choose between a chain of elifs and a match statement.

## Concept sections

1. **Comparison operators** — Equality versus assignment, the six comparisons, and comparing strings.
2. **if, elif, else** — The shape of a decision. Why elif is not the same as a second if. Ordering conditions from most specific to least.
3. **Indentation is syntax** — Blocks are defined by indentation. Four spaces. What the two indentation errors mean.
4. **Boolean logic** — and, or, not. Short-circuit evaluation explained with a practical example. Chained comparisons such as 0 < x < 10.
5. **Truthiness** — Empty string, empty list, zero, and None are falsy. Everything else is truthy. Why if items reads better than if len(items) > 0.
6. **Nesting and flattening** — When a nested if should become a combined condition or an early return, with a before and after example.
7. **A first look at match** — Pattern matching for multi-way choices, kept simple. Full treatment in intermediate Module 04.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_grades.py` | Map a score to a letter grade with correctly ordered conditions. |
| `ex02_truthiness.py` | Predict truthy or falsy for twenty values, then check. |
| `ex03_password_rules.py` | Validate a password against four rules with clear boolean logic. |
| `ex04_flatten.py` | Rewrite a four-level nested conditional as flat, readable code. |
| `ex05_ticket_price.py` | Price a ticket by age and day of week, covering every case. |

## Common mistakes this module must address

- **Using = instead of ==** — SyntaxError in a condition. Name the difference explicitly.
- **Writing if x == True** — Redundant and subtly wrong for non-boolean values.
- **Overlapping elif branches** — A case gets handled by the wrong branch. Teach ordering and mutual exclusivity.
- **Mixing tabs and spaces** — TabError. Configure the editor once and never think about it again.

## Self check questions

1. What is the difference between if and elif?
2. Which of '', '0', 0, [], None are falsy?
3. What does short-circuit evaluation mean and why does it matter?
4. Rewrite if len(names) > 0 idiomatically.
5. Why does Python use indentation instead of braces?

## Going deeper

- The Python Tutorial, section 4: More Control Flow Tools
- PEP 8 on indentation and line length
