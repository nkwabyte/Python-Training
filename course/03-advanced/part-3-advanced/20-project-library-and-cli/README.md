# Module 20 — Milestone Project: A Packaged Library and CLI

**Time budget:** 14 hours
**Prerequisite:** Modules 14-19

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## What this is for

Parts 1 and 2 built applications. This builds a **library** — something other
people install, import, and depend on. That changes almost every decision:
your API is a promise, your errors are someone else's problem to handle, and
your dependencies become theirs.

| From | Used for |
|---|---|
| 14 Generators | The streaming core: constant memory over unbounded input |
| 15 Decorators | The public plugin API, and caching |
| 16 Errors | An exception hierarchy consumers can actually catch |
| 17 Typing | `py.typed`, `mypy --strict`, a fully typed public surface |
| 18 Testing | 90 percent coverage, property tests, fast suite |
| 19 Stdlib | Files, encodings, serialization, no unnecessary dependencies |

---

## The brief

**`logmine`** — a streaming log analysis library with a CLI on top.

```python
from logmine import Pipeline, parse, filter_by, window, Stats

with open("app.log", encoding="utf-8") as fh:
    result = (Pipeline(fh)
              .parse(format="combined")
              .filter(lambda r: r.status >= 500)
              .window(minutes=5)
              .aggregate(Stats.count, Stats.p95("duration_ms"))
              .collect())
```

```bash
logmine analyse app.log --filter 'status >= 500' --window 5m --stats count,p95
logmine tail app.log --follow --filter 'level == "ERROR"'
logmine formats                       # list registered parsers
cat app.log | logmine analyse - --json | jq '.windows[0]'
```

---

## Requirements

### Functional

| # | Requirement |
|---|---|
| F1 | Parse at least four log formats: combined, JSON lines, syslog, and a user-supplied regex |
| F2 | A fluent, lazy pipeline: parse, filter, map, window, aggregate |
| F3 | Windowing: fixed, sliding, and session |
| F4 | Aggregations: count, sum, mean, min/max, percentiles, cardinality |
| F5 | A filter expression language (`status >= 500 and path ~ "^/api"`) |
| F6 | `--follow` mode that tails a growing file |
| F7 | Output as a table, JSON, or CSV |
| F8 | A registerable parser plugin API |

### Library constraints — the exercise

| # | Constraint | Why |
|---|---|---|
| L1 | Constant memory over a 100 GB input. Verify it. | Module 14 |
| L2 | Zero required runtime dependencies | Every dependency is one you impose |
| L3 | `py.typed`, `mypy --strict` clean, no `Any` in the public API | Module 17 |
| L4 | One exception base class; every error carries data | Module 16 |
| L5 | The library **never** prints, exits, or configures logging | It is not the application |
| L6 | Everything public is documented with a runnable example | |
| L7 | Public API frozen at 1.0 and covered by a compatibility test | |
| L8 | 90 percent coverage, plus property tests on the parsers | Module 18 |
| L9 | Test suite under 5 seconds | A slow suite is an unrun suite |
| L10 | Installable, importable, and runnable from a built wheel | Module 06 |

**L5 is the one that separates a library from a script.** A library that calls
`print()` cannot be used in a service. One that calls `sys.exit()` cannot be
used at all. One that calls `logging.basicConfig()` hijacks the entire host
application's logging. Add a `NullHandler` and stay silent.

---

## Structure

```
logmine/
├── pyproject.toml
├── README.md               with the example that appears above
├── CHANGELOG.md
├── src/logmine/
│   ├── __init__.py         the curated public API + __version__
│   ├── py.typed            the marker that makes your types visible downstream
│   ├── records.py          Record, Field types
│   ├── parsers/            combined.py  jsonl.py  syslog.py  regex.py
│   ├── pipeline.py         the lazy pipeline
│   ├── expressions.py      the filter language: lexer, parser, evaluator
│   ├── windows.py
│   ├── aggregates.py       streaming aggregates only
│   ├── errors.py
│   └── cli/                __init__.py  main.py  render.py
└── tests/
```

---

## Build it in eight stages

### Stage 1 — records and parsers (2h)

`Record` as a frozen dataclass with typed fields plus an `extra` mapping.
Parsers are generators: `Iterable[str] -> Iterator[Record]`.

**A malformed line must not stop the stream.** Decide now how a parse failure
is represented — an exception, a sentinel `Record`, or a tagged union — and
write down the reasoning. Whatever you choose, a 100 GB file with one bad line
on row 40,000,000 must still produce 39,999,999 records.

### Stage 2 — the lazy pipeline (2h)

Each stage returns a new `Pipeline` wrapping a generator. Nothing executes
until `.collect()`, `.first()`, or iteration.

The design question worth solving properly: **`Pipeline` must be typed such
that `.map(str)` on a `Pipeline[Record]` yields a `Pipeline[str]`** and mypy
knows it. That is Module 17's generic pipeline exercise, for real.

### Stage 3 — the expression language (3h)

The largest single piece, and the most fun. A lexer, a recursive-descent
parser producing an AST, and an evaluator.

```
status >= 500 and (path ~ "^/api" or method == "POST") and not bot
```

Three requirements that make it more than a toy: **never `eval()`** (that is
arbitrary code execution on user input — Module 19); report errors with a
column number and a caret; and compile once, evaluate per record, so parsing
does not happen 100 million times.

### Stage 4 — windows and aggregates (2h)

**Every aggregate must be streaming.** `count`, `sum`, `min`, `max` and `mean`
are trivial. `p95` is not, and that is the point: exact percentiles need every
value in memory, which breaks L1. Options: a bounded reservoir sample,
t-digest, or fixed histogram buckets. Pick one, implement it, and **document the
error bound** — an approximate answer with a stated bound is engineering; an
approximate answer presented as exact is a bug.

`cardinality` has the same shape. Exact needs a set of every distinct value;
HyperLogLog needs 12 KB for ±2 percent. Implementing one of these two is the
most interesting hour in the project.

### Stage 5 — the CLI (2h)

Thin. Parses arguments, builds a pipeline, renders. All the rules from
Module 07: data to stdout, messages to stderr, meaningful exit codes, `--json`
for machines.

### Stage 6 — packaging (1.5h)

`pyproject.toml` with a `[project.scripts]` entry point, `py.typed` in the
package data, classifiers, and a README that renders on PyPI.

```bash
python -m build
pip install dist/logmine-1.0.0-py3-none-any.whl
cd /tmp && python -c "import logmine; print(logmine.__version__)"
logmine --help
```

**Test from the built wheel, in a different directory.** That is the only way to
catch a missing `package_data` entry or a module you forgot to include — the
`src/` layout (Module 06) makes your own tests catch it too.

### Stage 7 — tests (2.5h)

- Property tests on every parser: any record you can serialise must parse back.
- Property tests on the expression language: any AST you can generate must
  round-trip through the formatter and re-parse to the same AST.
- A memory test: 10 million synthetic lines under a hard `tracemalloc` ceiling.
- A compatibility test that asserts the exact public API surface (L7).
- Under 5 seconds total.

### Stage 8 — documentation (1h)

Every public function with a runnable example. Then run them:

```bash
pytest --doctest-modules src/logmine
```

**A doctest that runs in CI cannot rot.** This is the single highest-value
documentation practice there is.

---

## Definition of done

- [ ] `pip install dist/*.whl` then `import logmine` works from `/tmp`
- [ ] `logmine --help` works after installation
- [ ] `mypy --strict src/` clean; downstream consumers see your types
      (`py.typed` present and in the wheel)
- [ ] `ruff check` clean
- [ ] `pytest --cov` at 90 percent, in under 5 seconds
- [ ] `pytest --doctest-modules src/` passes
- [ ] 10 million lines processed with peak memory under 50 MB, measured
- [ ] One malformed line in 10 million does not stop the stream
- [ ] `grep -rn "print(\|sys.exit\|basicConfig" src/logmine/ | grep -v cli/`
      returns nothing
- [ ] Zero required runtime dependencies (`pip install logmine` in a clean
      venv pulls nothing else)
- [ ] The filter language rejects `__import__("os").system("...")` as a syntax
      error, not by executing it
- [ ] `p95` documents its error bound, and a test asserts the bound holds
- [ ] The public API test fails if any exported name changes

---

## Rubric

| Area | 1 | 3 | 5 |
|---|---|---|---|
| **Laziness** | Materialises | Mostly lazy | Constant memory, measured, with the streaming aggregate to prove it |
| **API design** | Ad hoc | Consistent | Fluent, typed, documented, frozen and tested |
| **Errors** | Raises builtins | Own exceptions | Hierarchy, data-carrying, documented per function |
| **Typing** | Partial | Complete | `--strict`, `py.typed`, generics that actually track |
| **Testing** | Examples | Good coverage | Properties, memory bounds, API compatibility, fast |
| **Packaging** | Works locally | Installs | Wheel-tested, no deps, entry point, PyPI-ready |
| **Docs** | A README | Docstrings | Runnable examples, verified in CI |

---

## The five hard parts

Where the real learning is. Notice when you hit each.

1. **Streaming percentiles.** Exact needs all the data. You must choose an
   approximation and be honest about its bound. This is the moment
   "constant memory" stops being a slogan.
2. **A typed fluent pipeline.** Getting mypy to track `Pipeline[Record]` →
   `Pipeline[str]` through four chained calls is genuinely fiddly.
3. **An expression language without `eval`.** Everyone's first instinct is
   `eval()`, and it is a remote code execution vulnerability. Writing a real
   parser is a day you will be glad you spent.
4. **`--follow` on a rotated file.** Tailing works until logrotate moves the
   file. Detecting rotation by inode is the correct answer and is not obvious.
5. **Freezing the API.** Deciding what is public is a commitment. Anything you
   export, you support.

---

## Extensions

- Async parsers for network sources (previews Module 22)
- Parallel parsing with `multiprocessing` — note that `Record` must be
  picklable (Module 21)
- A `--profile` flag using `cProfile` (previews Module 23)
- Publish to TestPyPI and install it from there
- Semantic versioning with a script that diffs the public API between tags

---

## Where the solution is

[`solutions/`](solutions/) contains an architecture walkthrough and the two
hardest components — the streaming percentile and the expression parser — in
full. **Do not open it until Stage 4.**
