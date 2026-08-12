# Module 13 — Milestone Project: Plugin Document Pipeline

**Time budget:** 12 hours
**Prerequisite:** Modules 08-12

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## What this is for

Part 1's project was about structure: layers, files, exit codes. This one is
about **types**. Every design decision from Modules 08-12 shows up, and the
brief is written so that the wrong decision produces visible pain rather than an
abstract critique.

| From | Used for |
|---|---|
| 08 Classes | Encapsulation, properties, no leaked internals, `__slots__` where it pays |
| 09 Data model | The pipeline is iterable, documents are hashable, stages are callable |
| 10 Inheritance | `Protocol` for the plugin interface, composition for the pipeline |
| 11 Dataclasses | Frozen documents, enums for stage kinds, value objects throughout |
| 12 Design | Registry over inheritance, DI for I/O, descriptors for config |

---

## The brief

A document processing pipeline. Documents enter, pass through an ordered series
of stages, and come out transformed. Stages are **plugins**: third parties write
them, you never modify your code to accept a new one.

```python
pipeline = Pipeline.from_config({
    "stages": [
        {"kind": "read", "path": "input/*.md"},
        {"kind": "strip_frontmatter"},
        {"kind": "markdown_to_html"},
        {"kind": "minify", "level": 2},
        {"kind": "validate", "rules": ["no_broken_links", "has_title"]},
        {"kind": "write", "path": "output/"},
    ]
})

report = pipeline.run()
print(report.summary())
```

```bash
docpipe run config.toml
docpipe run config.toml --dry-run --explain
docpipe stages                          # list every registered stage
docpipe stages markdown_to_html         # describe one, with its options
docpipe validate config.toml            # check the config without running
```

---

## Requirements

### Functional

| # | Requirement |
|---|---|
| F1 | A `Document` type: content, metadata, provenance, immutable |
| F2 | Stages transform documents. At least eight built in. |
| F3 | Stages are registered by name and discovered without editing core code |
| F4 | Config is validated **before** anything runs, with all errors at once |
| F5 | A stage may produce 0, 1, or many documents (filter, transform, split) |
| F6 | Errors in one document do not abort the run; they are collected |
| F7 | A report: per stage, per document, timings, errors |
| F8 | `--dry-run` shows what would happen with no side effects |
| F9 | `--explain` shows the resolved plan, including defaults |
| F10 | Third-party stages installable via entry points |

### Design constraints — the actual exercise

| # | Constraint | Why |
|---|---|---|
| D1 | `Document` is a frozen dataclass. Stages return new documents. | Module 11 |
| D2 | The stage interface is a `Protocol`. No stage inherits from your code. | Module 10 |
| D3 | No `isinstance` in the pipeline core, except at the config boundary | Module 10 |
| D4 | `Pipeline` is iterable, sized, and indexable | Module 09 |
| D5 | All I/O is injected. The core is testable with zero filesystem access. | Module 12 |
| D6 | Stage options are validated at registration, not at run time | Module 12 |
| D7 | Adding a stage touches exactly **one** file — the new stage's | Module 12 |
| D8 | No class with a single method that is not `__call__` | Module 12 |
| D9 | `mypy --strict` clean, no `Any` in public signatures | Module 04 |
| D10 | A stage that raises cannot corrupt the pipeline or lose other documents | Module 09 |

---

## Structure

```
docpipe/
├── pyproject.toml
├── src/docpipe/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── document.py       Document, Metadata, Provenance
│   ├── protocols.py      Stage, Source, Sink, Clock -- ALL the Protocols
│   ├── registry.py       registration and discovery
│   ├── pipeline.py       composition and execution
│   ├── report.py         results, timings, errors
│   ├── config.py         parse and validate TOML
│   ├── errors.py
│   └── stages/
│       ├── __init__.py   imports every built-in so they register
│       ├── read.py  write.py  markdown.py  minify.py
│       ├── validate.py  filter.py  split.py  template.py
└── tests/
```

---

## Build it in eight stages

### Stage 1 — `Document` and the protocols (1.5h)

```python
@dataclass(frozen=True, slots=True)
class Document:
    content: str
    metadata: Metadata                    # frozen, not a dict
    provenance: tuple[str, ...] = ()      # tuple, NOT list -- Module 11

    def derive(self, content: str, *, by: str) -> "Document":
        return replace(self, content=content,
                       provenance=(*self.provenance, by))
```

`provenance` accumulating on every `derive` gives you a free audit trail: at the
end, every document knows exactly which stages touched it. That falls out of
immutability and would need bookkeeping without it.

**The decision to write down:** `Metadata` as a frozen dataclass, a
`FrozenDict`, or a plain dict? Each has a real cost. Choose and justify.

### Stage 2 — the registry (1.5h)

```python
STAGES: dict[str, StageFactory] = {}

def stage(name: str, *, options: type | None = None):
    def register(factory: StageFactory) -> StageFactory:
        if name in STAGES:
            raise ValueError(f"stage {name!r} is already registered by "
                             f"{STAGES[name].__module__}")
        STAGES[name] = factory
        return factory
    return register
```

Rejecting duplicate names is not pedantry. Two plugins claiming `"validate"`
must fail loudly at import, not resolve by import order — which is
non-deterministic and produces a bug nobody can reproduce.

### Stage 3 — config validation (1.5h)

Parse TOML, resolve defaults, validate every stage's options, and report **all**
errors at once (Module 06's lesson). A config error must never surface halfway
through processing 10,000 documents.

Make the error good:

```
config.toml: 3 problems

  [stages.2] minify: unknown option 'lvl'. Did you mean 'level'?
  [stages.3] validate: rule 'no_borken_links' is not registered
             (available: no_broken_links, has_title, max_length)
  [stages.5] write: 'path' is required
```

### Stage 4 — execution (2h)

The interesting design question. A stage takes one document and returns
`Iterable[Document]` — 0 for a filter, 1 for a transform, N for a split. That
single signature covers all three, and it means the pipeline is a **generator
pipeline** (Module 14, arriving early):

```python
def run(self, docs: Iterable[Document]) -> Iterator[Document]:
    for stage in self._stages:
        docs = self._apply(stage, docs)      # lazy: nothing runs yet
    return iter(docs)
```

Nothing is materialised, so a pipeline over 100,000 documents uses constant
memory. Get this shape right and the memory question never arises.

### Stage 5 — error isolation (1.5h)

D10 is the hardest requirement. One document failing must not lose the other
99,999, and a stage raising must not corrupt the pipeline. Consider: per-document
try/except, an error budget that aborts after N failures, and what a failure
inside a *generator* stage means for the documents after it.

That last one is genuinely subtle. Work out what happens when a generator raises
mid-iteration and whether the remaining documents are recoverable.

### Stage 6 — the report (1h)

Timings per stage, documents in and out, errors with the document that caused
them. Returned as data, rendered by the CLI (Module 07's rule).

### Stage 7 — the CLI (1.5h)

`run`, `stages`, `validate`, plus `--dry-run` and `--explain`. `--explain` must
print the **resolved** plan including every default, so a user can see what the
config actually means. This is one of the highest-value features a config-driven
tool can have.

### Stage 8 — a third-party plugin (1.5h)

Create a **separate package** — `docpipe-plugin-wordcount` — with its own
`pyproject.toml` declaring an entry point. Install it. Confirm `docpipe stages`
lists it with no change to your code.

If that requires editing anything in `docpipe`, D3 or D7 was violated, and this
stage is where you find out.

---

## Definition of done

- [ ] `mypy --strict src/` clean, no `Any` in a public signature
- [ ] `ruff check` clean
- [ ] `pytest --cov` at 90 percent or better
- [ ] The core test suite runs with **no filesystem access at all**
- [ ] `grep -rn "isinstance" src/docpipe/ | grep -v config.py` returns nothing
- [ ] A separately installed package adds a stage with zero core changes
- [ ] A stage raising on document 5000 still processes 5001 through 100000
- [ ] Two plugins claiming one name fail at import with both module names
- [ ] Config errors are all reported at once, with suggestions for typos
- [ ] `--dry-run` touches nothing; verified by running it with a read-only
      output directory
- [ ] A 100,000-document run uses constant memory (measure it — Module 23
      preview)
- [ ] Every `Document` carries the full list of stages that touched it

---

## Rubric

| Area | 1 | 3 | 5 |
|---|---|---|---|
| **Extensibility** | New stage means editing core | Registry works | Third-party package works, entry points, no core edit |
| **Types** | `Any` everywhere | Hints present | `mypy --strict`, `Protocol`s, no `Any` |
| **Immutability** | Mutable documents | Frozen documents | Frozen through and through, provenance free |
| **Errors** | First failure aborts | Collected | Isolated, budgeted, attributed, actionable messages |
| **Testability** | Needs the filesystem | Some fakes | Core is pure; every dependency injected |
| **Data model** | Plain methods | Some dunders | Iterable, sized, indexable, hashable, useful reprs |
| **Config** | Fails at runtime | Validated | All errors at once, typo suggestions, `--explain` |

Score 1 or 2 anywhere and fix it before Part 3.

---

## The traps this brief is built around

Each is a decision that seems fine and gets expensive. Notice when you hit them.

1. **Stage as a class hierarchy.** `class MyStage(BaseStage)` seems natural and
   immediately violates D2 — third parties must now import and inherit from you.
   A `Protocol` plus a registered callable does not.
2. **Metadata as a mutable dict.** One stage mutating it, and every earlier
   document silently changes too. Module 02, in production.
3. **Materialising between stages.** `docs = list(stage(docs))` is the obvious
   way to write it, works fine at 100 documents, and exhausts memory at 100,000.
4. **`isinstance` for stage dispatch.** Works until the first third-party stage.
5. **Validating options at run time.** A config typo surfaces after 40 minutes
   of processing instead of at second zero.
6. **The clock.** Timings need `perf_counter`. If it is called inside the
   pipeline rather than injected, no test can assert on a duration.

---

## Extensions

- Parallel execution with `concurrent.futures` (previews Module 21). What must
  be true of a stage for it to be safe to run in parallel? Enforce it.
- Caching: skip a stage if its input document hash and options are unchanged.
- A stage that needs *all* documents (sort, deduplicate). How does that fit a
  streaming pipeline, and what does it cost?
- Conditional stages: run only if a predicate matches.
- Async stages for network-bound work (previews Module 22).

---

## Where the solution is

[`solutions/`](solutions/) has an architecture walkthrough and the key modules.
**Do not open it until Stage 5 runs.** The value here is in hitting the traps
yourself; reading the answers first removes it entirely.
