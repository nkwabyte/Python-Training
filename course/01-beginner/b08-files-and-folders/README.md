# Module B08 — Files and Folders

**Level:** Beginner  |  **Time:** L3 E5  |  **Prerequisite:** Module B07

> **Status: curriculum outline.** The full lesson, exercises, and solutions are
> written in a later build pass. This file specifies exactly what the module
> must contain, so the build can resume without re-deriving anything.

---

## Why this module

A program that cannot save anything is a toy. This module is the moment the
learner's work becomes persistent, and it is also the first place their code
can damage something, so it teaches safe habits from the first example: open
with with, write to a new file before overwriting an old one, and never build a
path by gluing strings together. CSV and JSON appear here because the learner
already has lists and dictionaries, which are exactly what those two formats
turn into.

## What you will be able to do

- Read and write text files using with, and explain what with guarantees.
- Build paths with pathlib instead of string concatenation.
- Read a CSV into a list of dictionaries and write one back.
- Save and reload program state as JSON.
- Handle a missing file without crashing.

## Concept sections

1. **Opening a file** — Read, write, and append modes. Why write mode silently destroys the old contents, demonstrated safely.
2. **The with statement** — Automatic closing, even when something goes wrong. Presented as a rule now, explained as a protocol in intermediate Module 09.
3. **Reading line by line** — Iterating a file object. Why reading a large file all at once is a habit to avoid.
4. **Paths with pathlib** — Path objects, joining with the slash operator, exists, mkdir, suffix, and stem. Why hard-coded separators break on someone else's machine.
5. **CSV** — csv.DictReader and csv.DictWriter. A spreadsheet becomes a list of dicts and the learner already knows what to do with those.
6. **JSON** — dump and load. Which Python types survive the round trip and which do not.
7. **Failing safely** — Checking existence, catching FileNotFoundError, and writing to a temporary name before replacing the real file.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_read_write.py` | Round trip a text file and count its lines and words. |
| `ex02_pathlib.py` | Rewrite six os.path string operations using pathlib. |
| `ex03_csv_report.py` | Load a CSV of sales, summarise by category, write the summary out. |
| `ex04_json_state.py` | Persist and restore a small application state between runs. |
| `ex05_safe_write.py` | Write via a temporary file so a crash cannot corrupt the original. |

## Common mistakes this module must address

- **Opening in w mode to read** — The file is emptied. Show the damage and the fix.
- **Forgetting to close without with** — Data not flushed, file locked on Windows. Make with non-negotiable.
- **Building paths with plus and slashes** — Breaks across operating systems.
- **Assuming JSON preserves every type** — Tuples come back as lists, and sets do not survive at all.

## Self check questions

1. What does with guarantee that a bare open does not?
2. Which mode should you use to add to the end of a log file?
3. Why is pathlib preferable to string paths?
4. What does DictReader give you for each row?
5. How do you handle a file that might not exist?

## Going deeper

- The Python Tutorial, section 7.2: Reading and Writing Files
- The pathlib module documentation
