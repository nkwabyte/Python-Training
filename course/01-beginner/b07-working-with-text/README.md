# Module B07 — Working with Text

**Level:** Beginner  |  **Time:** L3 E5  |  **Prerequisite:** Module B06

> **Status: curriculum outline.** The full lesson, exercises, and solutions are
> written in a later build pass. This file specifies exactly what the module
> must contain, so the build can resume without re-deriving anything.

---

## Why this module

Most beginner programs are text in, text out. Text is also where the first
genuinely confusing bug lives: a string method that seems to do nothing,
because strings cannot be changed in place. This module makes immutability
concrete rather than theoretical, and gives the learner a working toolkit for
cleaning and reshaping the messy text that real input always is.

## What you will be able to do

- Use the string methods that cover most real work: strip, split, join, replace, lower, startswith.
- Explain why a string method returns a new string instead of changing the old one.
- Slice a string confidently, including with negative indexes.
- Format numbers and text into aligned, readable output.
- Clean a line of untrusted user input before using it.

## Concept sections

1. **Strings are immutable** — Methods return new strings. The classic bug of calling s.upper() and ignoring the result, shown before it is explained.
2. **The method toolkit** — strip, lower, upper, title, replace, startswith, endswith, find, count, and when each earns its place.
3. **split and join** — Turning text into a list and back. Splitting a CSV line by hand to understand what a parser does for you.
4. **Slicing** — start, stop, step on strings. Negative indexes. Reversing. The same rules that apply to lists.
5. **Formatting output** — f-string alignment, width, and precision. Building a table that lines up in a terminal.
6. **Multi-line text and escapes** — Triple quotes, newline, tab, and the raw string prefix for Windows paths.
7. **A first look at membership and searching** — in for substrings, and a one-paragraph preview of regular expressions with a pointer to advanced Module 19.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_immutable.py` | Predict and fix five cases where a string method result was discarded. |
| `ex02_clean_input.py` | Normalise messy names: whitespace, capitalisation, and stray punctuation. |
| `ex03_split_join.py` | Parse a semicolon-separated record and rebuild it in a new order. |
| `ex04_slices.py` | Twelve slicing puzzles including negative steps. |
| `ex05_table.py` | Print an aligned report from a list of records using f-string formatting. |

## Common mistakes this module must address

- **Discarding a method result** — s.strip() alone does nothing useful. The single most common text bug.
- **Assuming split() and split(' ') behave the same** — They differ on runs of whitespace. Show it.
- **Off-by-one in slices** — The stop index is exclusive. Draw the boundaries between characters.
- **Concatenating in a loop for large text** — Works, but teaches a habit that scales badly. Show join.

## Self check questions

1. Why does s.upper() not change s?
2. What is the difference between split() and split(' ')?
3. What does s[-3:] give you?
4. How would you turn a list of words into one comma-separated line?
5. Which method removes surrounding whitespace?

## Going deeper

- The standard library reference on string methods
- The format specification mini-language
