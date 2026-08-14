# Module B02 — Data, Names, and Types

**Level:** Beginner  |  **Time:** L3 E5  |  **Prerequisite:** Module B01

---

## Why this module

Beginners are often told that a variable is a box. In Python that picture causes
more confusion than it solves. This module replaces it with the better idea:
names point at values, and reassignment changes which value a name points to.
From there, the learner gets the core types they will use most often and a safe
way to move between them.

## What you will be able to do

- Trace names through reassignment and predict the value each name refers to.
- Use `int`, `float`, `str`, and `bool` correctly.
- Convert between types intentionally and understand why `int("3.5")` fails.
- Remember that `input()` always returns text.
- Format output cleanly with f-strings.

## Concept sections

1. **Names are labels, not boxes** — Assignment binds a name to a value.
2. **Numbers** — `int`, `float`, arithmetic, integer division, modulo, exponent.
3. **Text** — Strings, quotes, escapes, concatenation, repetition, `len`.
4. **True, False, and None** — Booleans and absence of a value.
5. **Type conversion** — `int`, `float`, `str`, `bool` as functions.
6. **f-strings** — Values inside text, formatting to two decimals, readable output.
7. **Naming things well** — `snake_case`, clear names, and reserved words.

## Worked example

```python
price = 12.5
tax_rate = 0.2
tax = price * tax_rate
total = price + tax
print(f"Total: ${total:.2f}")
```

Ask two questions every time: what type is each value, and what type should it
be before I do this operation?

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_labels.py` | Trace assignment and rebinding. |
| `ex02_calculator.py` | Read two numbers and print arithmetic results. |
| `ex03_conversions.py` | Fix a script that treats input as a number. |
| `ex04_receipt.py` | Print a small formatted receipt. |
| `ex05_naming.md` | Improve badly named variables and explain why. |

## Common mistakes this module must address

- **Adding a string to a number** — convert deliberately.
- **Assuming `input()` returns a number** — it returns text.
- **Using a builtin as a name** — do not shadow `list` or `str`.
- **Expecting exact decimal arithmetic** — `0.1 + 0.2` is a lesson, not a bug.

## Self check questions

1. What does a name refer to after `x = 5`, `y = x`, `x = 6`?
2. Why does `input()` need converting before arithmetic?
3. What is the difference between `None`, `0`, and `False`?
4. When would you choose `float` over `int`?
5. Write an f-string that prints a price to two decimal places.

## Going deeper

- The Python Tutorial, section 3
- PEP 8 naming conventions
- The format specification mini-language

