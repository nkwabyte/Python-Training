# Module 06 — Modules, Packages, and Project Layout

**Time budget:** 4 hours lesson, 5 hours exercises
**Prerequisite:** Modules 01-05

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

Every Python developer loses at least one full day to an import error. Usually
several. The errors are:

```
ModuleNotFoundError: No module named 'mypackage'
ImportError: attempted relative import with no known parent package
ImportError: cannot import name 'X' from partially initialized module (circular import)
AttributeError: module 'X' has no attribute 'Y'
```

All four have precise, learnable causes. This module removes them permanently,
and gives you a project layout that prevents most of them from arising.

---

## 1. What `import` actually does

```python
import json
```

1. Look in `sys.modules`. If `"json"` is there, bind it and **stop**. The module
   body does not run again.
2. Otherwise, walk the *finders* in `sys.meta_path`. In practice: built-in
   modules, then frozen modules, then the path finder, which searches
   `sys.path` in order.
3. Load it: read the source (or a cached `.pyc`), compile, create a module
   object, **execute the body top to bottom** inside that module's namespace.
4. Insert it into `sys.modules` **before** executing the body. (This is what
   makes some circular imports survivable — more below.)
5. Bind the name in the importing namespace.

Three consequences worth memorising:

**A module's body runs exactly once per process.** Editing a module and
re-importing it in the same REPL session does nothing. That is why
`importlib.reload` exists, and why restarting is usually easier.

**Import executes code.** `import mymodule` runs every top-level statement in
it. A module that opens a database connection or reads a file at import time
does that whenever anyone imports it, including your test suite.

**Names are bound at import time.** `from x import y` copies the *current*
binding of `y`. If `x.y` is later rebound, your copy does not change:

```python
from config import DEBUG      # copies the value NOW
import config                  # binds the MODULE; config.DEBUG reads it later
```

That is a real difference, and it is why patching in tests usually targets
`module.attribute` rather than an imported name (Module 18).

---

## 2. `sys.path`, precisely

```python
import sys; print(sys.path)
```

Built in this order:

| Position | Contents | Set by |
|---|---|---|
| First | Script's directory (`python app.py`), or CWD (`-c`, `-m`, REPL) | The interpreter |
| Then | `PYTHONPATH` environment variable, if set | You |
| Then | Standard library directories | The install |
| Last | `site-packages` for the active environment | The venv |

The first entry is the one that bites. `python app.py` puts `app.py`'s directory
first; `python -m pkg.mod` puts the **current working directory** first. That
difference is the whole `-m` story.

**Never modify `sys.path` at runtime** to make imports work:

```python
sys.path.insert(0, "../..")     # a smell that becomes a bug
```

It breaks when the CWD changes, when the file is moved, when the code is
packaged, and when someone imports your module instead of running it. The
correct fix is always: install your package (`pip install -e .`) or run it with
`-m` from the right directory.

---

## 3. Packages

A **package** is a directory Python can import. Two kinds:

```
mypkg/                    regular package
├── __init__.py           <- its presence makes this a package
├── core.py
└── util.py

mynamespace/              namespace package (PEP 420, 3.3+)
└── plugin.py             <- no __init__.py; can span multiple directories
```

Use a **regular package** — include `__init__.py` — unless you specifically want
a namespace package for a plugin system split across distributions. The absence
of `__init__.py` interacts badly with test discovery and with some tooling, and
the failure mode is confusing.

### What belongs in `__init__.py`

```python
# mypkg/__init__.py
"""One-line description of the package."""

from mypkg.core import Engine, run          # curate the public API
from mypkg.errors import EngineError

__all__ = ["Engine", "EngineError", "run"]  # what `from mypkg import *` gives
__version__ = "1.2.0"
```

Its job is to define the package's **public surface**, so callers write
`from mypkg import Engine` instead of `from mypkg.core.internals import Engine`.
That indirection is what lets you reorganise internals without breaking anyone.

Keep it small and side-effect-free. Every import of any submodule executes
`__init__.py` first, so expensive work there is paid by everyone — this is the
most common cause of a slow CLI startup.

---

## 4. Absolute and relative imports

```python
# inside mypkg/core.py
from mypkg.util import helper       # ABSOLUTE -- preferred
from .util import helper            # relative: same package
from ..other.thing import helper    # relative: parent package
```

**Prefer absolute imports.** They work identically wherever the file is read
from, they survive moving a file, and they are unambiguous to a reader.

Relative imports are acceptable within a self-contained subpackage where the
sibling relationship is meaningful. They have one hard rule:

> **A relative import only works when the module is imported as part of a
> package.** Running the file directly makes `__package__` empty, and the
> relative import has nothing to be relative *to*.

That is this error, exactly:

```
ImportError: attempted relative import with no known parent package
```

```bash
python mypkg/core.py        # FAILS: core.py is a script, not part of a package
python -m mypkg.core        # WORKS: imported as part of mypkg
```

**The rule: code inside a package is run with `-m`.**

---

## 5. `__main__.py` and `python -m`

```
mytool/
├── __init__.py
├── __main__.py         <- runs on `python -m mytool`
└── cli.py
```

```python
# mytool/__main__.py
import sys
from mytool.cli import main

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

This is how `python -m http.server`, `python -m pytest`, and `python -m venv`
all work. It gives your package a runnable entry point that works without
installation. Once installed, a `[project.scripts]` entry in `pyproject.toml`
(Module 30) provides the `mytool` command that most users will actually type.

One subtlety worth knowing: under `-m`, your entry module is executed as
`__main__`, so a class defined there has `__module__ == "__main__"`. If another
module also imports it by its real name, you get **two distinct classes with the
same name**, and `isinstance` fails mysteriously. Keep `__main__.py` to a thin
shim that imports and calls; define nothing important in it.

---

## 6. Circular imports

```python
# a.py
from b import beta
def alpha(): return beta()

# b.py
from a import alpha              # ImportError
def beta(): return "b"
```

**The mechanism.** Importing `a` starts executing `a`'s body and puts a
*partially initialised* `a` in `sys.modules`. `a` imports `b`, which starts
executing, which imports `a` — found in `sys.modules`, so no re-execution — and
tries to read `alpha` from it. But `a`'s body has not reached the `def alpha`
line yet. The name does not exist. Hence:

```
ImportError: cannot import name 'alpha' from partially initialized module 'a'
(most likely due to a circular import)
```

Note that `import a` (binding the module) often survives where
`from a import alpha` (reading an attribute now) fails, because the attribute is
not read until call time.

### Four fixes, in order of preference

**1. Extract the shared thing.** Usually the two modules both need a type or a
constant. Move it to a third module both import. This is the right fix roughly
80 percent of the time, and the cycle was telling you the design had a missing
piece.

```
a.py ─┐
      ├──> types.py
b.py ─┘
```

**2. Import inside the function.** Defers the import until call time, when both
modules are fully loaded.

```python
def alpha():
    from b import beta      # deferred
    return beta()
```

Legitimate, but it hides a dependency from the top of the file and adds a
(cached, tiny) lookup per call. Use it deliberately, with a comment.

**3. Import the module, not the name.**

```python
import b
def alpha(): return b.beta()      # attribute read happens at CALL time
```

**4. `if TYPE_CHECKING`** — for cycles that exist only because of type hints:

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from b import Beta            # not imported at runtime at all

def alpha(x: Beta) -> None: ...   # a string annotation; never evaluated
```

This is extremely common in typed codebases and costs nothing.

---

## 7. Project layout

Two layouts are in wide use. One of them is better and it is worth knowing why.

### The src layout — recommended

```
myproject/
├── pyproject.toml
├── README.md
├── src/
│   └── mypkg/
│       ├── __init__.py
│       ├── core.py
│       └── cli.py
├── tests/
│   ├── conftest.py
│   └── test_core.py
└── docs/
```

The point is that `src/` is **not** on `sys.path`. So `import mypkg` cannot
accidentally find your source directory — it can only find the *installed*
package. That means:

- Your tests exercise the package as users will receive it. A file you forgot to
  include in the distribution fails in *your* test run, not in a user's install.
- No accidental shadowing from files in the project root.
- The "works for me, broken when installed" class of bug is eliminated.

The cost is that you must install the package to work on it — which is one
command, once:

```bash
pip install -e .          # editable: edits take effect immediately
uv pip install -e .
```

### The flat layout

```
myproject/
├── pyproject.toml
├── mypkg/
│   └── __init__.py
└── tests/
```

Simpler, works without installing, and is fine for a small script or a personal
tool. It is what most tutorials show. Use `src/` for anything you intend to
distribute or keep.

### Where things go

| Thing | Location | Note |
|---|---|---|
| Source | `src/mypkg/` | |
| Tests | `tests/` | Outside the package, so they are not shipped |
| Config schema and defaults | `src/mypkg/config.py` | Code |
| Actual config values | Environment variables, or a file outside the repo | Not code |
| **Secrets** | Environment or a secret manager. **Never in the repo.** | Module 35 |
| Data files the package needs | `src/mypkg/data/`, read with `importlib.resources` | Not `open(__file__/..)` |
| Scripts | `scripts/`, or a `[project.scripts]` entry point | |

**Reading package data correctly:**

```python
from importlib.resources import files
schema = files("mypkg.data").joinpath("schema.json").read_text(encoding="utf-8")
```

Not `open(os.path.join(os.path.dirname(__file__), "data/schema.json"))`. The
`__file__` approach breaks when the package is installed from a zip, in a
frozen executable, or in some container layouts. `importlib.resources` works
everywhere.

---

## 8. Configuration and secrets, briefly

The rule (from the twelve-factor app, and it holds up):

> **Config that varies between deployments belongs in the environment. Code does
> not.**

```python
import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    database_url: str
    debug: bool = False
    timeout: int = 30

    @classmethod
    def from_env(cls) -> "Settings":
        url = os.environ.get("DATABASE_URL")
        if not url:
            raise RuntimeError("DATABASE_URL is required")   # fail at STARTUP
        return cls(
            database_url=url,
            debug=os.environ.get("DEBUG", "").lower() in {"1", "true", "yes"},
            timeout=int(os.environ.get("TIMEOUT", "30")),
        )
```

Three things this gets right, all of which matter more than they look:

1. **Validated once, at startup.** A missing variable crashes the process on
   boot, not at 3am when the code path is first hit.
2. **Frozen.** Configuration cannot be mutated halfway through a request.
3. **Typed.** `timeout` is an `int`, not the string the environment gave you.

`pydantic-settings` does all of this with less code and better errors, and is
what Module 28 uses. Understand the pattern first.

---

## Common mistakes in this module

| Mistake | Symptom | Fix |
|---|---|---|
| `python pkg/mod.py` | "attempted relative import" | `python -m pkg.mod` |
| `sys.path.insert` hacks | Works locally, breaks when packaged | `pip install -e .` |
| Heavy work in `__init__.py` | Slow startup for every consumer | Keep it to re-exports |
| Circular import | "partially initialized module" | Extract the shared piece |
| `from config import DEBUG` then patching `config.DEBUG` | Patch has no effect | Import the module, read the attribute |
| File named like a stdlib module | Bizarre `AttributeError` | Rename; `src/` layout prevents it |
| Secrets in the repo | A permanent leak, even after deletion | Environment variables |
| `open(__file__/../data)` | Breaks when installed from a zip | `importlib.resources` |
| No `__init__.py`, unintended namespace package | Confusing test-discovery failures | Add `__init__.py` |
| Config read at import time | Untestable, order-dependent | Read it in a function |

---

## Self-check quiz

1. What are the five steps of an import, and which one makes the second import
   of a module cheap?
2. What is `sys.path[0]` for `python app.py` versus `python -m pkg.mod`?
3. Why does a relative import fail when you run the file directly?
4. Explain "partially initialized module" in terms of what the interpreter is
   doing.
5. Name four fixes for a circular import and say which is usually right.
6. What is the concrete benefit of the `src/` layout, in one sentence?
7. Why does `from config import DEBUG` behave differently from `import config`
   when the value is later changed?
8. What belongs in `__init__.py`, and what must not?
9. Why is `importlib.resources` better than `open(__file__ + "/../data")`?
10. Where do secrets go, and why is deleting them from git insufficient?

---

## Exercises

1. **[`ex01_import_lab/`](exercises/ex01_import_lab/)** — A package that fails
   five different ways. Diagnose each from the error alone, then fix.
2. **[`ex02_circular/`](exercises/ex02_circular/)** — A real circular import
   between three modules. Fix it four different ways and argue for one.
3. **[`ex03_restructure/`](exercises/ex03_restructure/)** — Convert a 400-line
   single-file script into a proper `src/` package with a `pyproject.toml`, a
   `__main__.py`, and tests that run against the installed package.
4. **[`ex04_settings.py`](exercises/ex04_settings.py)** — Build a typed,
   validated, layered settings object: defaults, then a file, then the
   environment, with clear errors.

---

## Going deeper

- [The import system](https://docs.python.org/3/reference/import.html) — dense, definitive
- [`importlib.resources`](https://docs.python.org/3/library/importlib.resources.html)
- [PEP 420 — Namespace packages](https://peps.python.org/pep-0420/)
- [Packaging User Guide: src layout vs flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)
- [The Twelve-Factor App: Config](https://12factor.net/config)

---

**Next:** [Module 07 — Milestone Project: Inventory CLI](../07-project-inventory-cli/README.md)
