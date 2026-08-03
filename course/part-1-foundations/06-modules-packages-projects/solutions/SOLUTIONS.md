# Solutions — Module 06

---

## Exercise 06.1 — Five import failures

### Case 1 — running a package module directly

```
ImportError: attempted relative import with no known parent package
```

**Q1a.** `__package__` is `''` (empty). When you run a file directly, Python
sets `__name__` to `"__main__"` and `__package__` to `""`. A relative import
means "relative to my package", and there is no package, so there is nothing for
the leading dot to resolve against.

**Q1b.**

```bash
python -m mypkg.core          # works
```

Two things change. `sys.path[0]` becomes the current working directory instead
of `mypkg/`, so `mypkg` itself is importable. And `__package__` becomes
`"mypkg"`, giving the leading dot something to resolve against.

**Q1c.** `python mypkg/util.py` **works**, because `util.py` uses an absolute
import (in fact, none at all). The absolute form does not depend on
`__package__`. This is the practical argument for preferring absolute imports:
the file behaves the same however it is reached.

### Case 2 — the module that is not there

**Q2a.** From `/tmp`, `sys.path[0]` is `/tmp`, which does not contain `mypkg`.
From the exercise directory it does. `sys.path[0]` is the current directory for
`-c`, `-m`, and the REPL.

**Q2b.** Either install it (`pip install -e .` with a `pyproject.toml`, which is
the real fix and works from anywhere), or run from a directory that contains it.
Not `PYTHONPATH`, and definitely not `sys.path.insert` — both are per-shell
plasters that fail for the next person and in CI.

### Case 3 — the import that runs code

**Q3a.** `import mypkg.slow_init` printed two lines and slept for 1.5 seconds.
Importing a module executed its top-level statements, and those statements did
I/O.

**Q3b.** For a test suite this is fatal in three ways. Collection alone (pytest
imports every test module and everything they import) pays the cost, multiplied
by the number of modules. Tests cannot run at all in an environment without the
database. And test *ordering* becomes significant, because the connection is
created by whichever import happens first.

**Q3c.** Move the work into a function, called explicitly:

```python
_connection = None

def get_connection():
    global _connection            # a lazy singleton; acceptable here
    if _connection is None:
        _connection = connect()
    return _connection
```

**The general rule: importing a module must have no side effects.** No I/O, no
network, no environment reads, no logging configuration, no global mutation.
Define things; do not do things.

### Case 4 — the stale name

```
module attribute: True
imported name:    False
```

**Q4a.** `from mypkg.settings import DEBUG` copies the *current value* of the
attribute into a new name in your namespace. It is `DEBUG = mypkg.settings.DEBUG`
at import time. Rebinding `mypkg.settings.DEBUG` later changes the module's
attribute, not your copy — they were never linked.

**Q4b.** Use `import mypkg.settings` and read `settings.DEBUG` at the point of
use, so the attribute is fetched when you need it.

This matters enormously for testing. `unittest.mock.patch` works by
**temporarily replacing an attribute on an object**. So:

```python
# your_module.py
from time import time              # copied a reference to the function

# test
patch("time.time")                 # patches the time module's attribute
                                   # -> your_module.time is UNAFFECTED
patch("your_module.time")          # patches YOUR module's attribute -> works
```

The rule of thumb, which will save you an hour eventually: **patch where the
name is used, not where it is defined.** Module 18 covers this properly.

### Case 5 — the missing `__init__.py`

**Q5a.** `broken1` is a **namespace package** (PEP 420, since 3.3). A directory
without `__init__.py` is still importable; namespace packages exist so a single
package name can be split across multiple distributions and directories.

**Q5b.** Test discovery gets confusing. Without `__init__.py`, pytest uses
rootdir-based module naming, and two test files with the same basename in
different directories collide with an "import file mismatch" error that gives no
hint about the real cause.

**Q5c.** Because you almost never *want* a namespace package, and getting one by
accident produces failures that look unrelated to their cause. Add
`__init__.py` unless you are deliberately building a split-distribution plugin
namespace. The cost is one empty file; the benefit is that a whole class of
confusing error cannot occur.

---

## Exercise 06.2 — The circular import

### Task 1 — the cycle

```
order.py  ──imports──>  pricing.py  ──imports──>  customer.py  ──imports──>  order.py
   ^                                                                            │
   └────────────────────────────────────────────────────────────────────────────┘
```

The failing line is `from shop.customer import Customer` in `pricing.py`. At
that moment `sys.modules` contains:

- `shop.customer` — **partially initialised**. Its body started, reached
  `from shop.order import Order`, and has not yet defined `Customer`.
- `shop.order` — partially initialised, blocked on importing `pricing`.
- `shop.pricing` — partially initialised, executing this very line.

`shop.customer` is found in `sys.modules`, so it is not re-executed. The
attribute `Customer` is read from it. The attribute does not exist yet. That is
the error, and it is a **timing** problem, not a "these two files need each
other" problem.

### Task 2 — the four fixes

See [`ex02_circular_fixed/`](ex02_circular_fixed/) for the implemented version.

**A. Extract the shared piece** — `models.py` holds `Customer` and `Order` and
imports nothing from `shop`. The cycle disappears because the new module sits at
the *bottom* of the dependency graph. That is the test of a correct extraction:
if your new module still imports from the package, you have added a node to the
cycle rather than broken it.

**B. Import inside a function** — `Order.total()` imports `pricing` at call
time, when everything is loaded. Legitimate, and used once here with a comment
explaining why. It hides a dependency from the top of the file, so it should be
rare and always annotated.

**C. Import the module, not the name** — `import shop.customer` then
`shop.customer.Customer` at use time. Works because the attribute is read later.
Least intrusive; also the least informative about *why* the code is written that
way, so it tends to be silently broken by a future refactor.

**D. `if TYPE_CHECKING`** — used in `pricing.py`, where `Customer` is needed only
as an annotation. With `from __future__ import annotations`, annotations are
strings and never evaluated, so the runtime import vanishes entirely.

**D alone is not sufficient here**, and noticing that is the point of the
question. `customer.py` does not merely annotate with `Order` — `pricing.py`
*calls* `customer.discount_rate()`. That is a genuine runtime dependency, so no
amount of typing-only trickery removes it. **`TYPE_CHECKING` fixes typing
cycles; a runtime cycle needs a structural fix.** When `TYPE_CHECKING` does not
solve your cycle, that is a signal your modules have real behavioural coupling
and A is the answer.

### Task 3 — which fix

**A, the extraction.** It reads best (a new reader sees a plain dependency
graph), it survives new modules (anything else can depend on `models` freely),
it hides nothing, and — the real point — **the cycle was telling you the design
had a missing module.** Three modules all needed each other because the data
definitions were tangled with the behaviour. Separating "what things are" from
"what we do to them" is a good decomposition independent of the import problem.
The cycle was a symptom; A treats the cause.

### Task 4 — the regression test

See [`ex02_circular_fixed/test_no_cycle.py`](ex02_circular_fixed/test_no_cycle.py).
It imports each module **first, in a fresh subprocess**. This matters: a cycle
often survives in a test suite because some earlier test already imported the
modules in the lucky order and left them in `sys.modules`. Only a fresh
interpreter proves it is really gone. This test has caught reintroduced cycles in
real codebases.

---

## Exercise 06.3 — Script to package

No single solution file — the target structure is in the exercise README. The
five things that separate a good conversion from a mechanical one:

**Removing import-time I/O changes function signatures.** The original reads the
database into a global `DB` at import. The fix is not "move it into a function"
alone; it is passing the store explicitly, so that
`add(store, url, ...)` can be tested against a temporary file or an in-memory
fake. Global state removed at the top reappears as a parameter, and that is the
trade you want.

**The CLI/logic boundary was not obvious in the original.** `add()` validates,
mutates, saves, prints, *and* calls `sys.exit()`. Five responsibilities. In the
package version: `models.py` validates, `storage.py` saves, `search.py` queries,
`cli.py` prints and chooses the exit code. The test for whether you drew the line
correctly: **no module outside `cli.py` may import `sys` or call `print`.**

**Atomic writes.** The original truncates the user's data if the process dies
mid-write. The fix is write-to-temp-then-rename, since `os.replace` is atomic on
the same filesystem:

```python
tmp = path.with_suffix(".tmp")
tmp.write_text(json.dumps(data), encoding="utf-8")
tmp.replace(path)                 # atomic
```

**Under the flat layout, a forgotten module fails only for the user.** Tests
import from the project root, which is on `sys.path`, so they find the source
whether or not it was packaged. Under `src/`, only the installed package is
importable, so the failure happens in your own test run.

**Exit codes are an API.** 0 success, 1 general failure, 2 usage error is the
convention (`argparse` already uses 2). Scripts and CI pipelines branch on
these; returning 0 on failure is a silent breakage in someone's automation.

---

## Exercise 06.4 — Layered settings

See [`ex04_settings_solution.py`](ex04_settings_solution.py).

**`parse_bool` is the single most expensive line in twelve-factor config.**
Environment variables are always strings, and every non-empty string is truthy:

```python
DEBUG=false  →  os.environ["DEBUG"] == "false"  →  bool("false") is True
```

The operator sets `DEBUG=false` and debug mode turns **on**, in production, with
stack traces going to users. Raising on unrecognised input rather than
defaulting to `False` is deliberate — `DEBUG=maybe` is a typo, and silently
picking an interpretation means the same incident recurs with a different
spelling.

**Collect all errors, then raise once.** A person fixing configuration in a
container gets one error per restart otherwise, and each restart is a deploy.
Three of them is an afternoon. The solution's output:

```
invalid configuration:
  - APP_DEBUG='maybe': cannot interpret 'maybe' as a boolean. Use one of: ...
  - database_url is required. Set APP_DATABASE_URL, or add database_url ...
  - port must be between 1 and 65535, got 0
  - log_level must be one of ['DEBUG', 'ERROR', 'INFO', 'WARN', 'WARNING'] ...
```

That is what a good configuration error looks like: what is wrong, what the
value was, and what to do instead.

**`env` as a parameter, not `os.environ` read inside.** The same lesson as
`main(argv)` in Module 01. `os.environ` is global mutable state shared by every
test in the process; a test that mutates it and fails before cleanup poisons
every later test.

**`allowed_hosts` is a tuple, not a list.** `frozen=True` prevents *rebinding*
an attribute; it does not stop you mutating what the attribute points at. A
frozen dataclass holding a list is still mutable through that list, and it is
also unhashable. Module 02's tuple trap, applied to a design decision.

**Redaction parses the URL rather than regex-replacing likely secrets.** Masking
the password *component* works for every scheme and cannot be defeated by an
unusual character in the password. Connection strings in logs are one of the
most common real credential leaks, because logs are shipped to an aggregator
whose access policy is not the database's.

**Note on `tomllib`:** it is stdlib from 3.11 and requires the file be opened in
**binary** mode. On 3.10 and older, `tomli` is the same library under its old
name; the solution includes the conditional import.
