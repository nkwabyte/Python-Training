# Module B09 — When Things Go Wrong: Errors and Debugging

**Level:** Beginner  |  **Time:** L3 E5  |  **Prerequisite:** Module B08

> **Status: curriculum outline.** The full lesson, exercises, and solutions are
> written in a later build pass. This file specifies exactly what the module
> must contain, so the build can resume without re-deriving anything.

---

## Why this module

Beginners lose more hours to fear of errors than to the errors themselves. This
module reframes an exception as information, teaches a repeatable diagnostic
procedure, and introduces the debugger early enough that the learner never
becomes permanently dependent on scattering print statements. It deliberately
teaches narrow exception handling from the first example, so the bare except
habit never forms.

## What you will be able to do

- Name the six exceptions a beginner meets most and say what each usually means.
- Read a traceback bottom up and identify the failing line in your own code.
- Catch a specific exception and recover meaningfully.
- Use breakpoint to inspect a running program.
- Reduce a failing program to a minimal example that still fails.

## Concept sections

1. **Errors are information** — Syntax errors happen before anything runs. Runtime errors happen during. The difference tells you where to look.
2. **The six you will meet** — SyntaxError, NameError, TypeError, ValueError, IndexError, KeyError, each with a typical cause and a typical fix.
3. **Reading a traceback** — Bottom up. Your files versus library files. Following the call chain back to your own code.
4. **try and except** — Catching one named exception. Why except Exception is a last resort and bare except is never right.
5. **Raising your own** — raise ValueError with a message that tells the caller what to do differently.
6. **The debugger** — breakpoint(), then n, s, c, p, and q. Ten minutes of practice that saves years of print debugging.
7. **Shrinking the problem** — Comment out, halve the input, isolate. The general procedure for any bug, in any language.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_identify.py` | Match twelve tracebacks to their causes. |
| `ex02_fix_them.py` | Six broken scripts, one bug each, from the six common exceptions. |
| `ex03_handle.py` | Add narrow exception handling to a fragile input loop. |
| `ex04_debugger.md` | A guided pdb session through a program with a wrong result but no crash. |
| `ex05_minimise.py` | Reduce a fifty line failing script to five lines that still fail. |

## Common mistakes this module must address

- **Catching everything with bare except** — Hides real bugs including your typos, and swallows ctrl-c. Forbid it now.
- **Catching then ignoring** — except: pass turns a loud failure into a silent wrong answer.
- **Reading the traceback top down** — The top frame is usually library code you did not write.
- **Fixing symptoms** — Changing the line that raised without understanding why the value was wrong.

## Self check questions

1. What is the difference between a SyntaxError and a NameError?
2. Which end of the traceback do you read first?
3. Why is except Exception better than bare except, and still not great?
4. When should your code raise instead of returning None?
5. What does breakpoint() do?

## Going deeper

- The Python Tutorial, section 8: Errors and Exceptions
- The pdb module documentation
