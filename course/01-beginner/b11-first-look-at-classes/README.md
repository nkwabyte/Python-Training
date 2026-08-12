# Module B11 — A First Look at Objects and Classes

**Level:** Beginner  |  **Time:** L3 E5  |  **Prerequisite:** Module B10

> **Status: curriculum outline.** The full lesson, exercises, and solutions are
> written in a later build pass. This file specifies exactly what the module
> must contain, so the build can resume without re-deriving anything.

---

## Why this module

The learner has been using objects since Module B01 without being told. This
module names what they have been doing and shows them how to make their own,
but deliberately stops short of inheritance and the data model, which belong to
the intermediate track. The goal is comfort with the idea that data and the
functions that work on it can travel together, plus the honesty to say that a
function is often the better answer.

## What you will be able to do

- Explain what an object is, using types you have already used all along.
- Write a class with an initialiser, attributes, and methods.
- Give a class a readable printed form.
- Say when a class is worth it and when a function or a dictionary is better.
- Read someone else's class and use it from its documentation.

## Concept sections

1. **You have been using objects all along** — A string has methods. A list has methods. The dot is not new, only the making of your own is.
2. **Defining a class** — class, __init__, self, attributes. Building a single small example step by step.
3. **Methods** — Functions that belong to the data. Calling them, and what self really refers to.
4. **A readable object** — __repr__ so that printing your object is useful during debugging. The first dunder method, presented as a hook.
5. **When not to use a class** — A class with one method and no state should be a function. A class that only holds fields might be a dictionary or, better, a dataclass.
6. **A first look at dataclasses** — @dataclass removing the boilerplate the learner just wrote by hand. Full treatment in intermediate Module 11.
7. **Reading other people's classes** — Instantiating from a library's documentation, and knowing what to look for in it.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_bank_account.py` | A small class with state, methods, and validation. |
| `ex02_repr.py` | Add useful __repr__ to three classes and see the debugging difference. |
| `ex03_class_or_function.md` | Decide for eight scenarios: class, function, or dict. |
| `ex04_dataclass.py` | Rewrite a hand-written class as a dataclass. |
| `ex05_use_a_library.py` | Use a library class from its documentation alone. |

## Common mistakes this module must address

- **Forgetting self in a method signature** — TypeError about arguments. Explain the mechanism simply.
- **Shared mutable class attributes** — A list defined on the class is shared by every instance. Show the surprise.
- **Classes with no behaviour** — Six attributes and no methods is a record, not a class.
- **Trying to learn inheritance here** — Deliberately deferred to intermediate Module 10. Say so, so the learner does not feel behind.

## Self check questions

1. What is an object, in one sentence?
2. What does self refer to inside a method?
3. When does __init__ run?
4. Why is __repr__ worth writing?
5. Give an example where a function is a better choice than a class.

## Going deeper

- The Python Tutorial, section 9: Classes, first half only
- The dataclasses module documentation
