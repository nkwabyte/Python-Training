# Solutions — Module 01

Read these **after** attempting the exercises. Where your answer differs, ask
whether yours is wrong or merely different.

---

## Exercise 01.1 — Watch the pipeline

### Part A

**A1.** Nothing. Not one character. The file never began executing.

**A2.** Tokenize/parse. Python compiles the entire file to bytecode *before*
executing any of it, so a syntax error anywhere in the file prevents the whole
file from running. This is the observation that kills the "Python reads your
code line by line" mental model, and it is worth remembering for that reason
alone.

**A3.** `b.py` prints both lines. `undefined_name` is a perfectly valid *name*;
the compiler has no obligation to know whether it will exist at runtime. It
compiles to a `LOAD_GLOBAL undefined_name` instruction and moves on. The error
only exists if that instruction actually executes.

The general principle: **syntax is checked statically, everything else
dynamically.** Names, types, attributes, arity — all runtime. That is why a
typo in a rarely-taken branch can survive to production, and why Modules 17 and
18 exist.

**A4.** Adding `f()` produces `NameError: name 'undefined_name' is not defined`
at execution time, after both prints have already appeared. Same file, same
text, different stage.

### Part B

**B1.** Constant folding. Both operands are compile-time constants, so the
compiler evaluates `1 + 2` during compilation and emits `LOAD_CONST 3`. The
addition does not exist at runtime. `x = a + b` cannot be folded, because the
compiler has no idea what `a` and `b` will be, so it emits real `LOAD_NAME` and
`BINARY_OP` instructions.

You can exploit this: expensive constant expressions written literally cost
nothing at runtime. You can also be misled by it when micro-benchmarking —
`timeit("1+2")` measures nothing at all.

**B2.** The `map`/`lambda` version does more work per element. The comprehension
compiles to a loop that calls `BINARY_OP` directly in its own frame. The
`map(lambda ...)` version must *call a Python function* for every element, and
a Python function call means building a frame, which is one of the more
expensive things the interpreter does. This is why comprehensions are usually
faster than `map` with a lambda, and why `map` with a *builtin* (`map(int, xs)`)
is competitive again — no Python-level call.

Note also that the comprehension's bytecode shows it has its own code object.
Comprehensions get their own scope; the loop variable does not leak. (In Python
2 it did. That change is why old blog posts about comprehensions mislead.)

**B3.** `LOAD_FAST` for the local, `LOAD_GLOBAL` for the global. `LOAD_FAST` is
faster: locals live in a fixed-size array on the frame and are accessed by
index, while globals require a dictionary lookup in the module namespace (and,
on failure, a second one in builtins).

This is the mechanism behind a real optimisation you will see in hot loops:

```python
def hot_loop(data):
    local_len = len          # bind the builtin to a local once
    return [local_len(x) for x in data]
```

Do not write that until a profiler tells you to (Module 23). But now you know
why it works.

### Part C

**C1.** `mymod.py` gets a `__pycache__` entry. `main.py` does not. Caching
happens on **import**, not on direct execution. The script you invoke is
compiled fresh each time, which is normally irrelevant because it is one file.

**C2.** The interpreter tag: `mymod.cpython-312.pyc`. Bytecode is not portable
across Python versions, so the version is encoded in the filename, letting 3.11
and 3.12 caches coexist in one directory without stepping on each other.

**C3.** Yes, automatically. By default the `.pyc` header stores the source's
last-modified time and size; if either differs, the cache is discarded and the
module is recompiled. (Python also supports hash-based `.pyc` files, PEP 552,
which are used when reproducible builds matter, since mtimes are not
reproducible.)

Genuine stale-cache problems are rare and almost always mean the filesystem is
lying about mtimes — containers with clock skew, some network mounts. If you
suspect it: `find . -name __pycache__ -exec rm -rf {} +`.

### Part D

**D1.** `sqlite3` is usually the most expensive of those three, since it loads a
C extension. The output is a *tree*: indented lines are imports triggered by
the line below them, and the two columns are self-time and cumulative-time in
microseconds. That distinction matters — a module can look expensive purely
because of what it imports.

**D2.** Import time is paid on **every process start**. A CLI tool that a user
runs 200 times a day pays it 200 times, and 400ms of import time is the
difference between a tool that feels instant and one that feels sluggish. A web
server pays it once at boot and then serves for weeks. This is why CLI tools do
lazy imports inside functions, and why `python -X importtime` is the first thing
to run when a CLI feels slow.

---

## Exercise 01.2 — The shadowing bug

### The traceback

```
AttributeError: module 'random' has no attribute 'randint'
```

This message is the tell. `AttributeError` on a *module* almost always means one
of two things: you misspelled the attribute, or you are not importing the module
you think you are. The message says "module 'random'", which is technically
true and completely misleading — it *is* a module named `random`, just not the
one in the standard library.

### The diagnosis

```python
>>> import random
>>> random.__file__
'/…/exercises/ex02_shadowing/random.py'     # <- not the stdlib
```

Every module object carries `__file__`. Printing it is the fastest possible
diagnosis and works for any suspicious import.

### Q1 — the mechanism

`sys.path[0]` is the directory of the script being run. It is searched **before**
the standard library directories. When `app.py` executes `import random`, Python
checks `sys.modules` (miss), checks built-in modules (miss — `random` is written
in Python, not compiled into the interpreter), then walks `sys.path` in order
and finds `./random.py` first.

Note the subtlety: modules that *are* compiled into the interpreter (`sys`,
`builtins`, `_thread`) cannot be shadowed this way, because they are resolved
before `sys.path` is consulted. That is why naming a file `sys.py` is annoying
but naming one `random.py` is catastrophic.

### Q2 — why the two errors differ

They differ only in the attribute named: `app.py` wants `randint`, `sampler.py`
wants `sample`. Same root cause, two symptoms. That is the lesson: a single
environment problem presents as several unrelated-looking errors, and if you
chase each symptom individually you will waste an afternoon. When two modules
fail in unrelated ways at the same time, suspect the environment before
suspecting the code.

### Q3 — the fixes

1. Rename `random.py` to something that is not a stdlib name — `sampling.py`,
   `rand_helpers.py`.
2. Update the imports that referenced it (in this project, none did — which is
   itself instructive: the file was never even used, and it still broke
   everything).
3. **Delete `__pycache__/`.** This is the step people miss. A stale
   `__pycache__/random.cpython-312.pyc` will still be found and imported even
   after you delete `random.py`, because the import system can load bytecode
   whose source no longer exists. You fix the bug, re-run, see the identical
   error, and conclude you were wrong about the cause.

### Q4 — other dangerous filenames

Any of `json.py`, `types.py`, `string.py`, `email.py`, `queue.py`, `logging.py`,
`select.py`, `code.py`, `test.py`, `copy.py`, `io.py`, `time.py`, `csv.py`,
`socket.py`, `token.py`, `abc.py`, `enum.py`, `secrets.py`, `platform.py`,
`operator.py`, `statistics.py`, `parser.py`.

`test.py` deserves special mention: it shadows the stdlib `test` package and
breaks pytest collection in ways that are genuinely hard to trace.

### Q5 — automatic detection

```bash
python - <<'EOF'
import sys, pathlib
bad = [p.name for p in pathlib.Path('.').glob('*.py') if p.stem in sys.stdlib_module_names]
print("shadowing:", bad or "none")
EOF
```

Or just run your Exercise 01.4 tool, which does exactly this and exits non-zero
so it can live in CI. `ruff` also has a rule for this (`A005`,
`builtin-module-shadowing`) which you can enable.

### Q6 — is `stats.py` a problem?

No. The stdlib module is `statistics`, not `stats`.

```python
>>> "stats" in sys.stdlib_module_names
False
>>> "statistics" in sys.stdlib_module_names
True
```

The implication: do not guess, check. The set is right there in the interpreter.
Two seconds of `in sys.stdlib_module_names` beats either paranoia or a lost
afternoon. In practice, the strongest protection is a `src/` layout with a
package directory (Module 06), because then your modules live under a package
namespace and cannot shadow anything.

---

## Exercise 01.3 — `__name__` and the import guard

See [`ex03_name_main_solution.py`](ex03_name_main_solution.py). The four ideas
worth extracting:

**1. Compute or perform I/O, not both.** `greet` returning a string instead of
printing it is the difference between `assert greet("Ada") == "Hello, Ada!"` and
a test that has to capture stdout. Push I/O to the edges of your program; keep
the middle pure. This principle scales all the way up: it is the same reason
Module 28's FastAPI handlers stay thin.

**2. Import must not have side effects.** A module that reads a file, opens a
socket, or reads an environment variable at import time is a module that cannot
be imported by a test, cannot be imported in a container where that file is
absent, and makes import *order* significant. Do the work in a function.

**3. `main(argv)` takes argv as a parameter.** Reading `sys.argv` inside `main`
couples it to global interpreter state. Taking it as an argument means a test
can call `main(["Ada"])` directly and assert on the return code. This tiny
choice is what makes CLIs testable, and it costs nothing.

**4. `raise SystemExit(main(...))` rather than `sys.exit(...)` or bare `main()`.**
Returning an exit code from `main` keeps the function pure and testable; the
guard is the only place that talks to the process. Note that `SystemExit`
inherits from `BaseException`, not `Exception`, specifically so that a
`except Exception:` block does not accidentally swallow your program's exit
(Module 16).

**Verification.** The real test is:

```bash
python -c "import ex03_name_main_solution"
```

If that produces any output beyond the deliberate `__name__` line, the guard is
in the wrong place.

---

## Exercise 01.4 — Environment diagnostic tool

See [`ex04_env_report_solution.py`](ex04_env_report_solution.py). Keep it and
use it.

Two things worth calling out:

**`sys.prefix != sys.base_prefix` is the definition of "in a venv."** It comes
straight from PEP 405. The `VIRTUAL_ENV` environment variable is set by the
`activate` *shell script*, which means it is absent whenever a tool invokes
`.venv/bin/python` directly — which is what tox, uv, CI runners, and your IDE
all do. Checking the variable gives false negatives in exactly the situations
where you most want an answer.

**`sys.stdlib_module_names` (3.10+) beats iterating `sys.modules`.** It contains
every stdlib module name for this interpreter, whether or not it has been
imported. `sys.modules` only shows what has already loaded, so it would miss
precisely the collision you have not triggered yet.

---

## Exercise 01.5 — Traceback triage

| Case | Exception | Frame that raised | Frame at fault |
|---|---|---|---|
| 1 | `ZeroDivisionError: division by zero` | `average`, the `/` | `case1` — it passed an empty list |
| 2 | `ValueError: not enough values to unpack (expected 3, got 2)` | `parse_row` | the *data*: row 2, `"grace,45"` |
| 3 | `KeyError: 'timeout'` | `get_setting` | `case3` — asked for a key that was never set |
| 4 | `TypeError: can't multiply sequence by non-int of type 'float'` | `total_price` | `case4` — a price is a string |
| 5 | `ConnectionError` ×2, chained | `fetch` | the retry strategy in `fetch_with_fallback` |

### Case 1 — the raising frame is not the faulty frame

`average` is correct code. It divides by `len(numbers)`, which is a reasonable
thing to do. The mistake is in the caller, which passed an empty list. This is
the central lesson of the exercise: **exceptions surface where the assumption
breaks, not where it was made.**

Two defensible fixes:

```python
def average(numbers: list[float]) -> float:
    if not numbers:
        raise ValueError("average() requires at least one value")   # fail loudly
    return sum(numbers) / len(numbers)
```

or return `float("nan")`, or make the empty case the caller's problem with a
documented precondition. The first is almost always right: an explicit
`ValueError` with a clear message beats a `ZeroDivisionError` that makes the
reader reconstruct what happened.

### Case 2 — the traceback does not tell you which row

This is the important one. You get `expected 3, got 2` and no indication of
*which* of the three rows was malformed. In a 4-million-line CSV that is a
genuinely bad afternoon.

Fix the code so the traceback carries the context:

```python
def parse_row(row: str, line_no: int) -> dict[str, str]:
    parts = row.split(",")
    if len(parts) != 3:
        raise ValueError(
            f"line {line_no}: expected 3 fields, got {len(parts)}: {row!r}"
        )
    name, age, city = parts
    return {"name": name, "age": age, "city": city}
```

Notice the `!r`. Using `repr` in error messages shows you quotes and whitespace,
which is exactly what you need when the bug is a trailing space or an empty
string. Make `!r` your default in exception messages.

The generalisable rule: **an exception message that does not identify the
offending input is half an exception message.** You will meet this again in
Module 16.

### Case 3 — two fixes, two meanings

```python
config.get(key)              # missing is FINE, you get None
config.get(key, default)     # missing is FINE, you get a sensible value
config[key]                  # missing is a BUG, and should crash
```

Choose based on whether a missing key is an expected state or a programming
error. Reaching for `.get()` reflexively is a common way to convert a loud bug
into a silent `None` that fails three functions later with a much worse
traceback.

### Case 4 — types that are wrong long before they fail

`"19.99" * 1` is valid Python — string repetition — so the failure is deferred
until `sum` tries to add a string to a float. The mistake happened when form
data was stored without conversion, possibly in a completely different module,
possibly hours earlier in wall-clock time.

This is the canonical argument for Module 17. A type checker flags
`dict[str, object]` arithmetic immediately, at the place the wrong value was
introduced, instead of three layers away at runtime. It is also the argument for
Module 28's Pydantic models: validate and convert **at the boundary**, so that
everything inside your program can trust its types.

### Case 5 — reading a chained traceback

The output contains two tracebacks joined by:

```
During handling of the above exception, another exception occurred:
```

That sentence means: an exception was raised *inside an `except` block*. Python
shows both because losing the first one would hide the original cause.

Compare with the other phrasing:

| Message | Meaning | How it arose |
|---|---|---|
| `During handling of the above exception, another exception occurred` | Implicit chaining. Usually accidental. | Raising inside `except` without `from` |
| `The above exception was the direct cause of the following exception` | Explicit chaining. Deliberate. | `raise NewError(...) from original` |

For someone debugging case 5, the **first** exception is the real story: the
host does not resolve. The second is just the fallback failing the same way. A
better implementation would not blindly retry:

```python
def fetch_with_fallback(url: str) -> str:
    try:
        return fetch(url)
    except ConnectionError as exc:
        fallback = url.replace("https://", "http://", 1)
        if fallback == url:
            raise
        try:
            return fetch(fallback)
        except ConnectionError as fallback_exc:
            raise ConnectionError(
                f"both {url} and {fallback} are unreachable"
            ) from exc          # <- point at the ORIGINAL cause
```

Note `from exc`, not `from fallback_exc`. You want the traceback to lead a
reader to the root problem, not to the symptom. Module 16 makes this systematic.
