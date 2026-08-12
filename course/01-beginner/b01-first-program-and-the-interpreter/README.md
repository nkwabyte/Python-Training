# Module B01 — Your First Program and How Python Runs It

**Level:** Beginner  |  **Time:** L2 E3  |  **Prerequisite:** None. This is the start.

> **Status: curriculum outline.** The full lesson, exercises, and solutions are
> written in a later build pass. This file specifies exactly what the module
> must contain, so the build can resume without re-deriving anything.

---

## Why this module

A beginner's first hour is usually spent fighting the environment, not the
language. This module removes that friction permanently: you install Python
once, understand what an editor, a terminal, a file, and an interpreter each
are, and you run code three different ways so that "it worked yesterday" never
becomes a mystery. It also plants the single most important beginner habit,
which is reading the error message instead of panicking at it.

## What you will be able to do

- Install Python and confirm the version from a terminal.
- Explain in plain words what happens between saving a file and seeing output.
- Run code three ways: the REPL, a saved file, and the editor's run button.
- Use print to see what your program is doing.
- Read a traceback well enough to find the line that broke.

## Concept sections

1. **What a program actually is** — Instructions, saved as text, that a program called an interpreter reads and acts on. No magic, no compilation step to worry about yet.
2. **Installing Python and checking it worked** — Official installer or a version manager. Running python --version. Why more than one Python on a machine is normal and how to tell which one you are using.
3. **The three places code lives** — The REPL for experiments, a .py file for anything you want to keep, and the editor that sits between you and both.
4. **Your first program** — print, a comment, and running it. Changing it and running again. The edit, run, look loop that the rest of the course repeats forever.
5. **Reading output and reading errors** — Standard output versus an error. Anatomy of a traceback in beginner terms: the last line says what, the line above says where.
6. **Setting up your editor** — VS Code or PyCharm, the Python extension, the integrated terminal, and turning on the format-on-save that will keep your code readable.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_hello.py` | Write, save, and run a first program that prints three lines. |
| `ex02_repl_tour.md` | Guided REPL session: evaluate expressions, use the up arrow, exit cleanly. |
| `ex03_break_it.py` | Deliberately introduce four errors and record what each traceback said. |
| `ex04_about_me.py` | Print a small formatted profile block, practising quotes and print. |

## Common mistakes this module must address

- **Running the file from the wrong folder** — The terminal says the file does not exist. Teach pwd, ls, and cd before anything else.
- **Smart quotes from a word processor** — SyntaxError on a line that looks perfect. Teach why a code editor is not optional.
- **Saving as .txt** — Nothing runs. Show the file extension explicitly.
- **Reading the traceback top down** — The beginner blames the wrong line. Establish bottom-up reading in week one.

## Self check questions

1. What is the difference between the REPL and a .py file?
2. Which line of a traceback names the actual error?
3. How do you check which Python version a terminal will use?
4. Why does a comment not change what the program does?
5. What does print actually do?

## Going deeper

- The Python Tutorial, section 2: Using the Python Interpreter
- Real Python: Your First Python Program
- The official Installing Python guide for your operating system
