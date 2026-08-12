# Module B06 — Functions: Naming a Piece of Work

**Level:** Beginner  |  **Time:** L4 E6  |  **Prerequisite:** Module B05

> **Status: curriculum outline.** The full lesson, exercises, and solutions are
> written in a later build pass. This file specifies exactly what the module
> must contain, so the build can resume without re-deriving anything.

---

## Why this module

Up to here the learner has written scripts. Functions are what turn a script
into a program that can grow. The goal of this module is not the syntax, which
is small, but the judgement: what deserves to be a function, what it should be
called, what it should take, and what it should give back. It also introduces
type hints early, as documentation that the tools can check, so that the
learner never experiences them as an advanced extra.

## What you will be able to do

- Write a function with parameters, a return value, and a docstring.
- Explain the difference between printing a result and returning one.
- Use default and keyword arguments to make calls readable.
- Describe what local scope means and why it protects you.
- Add simple type hints to every function you write.

## Concept sections

1. **Defining and calling** — def, parameters, arguments, the call, and the return value. The shape of a function in one page.
2. **Return versus print** — The single most common beginner confusion, shown with a function that is useless because it prints.
3. **Arguments** — Positional and keyword arguments, defaults, and why a default that is a list is a trap. The full explanation waits for intermediate Module 04, but the rule starts here.
4. **Docstrings** — One line saying what the function does. What the caller needs, what they get back.
5. **Local scope** — Names inside a function are private to it. Why that is a feature. What global does and why you will rarely want it.
6. **Type hints as documentation** — name: str, returns int. Running a type checker once so the learner sees it catch a real bug.
7. **Designing small functions** — One job per function. Naming with a verb. Refactoring a forty line script into five named steps, shown as a worked example.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_convert.py` | Write four pure conversion functions with hints and docstrings. |
| `ex02_return_vs_print.py` | Fix three functions that print when they should return. |
| `ex03_defaults.py` | Use defaults and keyword arguments to simplify a noisy call site. |
| `ex04_refactor.py` | Break a long script into named functions without changing behaviour. |
| `ex05_scope.py` | Predict the output of six scope puzzles, then verify. |
| `ex06_validate.py` | Write a validation function that returns a reason, not just a boolean. |

## Common mistakes this module must address

- **Printing instead of returning** — The value cannot be used by the caller. Demonstrate the failure concretely.
- **Forgetting to call the function** — Defining it does nothing. Show the silent no-output case.
- **A mutable default argument** — def f(items=[]) accumulates across calls. State the rule now, explain the mechanism in intermediate Module 04.
- **Functions that do three things** — Name it and if the name needs an and, split it.

## Self check questions

1. What is the difference between a parameter and an argument?
2. Why is print not a substitute for return?
3. What happens to a name created inside a function when it ends?
4. What does def f(x, y=2) allow at the call site?
5. Why write type hints in a language that ignores them at runtime?

## Going deeper

- The Python Tutorial, section 4.7 to 4.9
- PEP 257 on docstring conventions
