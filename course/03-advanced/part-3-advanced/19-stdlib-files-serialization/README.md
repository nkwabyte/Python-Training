# Module 19 — The Standard Library, Files, and Serialization

**Time budget:** 5 hours lesson, 7 hours exercises
**Prerequisite:** Modules 03 (encodings), 16

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

Python's standard library is its best feature. Most of what you would reach for
a dependency to do is already installed, tested by millions of users, and will
still work in ten years. This module is a working tour of the parts you will use
weekly, with the traps that make each one interesting.

---

## 1. `pathlib`

Use `Path` everywhere. `os.path` is string manipulation pretending to be file
handling.

```python
from pathlib import Path

p = Path("data") / "raw" / "input.csv"     # / is the join operator
p.name          # 'input.csv'
p.stem          # 'input'
p.suffix        # '.csv'
p.suffixes      # ['.csv']   -- ['.tar', '.gz'] for archive.tar.gz
p.parent        # Path('data/raw')
p.parents       # all ancestors, lazily
p.absolute()    # not resolved -- may contain '..'
p.resolve()     # canonical: symlinks followed, '..' removed
p.exists() / .is_file() / .is_dir() / .is_symlink()
p.stat().st_size / .st_mtime

p.read_text(encoding="utf-8")              # always name the encoding
p.write_text(data, encoding="utf-8")
p.read_bytes() / p.write_bytes(b"...")

p.mkdir(parents=True, exist_ok=True)       # both flags, almost always
p.unlink(missing_ok=True)
p.rename(other) / p.replace(other)         # replace OVERWRITES, rename may not
list(p.glob("*.csv")) / list(p.rglob("*.py"))
Path.home() / Path.cwd()
```

**`resolve()` versus `absolute()` matters for security.** A user-supplied path
like `../../etc/passwd` is only visible after resolution:

```python
target = (base / user_input).resolve()
if not target.is_relative_to(base.resolve()):    # 3.9+
    raise ValueError("path escapes the base directory")
```

That check is the difference between a file server and a directory traversal
vulnerability.

### Atomic writes, again

```python
tmp = path.with_suffix(path.suffix + ".tmp")     # SAME directory
tmp.write_text(data, encoding="utf-8")
tmp.replace(path)                                 # atomic within a filesystem
```

Module 07 covered this; it belongs in your fingers.

---

## 2. Files and I/O

```python
with path.open("r", encoding="utf-8", newline="") as fh: ...
with path.open("rb") as fh: ...             # binary: no encoding, no newline
```

| Mode | Meaning |
|---|---|
| `r` `w` `a` | read, truncate-and-write, append |
| `x` | create, fail if it exists — the safe way to avoid clobbering |
| `+` | read *and* write |
| `b` | binary |

Three things worth knowing:

**`newline=""` for the `csv` module.** Without it, `\r\n` inside a quoted field
is translated and the file is corrupted. The `csv` docs say this and everyone
skips it.

**Iterating a file yields lines lazily.** `for line in fh:` reads a buffer at a
time, so it works on a file larger than memory. `fh.readlines()` does not.

**Text mode does newline translation and encoding.** Binary mode does neither.
If you are computing a hash, comparing bytes, or handling anything non-text, use
binary.

```python
import shutil, tempfile, os

shutil.copy2(src, dst)              # copies metadata too
shutil.move(src, dst)
shutil.rmtree(path)
shutil.disk_usage(path)

with tempfile.TemporaryDirectory() as td: ...       # cleaned up always
with tempfile.NamedTemporaryFile(delete=False) as f: ...
```

---

## 3. `json`

```python
import json

json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False, default=str)
json.loads(text)
json.dump(obj, fh)      # to a file
json.load(fh)
```

**What JSON cannot represent, and what Python does about it:**

| Python | JSON | Round trip? |
|---|---|---|
| `dict` with str keys | object | yes |
| `dict` with int keys | object with **str** keys | **no** — `{1: "a"}` comes back `{"1": "a"}` |
| `tuple` | array | **no** — comes back as a `list` |
| `set`, `bytes`, `Decimal`, `datetime` | — | **no** — `TypeError` unless handled |
| `float('nan')`, `inf` | not valid JSON | Python emits `NaN` anyway, which other parsers reject |
| large `int` | number | yes, but many parsers lose precision above 2⁵³ |

```python
class Encoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return str(obj)             # str, NOT float -- Module 03
        if isinstance(obj, set):
            return sorted(obj)
        return super().default(obj)
```

**`ensure_ascii=False`** keeps non-ASCII readable (`"café"` rather than
`"café"`) and produces smaller output. **`sort_keys=True`** makes output
deterministic, which matters for diffs, caching and content hashing.

---

## 4. `csv`

```python
import csv

with path.open(newline="", encoding="utf-8") as fh:
    for row in csv.DictReader(fh):
        print(row["name"])

with path.open("w", newline="", encoding="utf-8") as fh:
    writer = csv.DictWriter(fh, fieldnames=["name", "qty"])
    writer.writeheader()
    writer.writerows(rows)
```

**Never parse CSV with `str.split(",")`.** Fields legitimately contain commas,
quotes, and newlines. Every hand-rolled parser is correct until the first
product name with a comma in it — which is about week two of production.

Real-world CSV needs: `csv.Sniffer` for unknown dialects, `utf-8-sig` for files
Excel produced (it writes a BOM), and awareness that Excel will happily turn
`SKU-001` into a date.

---

## 5. `sqlite3`

A full SQL database, in the standard library, with no server.

```python
import sqlite3

with sqlite3.connect("app.db") as conn:      # NOTE: commits, does NOT close
    conn.row_factory = sqlite3.Row           # dict-like rows
    conn.execute("PRAGMA foreign_keys = ON") # OFF by default!
    cur = conn.execute("SELECT * FROM users WHERE age > ?", (18,))
    for row in cur:
        print(row["name"])
```

**Always use parameters, never string formatting.**

```python
conn.execute(f"SELECT * FROM users WHERE name = '{name}'")   # SQL INJECTION
conn.execute("SELECT * FROM users WHERE name = ?", (name,))  # correct
```

This is not a style preference. `name = "'; DROP TABLE users; --"` is the entire
attack, and parameterisation makes it structurally impossible because the value
never becomes part of the statement.

Two sqlite-specific traps: `with conn:` is a **transaction** context manager,
not a closing one — it commits or rolls back and leaves the connection open.
And foreign key enforcement is **off** by default, so your constraints do
nothing until you turn the pragma on.

---

## 6. `pickle`, and why not to use it

```python
import pickle
pickle.dumps(obj); pickle.loads(data)
```

**Unpickling data executes arbitrary code.** A malicious payload runs whatever
it likes with your process's privileges. There is no safe way to unpickle
untrusted input — no validation, no sandbox, no "safe mode".

| Use pickle for | Never for |
|---|---|
| A cache you produced, on your own machine | Anything from a user or a network |
| `multiprocessing` (which uses it internally) | Long-term storage |
| A short-lived checkpoint | Anything another language must read |

It is also fragile across versions: pickling an instance stores a reference to
its class, so renaming or moving that class breaks every existing pickle.

For data, use JSON. For configuration, TOML. For a schema and speed, Protocol
Buffers, MessagePack or Arrow.

```python
import tomllib                         # 3.11+, READ ONLY
with path.open("rb") as fh:            # BINARY mode, always
    config = tomllib.load(fh)
```

---

## 7. `datetime`, and the one rule

```python
from datetime import datetime, date, timedelta, timezone, UTC
from zoneinfo import ZoneInfo          # 3.9+, real tz database

datetime.now(UTC)                       # aware. Correct.
datetime.now()                          # NAIVE. Almost always a bug.
datetime.now(ZoneInfo("Europe/London")) # aware, with DST handled
```

**Store and compute in UTC; convert to local time only for display.** A naive
datetime has no timezone, so comparing two of them from different sources is
meaningless, and arithmetic across a DST boundary is wrong.

```python
dt.isoformat()                          # '2026-08-03T12:00:00+00:00'
datetime.fromisoformat(text)            # 3.11+ parses almost anything ISO
dt.astimezone(ZoneInfo("Asia/Tokyo"))
dt.timestamp()                          # seconds since the epoch, UTC
```

Two things people get wrong:

**`timedelta` arithmetic is exact, calendar arithmetic is not.** Adding
`timedelta(days=30)` is 30×86400 seconds, which is not "one month" and is not
even 30 days across a DST change. For calendar months use
`dateutil.relativedelta`.

**`time.time()` for measuring intervals is wrong.** It is wall-clock and can
jump backwards (NTP, DST, a manual change). Use `time.perf_counter()` for
durations and `time.monotonic()` for timeouts.

---

## 8. `re`, at working depth

```python
import re

pattern = re.compile(r"(?P<user>\w+)@(?P<domain>[\w.]+)")   # compile once
m = pattern.search(text)
if m:
    m.group("user"), m["domain"], m.span()

pattern.findall(text)         # a list of strings or tuples
pattern.finditer(text)        # LAZY, and gives match objects -- prefer this
pattern.sub(r"\g<user> AT \g<domain>", text)
pattern.split(text)
```

| Want | Use |
|---|---|
| Non-greedy | `.*?` |
| Multiline `^`/`$` | `re.MULTILINE` |
| `.` matches newline | `re.DOTALL` |
| Readable pattern with comments | `re.VERBOSE` |
| A group that does not capture | `(?:...)` |
| Zero-width assertion | `(?=...)`, `(?!...)`, `(?<=...)` |

**Always use a raw string.** `"\d"` is a deprecation warning today and an error
tomorrow; `r"\d"` is correct.

**Do not parse HTML, XML or JSON with regex.** They are not regular languages.
Use `selectolax`/`BeautifulSoup`, `xml.etree`, and `json`.

**Catastrophic backtracking is real.** A pattern like `(a+)+b` against a long
string of `a`s takes exponential time — a denial-of-service vector known as
ReDoS. Avoid nested quantifiers over overlapping character classes, and never
build a pattern from untrusted input.

---

## 9. `subprocess`, safely

```python
import subprocess

result = subprocess.run(
    ["git", "log", "--oneline", "-n", "10"],   # a LIST, never a string
    capture_output=True, text=True, check=True, timeout=30, cwd=repo,
)
result.stdout
```

**Never use `shell=True` with anything user-supplied.**
`subprocess.run(f"grep {query} file", shell=True)` with
`query = "; rm -rf ~"` does exactly what it looks like. A list of arguments
bypasses the shell entirely, so quoting and injection cannot occur.

`check=True` raises on a non-zero exit — without it, failures are silent.
`timeout=` prevents a hang. Both should be habitual.

---

## 10. The rest, in one table

| Module | For | Note |
|---|---|---|
| `argparse` | CLI parsing | In the stdlib; Typer/Click are nicer |
| `logging` | Logs | Module 16 |
| `collections` | Containers | Module 05 |
| `itertools` | Lazy tools | Module 14 |
| `functools` | Function tools | Module 15 |
| `dataclasses` | Records | Module 11 |
| `enum` | Enumerations | Module 11 |
| `typing` | Hints | Module 17 |
| `secrets` | Tokens, keys | **Never `random`** for anything security-related |
| `hashlib` | Digests | `sha256`; and `scrypt`/`pbkdf2_hmac` for passwords, never plain sha256 |
| `hmac` | `compare_digest` | Constant-time comparison — use it for tokens |
| `uuid` | Ids | `uuid4` for random |
| `textwrap` | Wrapping, `dedent` | `dedent` is excellent for embedded text |
| `difflib` | Diffs, fuzzy matching | `get_close_matches` for "did you mean" |
| `statistics` | mean, median, stdev | Exact, unlike naive formulae |
| `zipfile` / `tarfile` | Archives | Beware path traversal in untrusted archives |
| `struct` | Binary layouts | For protocols and file formats |
| `shlex` | Shell-style splitting | `shlex.quote` if you truly must build a command |
| `platform` / `sys` | Environment | |
| `time` | `perf_counter`, `monotonic` | Not `time()` for intervals |

---

## Common mistakes in this module

| Mistake | Symptom | Fix |
|---|---|---|
| `open()` with no encoding | Works locally, breaks elsewhere | `encoding="utf-8"` |
| `csv` without `newline=""` | Corrupted rows with embedded newlines | Pass it |
| `str.split(",")` for CSV | Breaks on quoted commas | The `csv` module |
| f-string SQL | **SQL injection** | Parameters |
| `shell=True` with user input | **Command injection** | A list of arguments |
| `pickle` on untrusted data | **Arbitrary code execution** | JSON |
| `datetime.now()` naive | Wrong across timezones and DST | `datetime.now(UTC)` |
| `time.time()` for durations | Negative durations after an NTP jump | `perf_counter` |
| `random` for tokens | Predictable secrets | `secrets` |
| `==` for token comparison | Timing attack | `hmac.compare_digest` |
| Regex for HTML | Fails on valid input | A real parser |
| `json.dumps` on a `Decimal` | `TypeError`, or precision lost via float | A custom encoder emitting a string |
| Unresolved user paths | **Directory traversal** | `resolve()` + `is_relative_to` |

---

## Self-check quiz

1. What is the difference between `resolve()` and `absolute()`, and why does it
   matter for security?
2. Why does the `csv` module need `newline=""`?
3. Name four Python types that do not survive a JSON round trip.
4. Why is f-string SQL a vulnerability and not just bad style?
5. What does unpickling untrusted data allow, and what is the safe alternative?
6. Why is `datetime.now()` almost always wrong?
7. Why is `time.time()` the wrong tool for measuring a duration?
8. When must you use `secrets` rather than `random`?
9. What is catastrophic backtracking, and how do you avoid it?
10. Why is a list of arguments safer than `shell=True`?

---

## Exercises

1. **[`ex01_pathlib.py`](exercises/ex01_pathlib.py)** — Convert twenty
   `os.path` operations, plus a directory-traversal check that must reject six
   attacks.
2. **[`ex02_formats.py`](exercises/ex02_formats.py)** — Round-trip a rich data
   structure through JSON, CSV, TOML and SQLite. Document what each loses.
3. **[`ex03_datetime.py`](exercises/ex03_datetime.py)** — Twelve datetime
   puzzles, all with a DST or timezone trap.
4. **[`ex04_security.py`](exercises/ex04_security.py)** — Five vulnerable
   functions: SQL injection, command injection, path traversal, unsafe
   deserialization, and a timing attack. Exploit each, then fix it.

---

## Going deeper

- [The Python Standard Library](https://docs.python.org/3/library/) — skim the index once; you will remember what exists
- [`pathlib`](https://docs.python.org/3/library/pathlib.html), [`sqlite3`](https://docs.python.org/3/library/sqlite3.html), [`re` HOWTO](https://docs.python.org/3/howto/regex.html)
- [Pickle security](https://docs.python.org/3/library/pickle.html#restricting-globals) — read the warning box
- [OWASP: Injection](https://owasp.org/www-project-top-ten/) — the vulnerability classes in this module, in context

---

**Next:** [Module 20 — Milestone Project: A Packaged Library and CLI](../20-project-library-and-cli/README.md)
