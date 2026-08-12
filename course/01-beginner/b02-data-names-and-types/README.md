# Module B02 — Data, Names, and Types

**Level:** Beginner  |  **Time:** L3 E5  |  **Prerequisite:** Module B01

> **Status: curriculum outline.** The full lesson, exercises, and solutions are
> written in a later build pass. This file specifies exactly what the module
> must contain, so the build can resume without re-deriving anything.

---

## Why this module

Beginners are usually taught that a variable is a box you put a value into.
That model is wrong in Python and it causes confusion later, in Module 02 of
the intermediate track, where names and objects are treated rigorously. This
module teaches the correct idea gently from the very first day: a name is a
label attached to a value. It also covers the four types that ninety percent of
beginner code uses, and how to move between them safely.

## What you will be able to do

- Create names and rebind them, and predict what a name refers to after each line.
- Use int, float, str, and bool correctly and say what each is for.
- Convert between types on purpose and explain why int('3.5') fails.
- Take input from a user and remember that input always gives you text.
- Build readable output with f-strings.

## Concept sections

1. **Names are labels, not boxes** — Assignment attaches a label to a value. Reassignment moves the label. A first, gentle look at the idea the intermediate track makes precise.
2. **Numbers** — int and float. Arithmetic operators, integer division, modulo, exponent. One honest warning about 0.1 plus 0.2 without going into IEEE 754 yet.
3. **Text** — Strings, quotes, escapes, concatenation, and repetition. Length with len.
4. **True, False, and None** — Booleans as the answers to yes or no questions. None as the absence of a value, not as zero.
5. **Type conversion** — int, float, str, bool as functions. Which conversions work, which raise, and why input always returns a string.
6. **f-strings** — Embedding values in text, formatting numbers to two decimal places, and why f-strings beat concatenation.
7. **Naming things well** — snake_case, names that say what they hold, and the reserved words you cannot use.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_labels.py` | Trace a sequence of assignments and predict each value before running. |
| `ex02_calculator.py` | Read two numbers from input and print sum, difference, product, quotient. |
| `ex03_conversions.py` | Fix a broken script that treats input as a number. |
| `ex04_receipt.py` | Format a small receipt with aligned columns and two decimal places. |
| `ex05_naming.md` | Rename fifteen badly named variables and justify each choice. |

## Common mistakes this module must address

- **Adding a string to a number** — TypeError. The fix is a deliberate conversion, not a guess.
- **Assuming input returns a number** — '5' plus '5' becomes '55'. This surprises every beginner exactly once.
- **Using a builtin as a name** — Naming something list or str breaks later lines mysteriously.
- **Expecting exact decimal arithmetic** — 0.1 plus 0.2 is not 0.3. Acknowledge it now, explain it fully in intermediate Module 03.

## Self check questions

1. What does a name refer to after x = 5 then y = x then x = 6?
2. Why does input always need converting before arithmetic?
3. What is the difference between None, 0, and False?
4. When would you choose float over int?
5. Write an f-string that prints a price to two decimal places.

## Going deeper

- The Python Tutorial, section 3: An Informal Introduction to Python
- PEP 8 naming conventions
- The format specification mini-language, skim only
