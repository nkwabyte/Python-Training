# Reference Notes — Plugin Document Pipeline

**Do not read this until Stage 5 runs.** The value of this project is in hitting
the six traps yourself.

This is an architecture walkthrough rather than a full implementation. The
project is large enough that copying an answer would defeat it; what follows is
the set of decisions that determine whether your version works, each with the
reasoning and the code that expresses it.

---

## 1. The extension point

```python
# protocols.py -- the ONLY thing a plugin author needs to satisfy,
# and they do not import it.
class Stage(Protocol):
    name: str
    def __call__(self, doc: Document) -> Iterable[Document]: ...
```

**Why a Protocol and not a base class.** With `class MyStage(BaseStage)`, every
plugin author imports your package, and every rename in your base class breaks
every plugin ever written. With a Protocol, plugins define a class of the right
shape and your name never appears in their code. You can rename `BaseStage` to
anything; nothing breaks, because nothing referred to it.

**Why `__call__` rather than a `process` method.** A plain function is then a
valid stage. Most stages are one transformation, and D8 says a class with a
single non-`__call__` method should have been a function. This signature lets
both work with no adapter.

```python
@stage("upper")
def upper(doc: Document) -> Iterable[Document]:
    yield doc.derive(doc.content.upper(), by="upper")
```

**Why `Iterable[Document]` out, not `Document`.** One signature covers three
behaviours: yield nothing (a filter), yield one (a transform), yield several (a
split). Without it you need three stage types, three registries, and an
`isinstance` check in the core — which D3 forbids for exactly this reason.

---

## 2. The Document

```python
@dataclass(frozen=True, slots=True)
class Document:
    content: str
    metadata: Metadata
    provenance: tuple[str, ...] = ()

    def derive(self, content: str, *, by: str, **meta: Any) -> Document:
        return replace(self, content=content,
                       metadata=self.metadata.with_(**meta),
                       provenance=(*self.provenance, by))
```

**`provenance` is the payoff for immutability.** Every `derive` appends one
entry, so at the end each document carries the exact list of stages that touched
it. Nobody implemented an audit trail; it fell out of the shape.

**The metadata decision.** Three options, all defensible:

| Choice | Cost | Benefit |
|---|---|---|
| `frozen dataclass` | Fixed fields; plugins cannot add their own | Type-checked, fastest |
| `FrozenDict` (Module 09) | Untyped values | Plugins can add keys; hashable |
| plain `dict` | **Mutable — trap 2** | Familiar |

Recommended: a **frozen dataclass with an `extra: FrozenDict` field**. Core
fields are typed and checked; plugins get a namespace of their own that cannot
collide with core fields. The plain dict is the trap: one stage mutating it
changes every document that shares it, and they all do, because `replace()` is
a shallow copy (Module 11).

**`slots=True`** because a run may hold 100,000 of these.

---

## 3. The registry

```python
STAGES: dict[str, StageFactory] = {}

def stage(name: str, *, options: type[Any] | None = None) -> Callable[[F], F]:
    def register(factory: F) -> F:
        if name in STAGES:
            existing = STAGES[name].__module__
            raise ValueError(
                f"stage {name!r} is already registered by {existing}; "
                f"{factory.__module__} cannot also claim it"
            )
        factory.options_type = options          # type: ignore[attr-defined]
        STAGES[name] = factory
        return factory
    return register
```

**Rejecting duplicates loudly is not pedantry.** Two plugins claiming
`"validate"` resolved by import order is non-deterministic, works on your
machine, and fails in production with no error at all. The message must name
**both** modules, or the user cannot tell which plugin to remove.

**Discovery, and the difference that matters:**

```python
def discover() -> None:
    from docpipe import stages          # built-ins: import to register
    for ep in entry_points(group="docpipe.stages"):
        ep.load()                        # third-party: found without importing
```

A decorator registry only sees plugins whose module has been imported. Entry
points are declared in `pyproject.toml` and found across every installed
distribution. That is the whole reason entry points exist, and it is why Stage 8
of the brief is a separate installable package — if that step required editing
`docpipe`, the design failed.

---

## 4. Execution: lazy from end to end

```python
def run(self, docs: Iterable[Document]) -> Iterator[Document]:
    for stage in self._stages:
        docs = self._apply(stage, docs)      # builds a chain; runs nothing
    return iter(docs)

def _apply(self, stage: Stage, docs: Iterable[Document]) -> Iterator[Document]:
    for doc in docs:
        try:
            yield from stage(doc)
        except Exception as exc:                        # noqa: BLE001
            self._report.record_error(stage.name, doc, exc)
            if self._report.error_count > self._budget:
                raise TooManyErrors(self._report) from exc
```

**Trap 3 lives here.** `docs = list(stage(docs))` is the natural way to write
it, works fine at 100 documents, and exhausts memory at 100,000. The generator
version holds one document at a time regardless of input size.

**Error isolation must be *inside* the loop.** This is the subtle part of D10
and the thing most builds get wrong: an exception inside a generator terminates
that generator **permanently** — you cannot resume it. So a try/except wrapped
around the whole pipeline loses every remaining document. Per-document, inside
the loop, is the only shape that works.

**The error budget** exists because 40,000 failures is not a data problem, it is
a configuration problem, and continuing wastes 40 minutes to reach the same
conclusion.

---

## 5. Config validated up front

Three passes, in order, collecting everything:

1. **Structure** — is it valid TOML, does it have a `stages` list?
2. **Names** — is every `kind` registered? On a miss, use
   `difflib.get_close_matches` against the registry for a "did you mean".
3. **Options** — for each stage, check its declared options type: unknown keys,
   missing required, wrong types.

```
config.toml: 3 problems

  [stages.2] minify: unknown option 'lvl'. Did you mean 'level'?
  [stages.3] validate: rule 'no_borken_links' is not registered
             (available: no_broken_links, has_title, max_length)
  [stages.5] write: 'path' is required
```

**Trap 5** is validating options at run time. A typo then surfaces after 40
minutes of processing rather than at second zero. The rule from Module 06 holds
at every scale: **validate configuration once, at startup, and report all
problems together** — because each restart cycle costs the user a full run.

---

## 6. Injecting the world

```python
@dataclass(frozen=True)
class Runtime:
    fs: FileSystem = field(default_factory=RealFileSystem)
    clock: Callable[[], float] = time.perf_counter
    now: Callable[[], datetime] = lambda: datetime.now(timezone.utc)
```

One `Runtime` object rather than five parameters threaded through every call.
Stages that need I/O receive it; stages that do not, do not.

This is what makes the "core test suite touches no filesystem" requirement
achievable. And the clock in particular is what lets a test assert
`report.stage_times["minify"] == 0.5` exactly, rather than asserting it is "some
positive number" — which is a much weaker test (Module 08).

---

## 7. The traps, and what hitting each teaches

| Trap | Symptom when you hit it | The lesson |
|---|---|---|
| Base class for stages | Stage 8 needs core edits | Extension points define shape, not ancestry |
| Mutable metadata | A test on document 1 fails after adding document 2 | Module 02, in production |
| Materialising between stages | Fine at 100 docs, dead at 100,000 | Laziness is a design decision, not an optimisation |
| `isinstance` dispatch | The first third-party stage does not run | Dispatch on registration, not on type |
| Runtime option validation | A typo costs 40 minutes | Validate at the boundary, once |
| Clock called internally | Timing tests assert "> 0" and nothing more | Inject anything that varies |

**The most useful thing you can do at the end of this project** is note which
traps you hit. Each one maps to a module, and the ones you hit are the ones to
reread before Part 3.

---

## What a good solution looks like from outside

```bash
$ docpipe stages
read              read files matching a glob
strip_frontmatter remove YAML frontmatter
markdown_to_html  convert markdown to HTML
minify            collapse whitespace (level: 1-3)
validate          apply named rules
write             write documents to a directory
wordcount         add a word count      [docpipe-plugin-wordcount 0.1.0]

$ docpipe run config.toml --explain
resolved plan (6 stages):
  1. read              path='input/*.md'  encoding='utf-8' (default)
  2. strip_frontmatter format='yaml' (default)
  ...

$ docpipe run config.toml
processed 100,000 documents in 42.3s
  read              100,000 ->  100,000    3.1s
  markdown_to_html  100,000 ->  100,000   28.7s
  validate          100,000 ->   99,997    6.2s   3 errors
  write              99,997 ->   99,997    4.3s

3 errors (see --report errors.json)
```

Note what that last run demonstrates: 100,000 documents, three failures, and the
other 99,997 completed. That is D10, and it is the requirement that separates a
pipeline you can run on real data from one you can demo.
