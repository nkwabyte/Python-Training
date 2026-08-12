# NotebookLM Visual Prompts — Module 01: The Runtime and the Toolchain

**Generate these after your first read of the README, before you start the
exercises.**

---

## Sources to add

| Source | Type |
|---|---|
| `01-runtime-and-toolchain/README.md` | Upload |
| `SETUP.md` | Upload |
| `course/appendix/glossary.md` | Upload |
| https://docs.python.org/3/reference/import.html | Website |
| https://docs.python.org/3/library/dis.html | Website |
| https://peps.python.org/pep-0405/ | Website |

---

## 1. Cinematic Video Overview

**Format:** Explanation
**Visual style:** Custom, with this description:

```
Clean technical schematic. Flat vector diagrams on a dark background. Files
shown as labelled rectangles, data flowing between them along animated arrows.
Monospace type for all code, filenames, and paths. No characters, no offices,
no mascots, no laptop-with-coffee stock imagery. Think interpreter
documentation, not a corporate explainer.
```

**Steering prompt (paste this whole block):**

```
Audience: a working programmer, fluent in at least one other language, who can
already write Python syntax but has never looked underneath it. They are not a
beginner. Do not explain what a variable or a loop is.

Thesis: Python is not "just interpreted". Source becomes an abstract syntax
tree, then bytecode, then it is executed by a virtual machine, and the boundary
between the compile step and the execute step is what determines which of your
mistakes are caught early and which are caught by your users.

Structure the video as the journey of one file, app.py, from typing Enter to
producing output.

1. TOKENIZE AND PARSE. Show the source text becoming a tree. Make the point
   that this stage checks SYNTAX ONLY. Show a file where line 1 is a valid
   print and line 3 has a syntax error, and show that line 1 NEVER RUNS. This
   is the moment the viewer should understand what "compile time" means in
   Python.
2. COMPILE. Show the tree becoming a flat list of bytecode instructions. Show
   the actual disassembly of a two-line add function as a stack machine:
   push a, push b, apply the binary operator, return. Animate the value stack.
3. CACHE. Show __pycache__/module.cpython-312.pyc being written, and state
   clearly that this happens for IMPORTED modules, not for the script you ran,
   and that it saves parse time, not execution time.
4. EVALUATE. Show the eval loop stepping through instructions. Show a NameError
   occurring at this stage, not the previous one, on a line that was compiled
   perfectly happily.

Then a second act on the environment, which is a separate idea and should feel
like one:

5. THE INTERPRETER, THE ENVIRONMENT, AND THE PACKAGE MANAGER as three distinct
   things. Show one machine with three projects, each with its own .venv
   directory containing its own site-packages, and show two projects holding
   incompatible versions of the same library side by side without conflict.
   Show that activating an environment simply puts its bin/ directory at the
   front of PATH. Emphasise there is no global registry and no magic.
6. sys.path AND THE SHADOWING BUG. This is the highest-value 45 seconds in the
   video. Show a project folder containing a file the user wrote called
   random.py, next to app.py which does "import random". Animate the search:
   sys.modules cache first, then built-ins, then each sys.path entry IN ORDER,
   with the script's own directory FIRST. Show the arrow landing on the user's
   file instead of the standard library, and show the resulting bizarre
   AttributeError. Then show the one-line diagnosis: print(random.__file__).

Close on reading a traceback bottom-up. Show a three-frame traceback and
animate the reading order as arrows going UPWARD from the last line: first the
exception type and message, then the frame that raised, then the call chain.

Do not cover: syntax, data types, classes, or how to write Python code. This
video is only about what runs it.
```

---

## 2. Mind Map

**Prompt:**

```
Build a mind map titled "From Source to Output".

Primary branch 1: "The pipeline". Sub-branches for Tokenize/Parse, Compile,
Cache, Evaluate. Under each: what it consumes, what it produces, and which
class of error surfaces there. Make the syntax-error vs runtime-error split
visually obvious.

Primary branch 2: "Where code lives". Sub-branches: script, module, package,
__name__ == "__main__", python -m vs python file.py, and what changes about
sys.path between them.

Primary branch 3: "How import finds things". Ordered sub-branches: sys.modules
cache, built-ins, sys.path entries. Add a leaf for the shadowing bug and its
one-line diagnosis.

Primary branch 4: "The environment". Sub-branches: interpreter, virtual
environment, package manager, site-packages, PATH activation, pinning vs
ranges, lockfiles.

Primary branch 5: "Implementation vs language". Sub-branches listing at least
four things that are CPython behaviour rather than Python guarantees: the GIL,
reference counting, small-int caching, int memory size.
```

---

## 3. Study Guide, Quiz, and Flashcards

**Study Guide prompt:**

```
Produce a study guide for someone who will be debugging a broken Python
environment tomorrow morning.

Include a diagnosis table: given a symptom, what is the likely cause and what
is the FIRST command to run. Cover at least ten symptoms, including
ModuleNotFoundError for an installed package, an AttributeError from a standard
library module, "attempted relative import with no known parent package", an
import that works in the terminal but fails in the editor, and code changes
that appear to have no effect.

Include a table of the four ways to run Python (file, -m, -c, REPL) with what
sys.path[0] is in each case and when each is correct.

End with five scenarios described only by symptom, each followed by the
diagnosis and the minimal fix.
```

**Quiz prompt:**

```
Generate 15 questions on the Python runtime and environment. Weight them
heavily toward diagnosis rather than recall. Give a symptom or a traceback and
ask for the cause. Include at least four questions where the naive answer is
wrong: a file shadowing a stdlib module, a module executing on import because
it lacks a __name__ guard, a package run as a script instead of with -m, and an
assert used for validation that vanishes under -O.

For each answer, state not just what is correct but what the tempting wrong
answer was and why it fails.
```

**Flashcards prompt:**

```
20 flashcards. Front: a term, a command, or an error message. Back: what it
means and the one-line action it implies.

Include: __pycache__, sys.path[0], sys.modules, __name__ == "__main__",
python -m, site-packages, virtual environment, dis, bytecode, AST,
SyntaxError vs NameError timing, ModuleNotFoundError, "attempted relative
import", CPython vs Python, pinning vs ranges, uv, ruff, mypy, breakpoint(),
python -i.
```

---

## The specific visuals to insist on

Add these to the steering prompt if the first generation is too abstract.

1. **The syntax error that kills line 1.** A file where a valid `print` on line
   1 never executes because of an error on line 3. Show the whole file greying
   out at once. This is the single clearest way to make "compile time" concrete
   in a language people believe has none.
2. **The bytecode stack machine.** `a + b` as four instructions with an animated
   value stack: push, push, pop-pop-apply-push, return.
3. **The shadowing search.** A folder with a user-written `random.py`, and the
   import search visibly checking directories in order and stopping at the
   wrong one.
4. **Three projects, three environments.** One machine, three `.venv`
   directories, two incompatible versions of the same package living peacefully.
   Then the same machine with no venvs, and the version collision.
5. **PATH activation.** A literal queue of directories with the venv's `bin/`
   being inserted at the front, and `which python` resolving to it.
6. **The traceback read upward.** Arrows numbered 1, 2, 3 going from the bottom
   line upward, with labels "what", "where", "how I got here".
7. **The `-O` disappearing assert.** The same file compiled twice, with the
   assert statement literally vanishing from the bytecode in one of them.

---

## Analogies that work

- **A recipe compiled into instructions for a specific kitchen robot.** The
  parse-and-compile step converts a recipe into robot instructions; the eval
  loop is the robot executing them. It makes clear that a *typo in the recipe*
  is caught during conversion, but *"there is no flour in the cupboard"* is only
  discovered while cooking.
- **A venv as a separate toolbox per job site**, rather than one shared
  workshop. Activation is picking up that toolbox. Nothing is registered
  centrally; you just carry a different box.

## Analogies to refuse

- **"Python reads your code line by line as it runs."** This is the standard
  explanation and it is wrong in a way that matters: it cannot explain why a
  syntax error on line 500 prevents line 1 from running. Instruct the model not
  to use it.
- **Comparing an environment to a "container" or "sandbox".** A venv isolates
  nothing but the package search path. It is not a security or process
  boundary, and calling it a sandbox creates dangerous expectations.

---

## Accuracy guardrails

Paste these into the steering prompt:

```
Accuracy requirements:
- Do not say Python is "not compiled". It compiles to bytecode. It does not
  compile to machine code ahead of time. Say it precisely.
- Do not claim .pyc files make a program run faster. They eliminate parse and
  compile time at import, which affects STARTUP only.
- The GIL, reference counting, small-integer caching, and the memory size of an
  int are CPython implementation details, not Python language guarantees. Label
  them as such every time they appear.
- Do not describe a virtual environment as isolating processes, filesystems, or
  security boundaries. It changes where packages are installed and found. That
  is all.
- Do not present `python setup.py install` or `easy_install` as current. They
  are obsolete.
- State that `assert` statements are removed by the -O flag, and therefore must
  never be used for input validation or security checks.
- Do not use `List[int]` / `Dict[str, int]` typing syntax. This course targets
  3.12; use `list[int]` and `dict[str, int]`.
```

---

## After watching, you should be able to

- [ ] Explain why a syntax error on the last line prevents the first line from
      running, in terms of the pipeline.
- [ ] Say what `__pycache__` caches and what it does *not* speed up.
- [ ] Given `import foo` behaving strangely, name the one line that diagnoses a
      shadowed module.
- [ ] Describe what a virtual environment is physically, on disk, in two
      sentences with no metaphors.
- [ ] Say what `sys.path[0]` is for `python app.py`, for `python -m pkg.mod`,
      and for the REPL.
- [ ] Explain the difference between `__name__ == "__main__"` being true and
      false, and what breaks without the guard.
- [ ] Read a three-frame traceback aloud in the correct order.
- [ ] Name four things that are CPython behaviour rather than Python guarantees.
