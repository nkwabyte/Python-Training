# Setup

Get this right once and it will stay out of your way for twenty weeks. Budget
about an hour. The single most common reason people bounce off Python is not
the language, it is a broken environment producing errors that look like
language errors.

Target: **Python 3.12 or 3.13**. Everything in this course runs on 3.12. Where a
feature needs 3.13, the README flags it. Where a 3.10/3.11 fallback exists, it
is noted.

---

## 1. The mental model you need before installing anything

Three things get confused constantly. Keep them separate in your head:

| Thing | What it is | Where it lives |
|---|---|---|
| **The interpreter** | The `python3` binary that executes bytecode | System-wide, one per installed version |
| **The environment** | A directory holding a specific set of installed packages | Per project (`.venv/`) |
| **The package manager** | The tool that puts packages into an environment | `pip`, or `uv` |

Almost every "it works on my machine" problem in Python is one of these three
being different from what you assumed. The fix is always the same: make the
environment explicit and per-project.

---

## 2. Install Python

### macOS

Do **not** use the `/usr/bin/python3` that ships with macOS. It exists for the
operating system, not for you, and installing into it can break system tools.

```bash
# Homebrew (if you do not have it: https://brew.sh)
brew install python@3.12

# verify
python3.12 --version    # Python 3.12.x
```

Better still, install `uv`, which can manage interpreters *and* environments:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.12
uv python list
```

### Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3-pip
python3.12 --version
```

If your distro is older than 3.12, use `uv python install 3.12` or the deadsnakes
PPA rather than compiling from source.

### Windows

Use the official installer from [python.org](https://www.python.org/downloads/),
and **tick "Add python.exe to PATH"** on the first screen. Then use PowerShell,
not cmd.exe, for everything in this course. Or install `uv`:

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
uv python install 3.12
```

WSL2 is also an excellent option and makes every Linux instruction in this
course apply directly.

---

## 3. Set up this course's environment

From the root of this folder:

### Option A — `uv` (recommended, 10-100x faster)

```bash
uv venv --python 3.12          # creates .venv/
source .venv/bin/activate      # Windows: .venv\Scripts\activate
uv pip install -r requirements-dev.txt
```

### Option B — stdlib `venv` + `pip`

```bash
python3.12 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

### Verify

```bash
which python                   # must point INSIDE .venv
python --version               # 3.12.x
python -c "import sys; print(sys.prefix)"
```

If `which python` does not point inside `.venv`, the activation did not take.
Nothing else will work correctly until it does.

**The rule you must internalise:** if you are about to type `pip install` and
you have not activated an environment, stop. Every dependency problem you will
ever have starts there.

---

## 4. The tools, and why each one earns its place

`requirements-dev.txt` in this folder installs the following. This is a
deliberately small set; Python tooling has consolidated hard in recent years.

| Tool | Replaces | Why |
|---|---|---|
| **ruff** | flake8, isort, pylint, black | Linter and formatter in one, written in Rust, effectively instant |
| **mypy** | — | Static type checker. Your compiler substitute. |
| **pytest** | unittest | The testing framework everyone actually uses |
| **pytest-cov** | — | Coverage reporting |
| **hypothesis** | — | Property-based testing (Module 18) |
| **ipython** | the plain REPL | A REPL with history, `?`, `%timeit`, and tab completion that works |
| **rich** | — | Readable tracebacks and terminal output; used in later modules |

Later parts add their own dependencies (`httpx`, `fastapi`, `sqlalchemy`,
`numpy`, `pandas`, `scikit-learn`). Each module's README installs what it needs,
so you are never carrying dependencies you have not been taught.

### Configure them

The repository root has a `pyproject.toml` with ruff and mypy already
configured. The settings that matter:

```toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "C4", "RET", "PTH"]
# E/F  pycodestyle + pyflakes: the basics
# I    import sorting
# UP   pyupgrade: rewrites old idioms to modern ones as you learn them
# B    bugbear: catches the mutable-default-argument trap automatically
# SIM  simplification suggestions
# C4   comprehension improvements
# RET  return-statement hygiene
# PTH  nudges os.path -> pathlib

[tool.mypy]
python_version = "3.12"
strict = true                # start strict; you will learn faster
warn_unreachable = true
```

Starting mypy in `strict` mode is a deliberate teaching choice. It will be
annoying in week two and invaluable by week ten. If a specific exercise makes it
unbearable, relax it per-file with a comment rather than globally.

### Daily commands

```bash
ruff format .          # format
ruff check . --fix     # lint and autofix
mypy .                 # type check
pytest -q              # run tests
pytest --cov -q        # tests with coverage
```

Get these into muscle memory. Run them before you look at a solution file.

---

## 5. Editor setup

### VS Code

Install these extensions:

- **Python** (Microsoft) — the base
- **Pylance** — fast type-aware IntelliSense
- **Ruff** (Astral) — inline lint and format

Then in `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.analysis.typeCheckingMode": "basic",
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "charliermarsh.ruff",
  "editor.codeActionsOnSave": { "source.organizeImports": "explicit" },
  "python.testing.pytestEnabled": true
}
```

**Select the interpreter explicitly**: Command Palette → "Python: Select
Interpreter" → pick the one inside `.venv`. If your editor is using a different
interpreter than your terminal, you will see imports that work in one place and
fail in the other, and you will lose an hour to it.

### PyCharm

Settings → Project → Python Interpreter → Add → Existing environment → point at
`.venv/bin/python`. Enable ruff as an external tool or via the plugin.

### Neovim / other

Use `pyright` and `ruff` through your LSP client. `basedpyright` is a good
alternative to pyright with saner defaults.

---

## 6. Verify the whole chain

Create `setup/verify.py` (it is already in this folder) and run it:

```bash
python setup/verify.py
```

It checks: interpreter version, that you are inside a virtual environment, that
each tool imports, and that a small typed, tested example passes all three
tools. If it prints `ALL CHECKS PASSED`, you are ready for Module 01.

---

## 7. The REPL is a laboratory, not a toy

You will use it constantly in this course. Make it good.

```bash
ipython
```

The five things worth knowing on day one:

```python
obj?              # docstring and type
obj??             # source code, if available
%timeit expr      # benchmark an expression properly
%debug            # post-mortem debugger on the last traceback
_                 # the previous result
```

In the plain REPL, the equivalents are `help(obj)`, `type(obj)`, `dir(obj)`, and
`import pdb; pdb.pm()`.

**A habit worth forming now:** when you are unsure what something does, do not
search for it. Open the REPL and ask the object. `type(x)`, `dir(x)`,
`help(type(x).method)`, `x.__class__.__mro__`. Python is unusually
introspectable, and the person who uses that is much faster than the person who
searches.

---

## 8. Reading a traceback

You will read thousands of these. Two minutes now saves hours later.

```
Traceback (most recent call last):
  File "app.py", line 12, in <module>       <- where it started
    main()
  File "app.py", line 8, in main            <- the call chain, outermost first
    total = compute(values)
  File "app.py", line 4, in compute         <- where it actually blew up
    return sum(v / count for v in values)
ZeroDivisionError: division by zero          <- WHAT went wrong
```

Read it **bottom to top**:

1. **Last line**: the exception type and message. That is *what* happened.
2. **Second-to-last frame**: the line that raised. That is *where*.
3. **Frames above**: how you got there. Skim these for the first frame that is
   *your* code if the error is deep inside a library.

The most common mistake is reading top-down and stopping at the first file name,
which is usually the least relevant frame.

Install `rich` (already in `requirements-dev.txt`) and add this to a script to
get tracebacks with local variables shown at each frame:

```python
from rich.traceback import install
install(show_locals=True)
```

---

## 9. Common setup problems and their fixes

| Symptom | Cause | Fix |
|---|---|---|
| `command not found: python` | Only `python3` exists | Use `python3`, or activate a venv where `python` is defined |
| `ModuleNotFoundError` for something you installed | Installed into a different environment | `which python`, `pip list`, reactivate |
| Import works in terminal, fails in editor | Editor using a different interpreter | Select the `.venv` interpreter in your editor |
| `pip install` fails with "externally managed environment" | You are trying to install into system Python | Create and activate a venv. Do not use `--break-system-packages`. |
| `ImportError: attempted relative import with no known parent package` | Ran a package file as a script | `python -m package.module` instead of `python package/module.py` (Module 06) |
| Your file is named `random.py`/`json.py` and imports break | Your module shadows a stdlib module | Rename your file, delete `__pycache__` |
| `SyntaxError` on a modern feature | Old interpreter | `python --version`; you need 3.12 |
| Everything is slow on `pip install` | pip's resolver | Use `uv pip install` |

---

## 10. A note on `python` vs `python3`

Inside an activated virtual environment, `python` is correct and unambiguous —
it is the venv's interpreter. Outside one, `python` may not exist or may be
Python 2 on very old systems. This course assumes you are always inside an
activated environment, so it writes `python`.

If you ever find yourself typing `sudo pip install`, stop and re-read section 3.
There is no situation in this course where that is the right command.

---

## Ready

```bash
python setup/verify.py
```

Then open
[`course/02-intermediate/part-1-foundations/01-runtime-and-toolchain/README.md`](course/02-intermediate/part-1-foundations/01-runtime-and-toolchain/README.md).
