# Module 07 — Milestone Project: Inventory CLI

**Time budget:** 12 hours
**Prerequisite:** Modules 01-06

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## What this is for

The previous six modules taught pieces. This one is where they fuse. You will
build a complete command-line application from an empty directory, and by the
end you will have used, in anger, every idea from Part 1:

| From | Used for |
|---|---|
| 01 Runtime | `python -m`, entry points, exit codes, reading tracebacks |
| 02 Objects | Not leaking internals, copying, sentinels for optional fields |
| 03 Types | Money without float drift, explicit encodings, `Decimal` |
| 04 Functions | `main(argv)`, keyword-only flags, closures for the dispatch table |
| 05 Collections | The right container per operation, grouping, sorting |
| 06 Packaging | `src/` layout, no import-time I/O, config from the environment |

**Do not skip this.** A module you can pass a quiz on but cannot use in a
project, you do not know.

---

## The brief

An inventory manager for a small warehouse. It is used by a human at a terminal
and by cron jobs, so it must be pleasant interactively and correct
non-interactively.

```bash
inv add SKU-001 "Widget, blue" --qty 40 --price 9.99 --location A1 --tags fast,small
inv list --location A --sort qty --desc
inv move SKU-001 --to B3 --qty 10
inv adjust SKU-001 --delta -5 --reason damaged
inv search widget --in name,tags
inv report low-stock --threshold 10
inv report value --group-by location
inv export --format csv > inventory.csv
inv import inventory.csv --dry-run
inv history SKU-001
```

---

## Requirements

### Functional

| # | Requirement |
|---|---|
| F1 | `add` a new item: SKU, name, quantity, unit price, location, optional tags |
| F2 | `list` with filters (location prefix, tag, min/max qty), sorting, and a `--limit` |
| F3 | `move` quantity between locations, splitting the stock line if partial |
| F4 | `adjust` quantity by a delta, with a mandatory reason |
| F5 | `remove` an item, refusing if quantity is non-zero unless `--force` |
| F6 | `search` across name, SKU and tags, case-insensitively |
| F7 | `report low-stock`, `report value` (total value, grouped), `report dead-stock` (untouched for N days) |
| F8 | `export` and `import` in CSV and JSON, with `--dry-run` on import |
| F9 | `history` of every change to an item, append-only |

### Non-functional — these are the actual exercise

| # | Requirement | Why |
|---|---|---|
| N1 | Runs as `python -m inventory` **and** as `inv` after `pip install -e .` | Module 06 |
| N2 | `import inventory` does no I/O and takes under 100ms | Module 06 |
| N3 | Money is exact. `Decimal` or integer cents, never `float` | Module 03 |
| N4 | Every file read and written specifies `encoding="utf-8"` | Module 03 |
| N5 | Writes are atomic: a kill -9 mid-save must never corrupt the data file | Module 06 |
| N6 | Exit codes: 0 success, 1 operation failed, 2 usage error, 3 data file problem | Module 01 |
| N7 | Errors go to stderr, data goes to stdout. `inv list \| grep` must work | Unix convention |
| N8 | `--json` on any read command emits machine-readable output | Scriptability |
| N9 | No business logic in `cli.py`; no `print` or `sys.exit` outside it | Module 04 |
| N10 | Every function has type hints; `mypy --strict src/` is clean | Module 04 |
| N11 | Data file path from `--file`, else `$INVENTORY_FILE`, else a documented default | Module 06 |
| N12 | Tests do not touch the real data file, ever | Module 06 |

---

## Structure to build

```
inventory-cli/
├── pyproject.toml
├── README.md
├── src/
│   └── inventory/
│       ├── __init__.py       public API, __version__
│       ├── __main__.py       thin shim
│       ├── cli.py            argparse, dispatch, formatting, exit codes
│       ├── models.py         Item, Location, Money, Change
│       ├── store.py          load, save (atomic), the in-memory index
│       ├── operations.py     add/move/adjust/remove -- pure logic
│       ├── reporting.py      the three reports
│       ├── serialization.py  CSV and JSON in and out
│       └── errors.py         the exception hierarchy
└── tests/
    ├── conftest.py
    ├── test_models.py
    ├── test_store.py
    ├── test_operations.py
    ├── test_reporting.py
    ├── test_serialization.py
    └── test_cli.py
```

---

## Build it in eight stages

Each stage produces something that runs. Do not build the whole thing and then
test it — the point of the ordering is that you always have a working program.

### Stage 1 — the skeleton (1h)

`pyproject.toml`, the `src/` tree, `__main__.py`, and a `cli.py` that parses
`--version` and `--help` and nothing else. Get `python -m inventory --version`
and `pip install -e . && inv --version` both working before writing any logic.

Getting this working first means every later stage is testable the moment you
write it.

### Stage 2 — models (2h)

`Money` (from Module 03's exercise — reuse it), `Item`, `Change`. Frozen
dataclasses. Validation in `__post_init__`: SKU format, non-negative quantity,
non-empty name.

Decide now, and write it down: **is `Item` mutable?** The whole design follows
from this answer. The recommendation is immutable — operations return a *new*
`Item` rather than mutating, which makes the history log fall out naturally and
makes every operation trivially testable. Module 11 will make the case properly.

### Stage 3 — the store (2h)

Load and save with atomic writes. An in-memory index by SKU (a dict — Module 05)
and by location (a `defaultdict(list)`). A schema version field in the file
format from day one, so you can migrate later.

```python
def save(self, path: Path) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")
    tmp.replace(path)          # os.replace is atomic on the same filesystem
```

Test N5 for real: write a test that kills the process mid-save (or simulates it
by raising inside the serializer) and asserts the original file is intact.

### Stage 4 — operations (2h)

`add`, `move`, `adjust`, `remove`. Pure functions over the store, each returning
the changed items and a `Change` record. No printing, no exiting, no file
access. Every one of them testable in three lines.

The interesting one is `move` with a partial quantity: moving 10 of 40 units
from A1 to B3 must leave 30 in A1 and create-or-merge 10 in B3. Decide what
"merge" means when B3 already holds that SKU at a different unit price, and
write the decision down. There is no universally right answer, which is the
point — a real requirement has to be pinned by a human.

### Stage 5 — the CLI (2h)

Subparsers, dispatch, formatting, exit codes. The dispatch table is a dict of
name to handler (Module 04). Formatting uses the format mini-language
(Module 03) with column widths computed from the data.

The test that N9 is satisfied:

```bash
grep -rn "print(\|sys.exit" src/inventory/ --include="*.py" | grep -v cli.py
```

must return nothing.

### Stage 6 — reporting (1.5h)

Three reports, using `Counter`, `defaultdict`, grouped sorting, and
`heapq.nlargest` where appropriate (Module 05). Reports return data structures;
`cli.py` renders them. This is what makes `--json` a two-line addition rather
than a rewrite.

### Stage 7 — import and export (1.5h)

The `csv` module, not manual splitting (Module 03's exercise 5 explains why).
`--dry-run` must report exactly what *would* change, which forces the import
logic to be a pure function producing a diff.

Round-trip test: export, import into a fresh store, and assert the two stores
are equal. This one test finds more serialization bugs than any other.

### Stage 8 — hardening (2h)

- Run `ruff check`, `ruff format`, `mypy --strict`. Fix everything.
- Coverage report. Anything under 85 percent, ask why.
- Try to break it: an empty data file, a corrupt one, a data file that is a
  directory, a read-only directory, a SKU with a comma, a name with a newline,
  a name with an emoji, quantity as a string in the JSON, a 100 MB file, two
  processes writing at once.
- Write down what happened for each, and fix the ones that produced a traceback
  instead of a message.

**That last exercise is the most valuable hour in the project.** A traceback
reaching a user is a bug regardless of what caused it.

---

## Definition of done

- [ ] `python -m inventory --help` and `inv --help` both work
- [ ] `python -c "import inventory"` prints nothing and finishes in under 100ms
- [ ] `mypy --strict src/` is clean
- [ ] `ruff check src/ tests/` is clean
- [ ] `pytest --cov` shows 85 percent or better
- [ ] No `print` or `sys.exit` outside `cli.py`
- [ ] `inv list --json | python -c "import json,sys; json.load(sys.stdin)"` works
- [ ] `inv list 2>/dev/null | head -3` shows data with no error text
- [ ] A corrupted data file produces a clear message and exit code 3, not a
      traceback
- [ ] Killing the process mid-save leaves the original file intact
- [ ] Tests pass against the *installed* package, and never touch your real
      data file
- [ ] `inv export --format csv | inv import --dry-run -` reports no changes

---

## Rubric

Score yourself honestly. This is the checkpoint for Part 1.

| Area | 1 — needs work | 3 — solid | 5 — professional |
|---|---|---|---|
| **Structure** | One file, or logic in `cli.py` | Modules split by concern | Each module has one reason to change; dependencies flow one way |
| **Errors** | Tracebacks reach the user | Caught, with messages | Own exception hierarchy, mapped to exit codes, messages that say what to do |
| **Types** | None, or `Any` everywhere | Hints on public functions | `mypy --strict` clean, precise types, no `Any` |
| **Testing** | Manual only | Happy paths covered | Edge cases, failure injection, round-trip properties |
| **Data safety** | Direct overwrite | Atomic writes | Atomic + schema version + a corruption test |
| **CLI quality** | Works if used correctly | Good `--help`, sane errors | Composable, `--json`, correct streams, correct exit codes |
| **Money** | `float` | `Decimal` | Exact type with no lossy construction path |

Anything scoring 1 or 2, fix before Part 2. Those are the habits that compound.

---

## Extensions, if you want them

- A `--watch` mode that re-renders on file change
- Undo, by replaying the append-only history
- A locking scheme so two processes cannot corrupt the file (`fcntl.flock`,
  and think about what happens on NFS)
- Fuzzy search with `difflib.get_close_matches`
- A `--profile` flag that reports where the time went (previews Module 23)
- Swap the JSON store for SQLite behind the same interface (previews Modules
  10 and 27)

---

## Where the solution is

[`solutions/`](solutions/) contains a complete reference implementation.
**Do not open it until you have a working Stage 5.** Reading a finished design
before you have struggled with the decisions removes the entire benefit — the
value is in having made the choices badly first and seeing why.

When you do read it, read `operations.py` and `errors.py` first. Those are where
the design choices are visible.
