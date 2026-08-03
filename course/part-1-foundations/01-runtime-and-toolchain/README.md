# Module 01 — The Runtime and the Toolchain

**Time budget:** 3 hours lesson, 4 hours exercises
**Prerequisite:** [`SETUP.md`](../../../SETUP.md) completed, `python setup/verify.py` passing

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md) has ready-to-paste
> NotebookLM prompts for a video explainer, mind map, and study guide on this
> module. See [`course/VISUAL-GUIDE.md`](../../VISUAL-GUIDE.md) for the workflow.

---

## Why this module comes first

You already know how to write a `for` loop. What you probably do not know is
what actually happens between pressing Enter on `python app.py` and seeing
output, and that gap is where a specific class of confusion lives:

- Why does `import mymodule` sometimes pick up a stale version?
- Why does a `__pycache__` folder appear, and does it matter?
- Why does `python foo/bar.py` fail with a relative-import error when
  `python -m foo.bar` works?
- Why is Python "slow", and slow at *what* exactly?
- Why can two people run the same script and get different behaviour?

Every one of these is answered by understanding the runtime rather than the
language. Get it now and you will spend the next nineteen weeks debugging your
logic instead of your environment.

---

## 1. Python is a specification. CPython is a program.

"Python" names a language specification. The thing on your machine is an
*implementation* of it.

| Implementation | Written in | Why it exists |
|---|---|---|
| **CPython** | C | The reference implementation. When people say "Python", this is it. |
| **PyPy** | RPython | A JIT compiler. Often 3-10x faster on long-running pure-Python code. |
| **MicroPython** | C | Runs on microcontrollers with kilobytes of RAM. |
| **GraalPy** | Java | Runs on the JVM, interoperates with Java. |
| **Pyodide** | C → WASM | CPython compiled to WebAssembly; runs in a browser. |

This course targets CPython, because that is what you will deploy. But the
distinction matters for a reason that comes up constantly: **things that are
true of CPython are not necessarily true of Python.** The GIL is a CPython
implementation detail. Reference counting is a CPython implementation detail.
So is the exact memory size of an `int`. When you learn one of these, tag it
mentally as "CPython behaviour" so that you never build a design on it that a
runtime change could break.

```python
import sys
print(sys.implementation.name)     # 'cpython'
print(sys.version)                  # 3.12.x ... [Clang ...]
```

---

## 2. What actually happens when you run a script

Python is often called "interpreted", which is true but so compressed that it
misleads. There is a compilation step. It just targets a virtual machine instead
of your CPU.

```
app.py  (source text)
   |
   |  [1] TOKENIZE + PARSE      -> Abstract Syntax Tree
   v                               (SyntaxError happens HERE, before anything runs)
   AST
   |
   |  [2] COMPILE               -> bytecode: a flat list of VM instructions
   v
   code object  (cached to __pycache__/app.cpython-312.pyc for imported modules)
   |
   |  [3] EVALUATE              -> the eval loop executes bytecode one op at a time
   v
   output / side effects        (NameError, TypeError, etc. happen HERE, at runtime)
```

The crucial split is between stage 1-2 and stage 3.

**Stage 1-2 is static.** It happens before a single line of your program runs.
Only *syntax* is checked. This is why a file with a typo on line 500 will not
run line 1:

```python
print("hello")
def broken(:      # SyntaxError
    pass
```

You never see "hello". The whole file failed to compile.

**Stage 3 is dynamic.** Names, types, attributes, and arguments are all resolved
while the program runs. This is why this file *does* print "hello":

```python
print("hello")
def broken():
    return undefined_name + 1     # NameError, but only if you CALL it
```

That difference is the origin of most of Python's productivity and most of its
danger, and it is why Module 17 (typing) and Module 18 (testing) exist. In a
compiled language the compiler finds your typo. In Python, a test or a type
checker finds it, or your user does.

### See it for yourself

```python
import dis

def add(a, b):
    return a + b

dis.dis(add)
```

```
  2           0 RESUME                   0
  3           2 LOAD_FAST                0 (a)
              4 LOAD_FAST                1 (b)
              6 BINARY_OP                0 (+)
             10 RETURN_VALUE
```

That is your function. A stack machine: push `a`, push `b`, apply `+`, return.
You do not need to read bytecode fluently — Module 24 goes deep — but you should
know it exists, because it explains performance questions that are otherwise
mysterious. `dis` is the fastest way to settle an argument about what Python
"really does".

Try these and compare:

```python
dis.dis(compile("x = 1 + 2", "<s>", "exec"))       # constant folding at compile time
dis.dis(compile("s = 'a' + 'b' + 'c'", "<s>", "exec"))
dis.dis(compile("[x*2 for x in y]", "<s>", "exec"))  # comprehensions have their own scope
```

---

## 3. `__pycache__` and the `.pyc` question

When you **import** a module, CPython caches the compiled bytecode next to it:

```
mypackage/
├── util.py
└── __pycache__/
    └── util.cpython-312.pyc
```

Rules worth knowing:

- Caching happens for **imported modules**, not for the top-level script you ran.
  That is why running `app.py` never creates `__pycache__/app...pyc`.
- The cache key includes the source's mtime and size (or, with
  `PYTHONPYCACHEPREFIX` / hash-based pycs, a hash). Edit the source and the
  cache is invalidated automatically.
- The interpreter version is in the filename, so 3.11 and 3.12 caches coexist.
- **Never commit `__pycache__`.** It is in the course `.gitignore`.
- It saves *parse and compile* time, not execution time. Startup, not runtime.

If you ever genuinely suspect a stale cache (rare, but it happens with
filesystem clock skew in containers):

```bash
find . -name "__pycache__" -type d -exec rm -rf {} +
# or run without writing caches:
python -B app.py
```

---

## 4. Script, module, package: three words people use interchangeably and should not

| Term | Definition | Example |
|---|---|---|
| **Script** | A `.py` file you execute directly | `python app.py` |
| **Module** | A `.py` file that gets imported; becomes a module object | `import util` |
| **Package** | A directory of modules, importable as a unit | `import mypkg.util` |

The same file can be both a script and a module. That is what this idiom is
about, and it is the most misunderstood four lines in Python:

```python
def main() -> None:
    print("doing the work")

if __name__ == "__main__":
    main()
```

Every module has a `__name__`. When a file is **imported**, `__name__` is the
module's dotted name (`"util"`, `"mypkg.util"`). When a file is **run
directly**, `__name__` is the string `"__main__"`.

So the guard means: *do this only when I am the entry point, not when someone
imports me.* Without it, importing your module executes your program — which is
exactly what happens the first time someone tries to unit-test a script that
lacks the guard.

### Four ways to run Python, and when each is right

```bash
python app.py              # run a file as a script
python -m mypackage        # run a package's __main__.py
python -m mypackage.mod    # run a module inside a package, as a module
python -c "print(1+1)"     # run a string
python                     # REPL
```

`python -m` is not a stylistic preference. It changes `sys.path` and it changes
`__package__`, which is why relative imports work under `-m` and fail under
`python path/to/file.py`. Module 06 covers this in full; for now, absorb the
rule: **if it lives in a package, run it with `-m`.**

---

## 5. `sys.path`: how `import` finds things

When you write `import requests`, Python searches, in order:

1. `sys.modules` — the cache of already-imported modules. Import twice, execute
   once. (This is why editing a module mid-REPL-session does not take effect,
   and why `importlib.reload` exists.)
2. Built-in modules compiled into the interpreter (`sys`, `builtins`).
3. Each directory in `sys.path`, in order.

```python
import sys
for p in sys.path:
    print(p)
```

`sys.path[0]` is the directory of the script you ran (or the current directory
for `-m` and the REPL). **This is the source of the single most common
beginner-bites-expert bug in Python:**

```
project/
├── random.py       <- your file
└── app.py          <- does "import random"
```

`app.py` imports *your* `random.py`, not the standard library's, because the
script's directory comes first. Symptoms are bizarre: `AttributeError: module
'random' has no attribute 'choice'`. The same happens with `json.py`,
`string.py`, `email.py`, `types.py`, `test.py`, `queue.py`, `logging.py`.

Diagnose it in one line:

```python
import random
print(random.__file__)     # if this is in YOUR project, that's the bug
```

Fix: rename your file *and* delete the stale `__pycache__`.

---

## 6. Virtual environments, and why they are not optional

Without a virtual environment, every project on your machine shares one set of
installed packages. Project A needs `pydantic 1.x`, project B needs `2.x`. Only
one can win. That is the entire problem, and it is why the tooling exists.

A virtual environment is a directory containing:

- a symlink or copy of a Python interpreter,
- its own `site-packages` where installs land,
- an `activate` script that puts its `bin/` at the front of your `PATH`.

That is all it is. There is no magic and no global registry.

```bash
python3.12 -m venv .venv       # create
source .venv/bin/activate      # activate  (Windows: .venv\Scripts\activate)
which python                   # -> .../project/.venv/bin/python
pip install requests           # lands in .venv/lib/python3.12/site-packages
deactivate                     # leave
```

Prove to yourself where a package landed:

```python
import requests
print(requests.__file__)
```

### `uv`: the modern front end

`uv` (from Astral, the ruff people) is a drop-in replacement for `pip`,
`venv`, `pip-tools`, and `pyenv`, written in Rust. It is typically 10 to 100
times faster, and it resolves dependencies properly.

```bash
uv venv --python 3.12          # create an env, installing 3.12 if needed
uv pip install requests        # pip-compatible interface
uv pip compile requirements.in -o requirements.txt   # lockfile
uv run script.py               # run in the project env without activating
```

Both interfaces are in this course. Use `uv` day to day; understand `pip` and
`venv` because they are what exists on every machine and in every CI image.

### Pinning and lockfiles

```
requests            # "whatever version" -- irreproducible, avoid outside experiments
requests>=2.31      # a floor -- reasonable for a library you publish
requests==2.31.0    # exact -- correct for an application you deploy
```

The rule: **libraries specify ranges, applications pin exactly.** A library that
pins exactly makes itself uninstallable alongside anything else. An application
that does not pin will one day deploy a version you never tested. Module 30
covers the whole packaging model.

---

## 7. The REPL is a laboratory

You are going to spend a lot of time here. In a dynamically typed language, the
ability to interrogate a live object is the primary debugging tool, not a
fallback.

```python
>>> x = [1, 2, 3]
>>> type(x)              # what is it?
<class 'list'>
>>> len(dir(x))          # what can it do?
46
>>> [m for m in dir(x) if not m.startswith('_')]
['append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', ...]
>>> help(x.insert)       # how does it work?
>>> x.__class__.__mro__  # what is it, really?
(<class 'list'>, <class 'object'>)
>>> id(x)                # which object is it?  (Module 02)
```

Five habits worth forming today:

1. **Ask the object, do not search the web.** `dir()` and `help()` answer faster.
2. **`_` holds the last result.** `sum(_)` after computing a list saves retyping.
3. **`python -i script.py`** runs your script and then drops you into a REPL with
   all its variables still alive. Excellent for exploring a data structure you
   just built.
4. **`breakpoint()`** anywhere in your code drops into the debugger at that
   point. Module 18 goes deeper, but you can start using it today.
5. **Use ipython** for real work: history across sessions, `%timeit`, `%debug`,
   working tab completion.

---

## 8. Reading a traceback properly

You will read thousands of these. Read them **bottom-up**.

```
Traceback (most recent call last):
  File "/app/main.py", line 22, in <module>
    report(load("data.csv"))
  File "/app/report.py", line 9, in report
    avg = total / len(rows)
ZeroDivisionError: division by zero
```

| Line | What it tells you |
|---|---|
| Last line | The exception **type** and **message**. This is *what* went wrong. |
| Frame above it | The exact line that raised. This is *where*. |
| Frames above that | The call chain that got you there, outermost first. |

Two refinements that matter in real life:

**When the error is inside a library**, the last few frames are all library
code. Scan upward for the last frame that is *your* file. That is where your
mistake is; the library is usually just reporting it.

**When you see two tracebacks joined by text**, read the phrasing:

- `During handling of the above exception, another exception occurred` — you
  raised a new error *inside* an `except` block. Usually the second one is
  masking the first; the first is the real story.
- `The above exception was the direct cause of the following exception` — someone
  wrote `raise NewError(...) from original`. That is deliberate, good practice,
  and Module 16 teaches it.

---

## 9. Why "Python is slow" is an imprecise claim

Worth defusing now so you stop worrying about the wrong things.

Every bytecode operation carries interpreter overhead: unbox operands, dispatch
on type, box the result. A pure-Python numeric loop runs roughly 10 to 100 times
slower than the equivalent C. That is real.

But:

- Most programs are I/O-bound. Waiting on a network is the same speed in every
  language.
- The hot numeric libraries are not Python. `numpy` does its arithmetic in C
  over contiguous memory; a vectorised NumPy operation is within a small factor
  of hand-written C, and `pandas`, `scikit-learn`, `torch` are the same story.
- Algorithmic choices dominate interpreter overhead by orders of magnitude. An
  O(n) fix beats a 50x constant factor at any interesting n.
- CPython 3.11+ added a specialising adaptive interpreter that made typical code
  meaningfully faster, and the work continues.

The practical rule for this course, hammered again in Module 23: **never
optimise without a profile.** Your intuition about which line is slow is wrong
often enough that acting on it is a waste of a day.

---

## 10. The tools you will run every day

| Command | What it does | When |
|---|---|---|
| `ruff format .` | Formats your code | Before every commit |
| `ruff check . --fix` | Lints and autofixes | Before every commit |
| `mypy .` | Static type checking | Before every commit |
| `pytest -q` | Runs tests | Constantly |
| `python -m pdb app.py` | Debugger | When a print is not enough |
| `python -X importtime app.py` | Shows import cost per module | When startup is slow |
| `python -W error app.py` | Turns warnings into errors | When you want to find deprecations |
| `python -O app.py` | Strips `assert` statements | Never in this course; know it exists |

That last one is a real trap: `assert` disappears under `-O`. **Never use
`assert` for input validation or security checks** in production code. Use it
for internal invariants that should be impossible to violate. Raise a real
exception for anything else.

---

## Common mistakes in this module

| Mistake | Symptom | Fix |
|---|---|---|
| Naming a file `random.py`, `json.py`, `types.py` | Bizarre `AttributeError` from a stdlib module | Rename the file, delete `__pycache__`, check `mod.__file__` |
| Installing without an active venv | `ModuleNotFoundError` despite "installing it" | `which python` first; activate |
| `python pkg/mod.py` inside a package | `ImportError: attempted relative import with no known parent package` | `python -m pkg.mod` |
| Missing `if __name__ == "__main__":` | Importing the module runs the program | Add the guard |
| Committing `.venv/` or `__pycache__` | Bloated repo, broken on other machines | `.gitignore` (already provided) |
| Reading a traceback top-down | Chasing the wrong file | Read the last line first |
| `sudo pip install` | Broken system Python | Never. Use a venv. |
| Using `assert` to validate user input | Validation vanishes under `-O` | `if not ok: raise ValueError(...)` |
| Editing a module and re-importing in the same REPL | Old code still runs | `sys.modules` caches it; restart, or `importlib.reload` |

---

## Self-check quiz

Answer each in one or two sentences. If you cannot, re-read that section.

1. What is the difference between Python and CPython, and name two behaviours
   that belong to the implementation rather than the language.
2. Which errors are caught before your program runs, and which are not? Give an
   example of each.
3. What exactly is in `__pycache__`, when is it created, and what does it speed
   up?
4. What is `__name__` equal to when a file is run directly, and when it is
   imported?
5. What is `sys.path[0]`, and how does that produce the "I named my file
   `random.py`" bug?
6. What is a virtual environment, physically, on disk?
7. Why should an application pin exact versions while a library specifies
   ranges?
8. In a traceback, which line names the error, and which names the place it
   happened?
9. What is the difference between `python app.py` and `python -m app`?
10. Why is `assert` the wrong tool for validating user input?

---

## Exercises

Work in [`exercises/`](exercises/). Each file states its own goal. Attempt all
five before opening [`solutions/`](solutions/).

1. **[`ex01_pipeline.md`](exercises/ex01_pipeline.md)** — Not code. Observe the
   compile/run split, inspect bytecode with `dis`, and record what you saw.
2. **[`ex02_shadowing/`](exercises/ex02_shadowing/)** — A project that is broken
   by a shadowed stdlib module. Diagnose it from the traceback alone, then fix
   it, then explain the mechanism.
3. **[`ex03_name_main.py`](exercises/ex03_name_main.py)** — Make a file behave
   correctly both as an imported module and as a script.
4. **[`ex04_env_report.py`](exercises/ex04_env_report.py)** — Write a diagnostic
   tool that reports the interpreter, venv status, and import paths. You will
   reuse this whenever an environment misbehaves.
5. **[`ex05_traceback_triage.py`](exercises/ex05_traceback_triage.py)** — Five
   broken functions. For each: predict the exception before running, then run,
   then write down which frame was actually at fault.

---

## Going deeper (optional)

- [The `dis` module](https://docs.python.org/3/library/dis.html) — bytecode reference
- [The import system](https://docs.python.org/3/reference/import.html) — dense but definitive
- [`sys` module](https://docs.python.org/3/library/sys.html) — `path`, `modules`, `prefix`, `implementation`
- [PEP 405 — Virtual Environments](https://peps.python.org/pep-0405/) — what a venv actually is
- [uv documentation](https://docs.astral.sh/uv/)
- Talk: "Modern Python Developer's Toolkit" — a good survey of where the
  ecosystem landed after the 2023-2025 consolidation

---

**Next:** [Module 02 — Objects, Names, and the Data Model](../02-objects-names-data-model/README.md)
