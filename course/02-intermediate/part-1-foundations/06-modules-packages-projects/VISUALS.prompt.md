# NotebookLM Visual Prompts — Module 06: Modules, Packages, and Project Layout

---

## Sources to add

| Source | Type |
|---|---|
| `06-modules-packages-projects/README.md` | Upload |
| `01-runtime-and-toolchain/README.md` | Upload |
| https://docs.python.org/3/reference/import.html | Website |
| https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/ | Website |
| https://12factor.net/config | Website |

---

## 1. Cinematic Video Overview

**Format:** Explanation
**Visual style:** Custom, with this description:

```
Clean technical schematic on a dark background. Directory trees drawn as
literal nested folders. sys.path drawn as an ORDERED QUEUE of directories that
a search token travels along. Modules drawn as boxes whose contents fill in
progressively as their body executes. Monospace type for all paths and code.
No characters, no mascots.
```

**Steering prompt (paste this whole block):**

```
Audience: a programmer who can write Python but has lost hours to
ModuleNotFoundError and circular imports and does not know why either happened.

Thesis: `import` is a five-step procedure over an ordered search path, and it
EXECUTES CODE. Every import error in Python is one of those five steps failing
in a way you can name.

1. THE FIVE STEPS. Animate a single `import mypkg.core`:
     step 1: check sys.modules -- show a cache hit ending the whole process
             immediately, and say that this is why a module body runs once per
             process and why editing a module mid-REPL changes nothing.
     step 2: walk sys.path as an ORDERED QUEUE. Show the token entering each
             directory in turn and either finding or not finding the name.
     step 3: read source or a cached .pyc, compile.
     step 4: create an empty module box, INSERT IT INTO sys.modules WHILE STILL
             EMPTY, then execute the body top to bottom, filling the box in.
             The "insert before execute" order must be visually explicit --
             everything about circular imports depends on it.
     step 5: bind the name in the importing namespace.

2. sys.path[0] AND WHY -m MATTERS. Show two runs side by side: `python
   pkg/mod.py` putting pkg/ at the front of the queue, and `python -m pkg.mod`
   putting the CURRENT DIRECTORY at the front and setting __package__. Then
   show a relative import failing in the first case with nothing to be relative
   to, and succeeding in the second. This is the clearest possible explanation
   of "attempted relative import with no known parent package".

3. CIRCULAR IMPORTS. This is the centrepiece; give it the most time. Animate
   a importing b importing a:
     - a's box is created EMPTY and placed in sys.modules
     - a's body starts executing and reaches `from b import beta`
     - b's box is created, b's body starts, reaches `from a import alpha`
     - a is FOUND in sys.modules -- so no re-execution -- but the box is still
       half-empty, and `alpha` is not in it yet
     - the read fails
   Show the half-filled box as the central image. Then show the four fixes,
   each as a change to this picture: extracting the shared piece into a third
   box that both point at (show this as the cycle physically disappearing);
   deferring the import inside a function so it happens after both boxes are
   full; importing the module rather than the name so the attribute read
   happens later; and TYPE_CHECKING removing the runtime edge entirely.

4. SRC LAYOUT. Show two project trees side by side with sys.path drawn beside
   each. In the flat layout, the package directory sits in the project root,
   which IS on sys.path, so `import mypkg` finds the source directory. In the
   src layout, src/ is NOT on sys.path, so the only mypkg that can be found is
   the INSTALLED one. Then dramatise the payoff: a file the author forgot to
   include in the distribution. Under the flat layout the tests pass and the
   user's install crashes; under src, the author's own test run crashes first.

5. WHAT __init__.py IS FOR. Show a package with deep internal modules, and
   __init__.py as a FACADE that re-exports a small curated set of names. Then
   show internals being reorganised behind it while the public import path
   stays identical.

6. CONFIG. Show the same code artifact deployed to three environments, with
   configuration entering from the environment rather than being baked in.
   Show a startup-time validation gate rejecting a missing variable
   immediately, versus the same failure surfacing hours later on a rare code
   path.

Do not cover: pip, wheels, publishing, or dependency resolution. Those are
Module 30.
```

---

## 2. Mind Map

**Prompt:**

```
Build a mind map titled "Imports, Packages, and Layout".

Branch 1 "The import procedure": the five steps, sys.modules caching, module
bodies executing once per process, and the fact that import runs code.

Branch 2 "sys.path": how it is built and in what order, sys.path[0] for each
way of running Python, PYTHONPATH, site-packages, and why runtime sys.path
manipulation is a smell.

Branch 3 "Packages": regular vs namespace, __init__.py's job, __all__,
__main__.py and python -m, and the two-classes-with-the-same-name trap under -m.

Branch 4 "Import forms": absolute vs relative, when relative is acceptable, why
running a package file directly breaks relative imports, and the difference
between `from x import y` and `import x` when y is later rebound.

Branch 5 "Circular imports": the partially-initialised module mechanism, and
the four fixes with the trade-off of each.

Branch 6 "Layout": src vs flat, where tests go, where data files go,
importlib.resources, and what the src layout actually prevents.

Branch 7 "Config and secrets": environment over code, validate at startup,
frozen and typed settings, and why secrets in git are permanent.
```

---

## 3. Study Guide, Quiz, and Flashcards

**Study Guide prompt:**

```
Produce a study guide for someone who will spend tomorrow morning debugging
somebody else's broken Python project.

Include an error-to-cause table covering at least eight import errors:
ModuleNotFoundError for an installed package, ModuleNotFoundError for a local
package, "attempted relative import with no known parent package", "cannot
import name X from partially initialized module", AttributeError on a module,
an import that works in the terminal and fails in the IDE, code changes that
appear to have no effect, and a test suite that passes while the installed
package is broken. For each: the mechanism and the first command to run.

Include a decision table for the four circular-import fixes: what each costs,
and when each is the right choice.

Include a project-layout checklist covering source location, test location,
config, secrets, data files, and entry points.

End with five broken project structures described only by symptom, with the
diagnosis and minimal fix.
```

**Quiz prompt:**

```
Generate 15 diagnosis questions on imports and project structure. Give a
directory tree plus a command plus an error, and ask for the cause.

Required: running a package module directly, a circular import where `import x`
would have worked but `from x import y` did not, a name shadowing a stdlib
module, a test suite that passes because the flat layout hid a missing file,
a patched module attribute that had no effect because the name was imported
directly, and an expensive __init__.py causing slow startup.

For each answer, name the mechanism and the minimal fix, and state what the
tempting wrong fix would have been (usually a sys.path hack) and why it is
worse.
```

**Flashcards prompt:**

```
20 flashcards. Front: a term, an error, or a command. Back: meaning and action.

Include: sys.modules, sys.path[0], __init__.py, __all__, __main__.py,
python -m, absolute import, relative import, __package__, namespace package,
partially initialized module, TYPE_CHECKING, pip install -e, src layout,
importlib.resources, PYTHONPATH, editable install, twelve-factor config,
ImportError vs ModuleNotFoundError, importlib.reload.
```

---

## The specific visuals to insist on

1. **sys.path as an ordered queue** with a search token walking it and stopping
   at the first hit.
2. **The empty module box entering `sys.modules` before its body runs.**
   Everything about circular imports follows from this frame.
3. **The half-filled box** at the moment the circular read fails, with the
   missing name visibly absent.
4. **The cycle disappearing** when a shared piece is extracted into a third
   module.
5. **Two project trees with sys.path drawn beside each**, showing that `src/` is
   simply not on it.
6. **The forgotten file**: tests passing under flat layout, user install
   crashing; tests crashing under src layout.
7. **`__init__.py` as a facade** with internals being reorganised behind an
   unchanged public import path.
8. **`from x import y` copying a binding** versus `import x` holding a reference
   to the module — two arrows with different targets.

---

## Analogies that work

- **A search path as a list of addresses a courier visits in order**, delivering
  to the first one that accepts the parcel. It makes both the shadowing bug and
  the `-m` difference obvious.
- **A module body as a room being furnished.** It is registered as existing the
  moment the door is fitted, before any furniture is in it. Someone who walks
  in early finds an empty room — that is the partially initialised module,
  exactly.
- **`__init__.py` as a shop window.** The stock room can be rearranged freely as
  long as the window shows the same things in the same places.

## Analogies to refuse

- **"Importing is like including a file."** It is not textual inclusion, it
  caches, it executes once, and it creates a namespace object. The C `#include`
  analogy makes every caching behaviour inexplicable.
- **"A package is just a folder."** The `__init__.py`, the namespace it creates,
  and the execution it triggers are the whole subject.
- **Describing a circular import as "two files needing each other".** That
  makes it sound unavoidable. It is a TIMING problem about which names exist
  when, and it is usually a missing third module.

---

## Accuracy guardrails

```
Accuracy requirements:
- A module object is inserted into sys.modules BEFORE its body finishes
  executing. This ordering is the entire mechanism of circular imports and must
  be stated explicitly.
- `import x` and `from x import y` differ: the first binds the module object,
  the second copies the current binding of an attribute. Rebinding x.y later
  does not update the copy.
- Relative imports fail when a file is run directly because __package__ is
  empty, NOT because of sys.path.
- Namespace packages (no __init__.py) are legal since 3.3, but omitting
  __init__.py by accident is a common source of confusing behaviour. Do not
  present it as the default choice.
- The src layout's benefit is that src/ is not on sys.path, so imports resolve
  to the INSTALLED package. Say that mechanism; do not present it as mere
  convention or tidiness.
- Do not recommend sys.path manipulation as a fix for anything.
- __pycache__ caching affects import time only, not runtime speed.
- Do not claim `pip install -e .` copies files. It installs a path hook so the
  source directory is importable; edits take effect without reinstalling.
- Secrets committed to git remain in the history after deletion and must be
  rotated, not merely removed.
```

---

## After watching, you should be able to

- [ ] Recite the five steps of an import and say which makes re-import cheap.
- [ ] Explain why `python pkg/mod.py` breaks a relative import and `-m` does not.
- [ ] Draw the half-filled module box that causes a circular import error.
- [ ] Choose between the four circular-import fixes and justify the choice.
- [ ] Say in one sentence what the `src/` layout prevents.
- [ ] Explain why patching `config.DEBUG` fails when the caller wrote
      `from config import DEBUG`.
- [ ] Say what belongs in `__init__.py` and what must never go there.
- [ ] Name where config goes, where secrets go, and why deleting a secret from
      git is insufficient.
