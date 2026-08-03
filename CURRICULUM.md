# Curriculum Map

20 weeks at 10 to 15 hours per week. Each week is roughly one to two modules
plus exercise time. Milestone projects get a full week each.

Legend: **L** = lesson hours, **E** = exercise hours, **P** = project hours.

---

## Part 1 — Foundations (Weeks 1-4)

Goal: understand what the interpreter is actually doing. By the end of Part 1
you can reason about names and objects, choose the right built-in type for a
job, and organise code into modules and packages that import cleanly.

| Wk | Module | Topics | Time |
|---|---|---|---|
| 1 | [01 The Runtime and the Toolchain](course/part-1-foundations/01-runtime-and-toolchain/README.md) | CPython vs Python. Source to bytecode to eval loop. `__pycache__`. Interpreters (CPython, PyPy, MicroPython). Virtual environments, `pip`, `uv`, lockfiles. Script vs module vs package. `sys.path`. The REPL as a laboratory. Reading a traceback. | L3 E4 |
| 1-2 | [02 Objects, Names, and the Data Model](course/part-1-foundations/02-objects-names-data-model/README.md) | Everything is an object. Names are bindings, not boxes. Identity vs equality. Mutability and aliasing. Reference counting and the cycle collector. Small-int and string interning. Shallow vs deep copy. Truthiness. `None`. | L5 E6 |
| 2 | [03 Core Types and Their Behaviour](course/part-1-foundations/03-core-types/README.md) | `int` (arbitrary precision), `float` (IEEE 754 traps), `Decimal`, `Fraction`, `bool`. `str` vs `bytes` and the encoding boundary. f-strings and the format mini-language. Slicing. Hashability. `list`, `tuple`, `dict`, `set` at a glance. | L5 E6 |
| 2-3 | [04 Control Flow, Functions, and Scope](course/part-1-foundations/04-control-flow-and-functions/README.md) | Statements vs expressions. `for`/`else`, `while`/`else`, the walrus operator, `match`. Functions as objects. Positional-only and keyword-only params, `*args`/`**kwargs`, defaults and the mutable-default trap. LEGB scope, `global`, `nonlocal`, closures. Type hints as documentation that runs. | L5 E7 |
| 3 | [05 Collections in Depth and Comprehensions](course/part-1-foundations/05-collections-and-comprehensions/README.md) | `list` growth and complexity. `dict` insertion order and hashing. `set` algebra. Comprehensions and generator expressions. Sorting with `key`, stability, `operator`. `collections`: `Counter`, `defaultdict`, `deque`, `namedtuple`, `ChainMap`. Choosing the right container. | L4 E7 |
| 3-4 | [06 Modules, Packages, and Project Layout](course/part-1-foundations/06-modules-packages-projects/README.md) | The import system end to end. Absolute vs relative imports. `__init__.py`, namespace packages. `__main__` and `python -m`. Circular imports and how to break them. The src layout. `pyproject.toml` first contact. Where config and secrets go. | L4 E5 |
| 4 | [07 Milestone Project: Inventory CLI](course/part-1-foundations/07-project-inventory-cli/README.md) | A complete multi-module command-line application: `argparse`, JSON persistence, input validation, structured errors, exit codes, and a test script. | P12 |

---

## Part 2 — Object-Oriented Python (Weeks 5-8)

Goal: model problems with types, the Python way. By the end of Part 2 you can
design a class that behaves correctly under every language protocol, and you
know when a function would have been the better answer.

| Wk | Module | Topics | Time |
|---|---|---|---|
| 5 | [08 Classes and Encapsulation](course/part-2-oop/08-classes-and-encapsulation/README.md) | The class body as executable code. Instance vs class attributes and the shared-mutable trap. `self`. Bound methods. `@property`, setters, computed attributes. `_private` convention and `__name` mangling. `@classmethod` factories, `@staticmethod`. `__slots__`. | L5 E7 |
| 5-6 | [09 The Data Model: Dunder Methods](course/part-2-oop/09-dunder-and-data-model/README.md) | `__repr__` vs `__str__`. `__eq__` and `__hash__` as a pair. Ordering and `functools.total_ordering`. Container protocol: `__len__`, `__getitem__`, `__contains__`, `__iter__`. `__call__`. Arithmetic and reflected operators. Context managers: `__enter__`/`__exit__`. `__getattr__` vs `__getattribute__`. | L6 E8 |
| 6-7 | [10 Inheritance, Composition, and the MRO](course/part-2-oop/10-inheritance-composition-mro/README.md) | Has-a vs is-a. `super()` is not "the parent class". C3 linearisation and the diamond. Cooperative multiple inheritance and mixins. Abstract base classes. `Protocol` and structural typing. Duck typing and when to stop using `isinstance`. | L6 E8 |
| 7 | [11 Dataclasses, Enums, and Value Semantics](course/part-2-oop/11-dataclasses-and-value-semantics/README.md) | `@dataclass`, `field`, `frozen`, `slots`, `__post_init__`, ordering. `NamedTuple` vs `TypedDict` vs `dataclass` vs `dict`. `Enum`, `IntEnum`, `StrEnum`, `auto`. Pydantic as validating dataclasses. Copy semantics and immutability as a design tool. | L4 E6 |
| 8 | [12 Design Principles in Python](course/part-2-oop/12-design-principles-in-python/README.md) | SOLID translated into a language with first-class functions. Composition over inheritance in practice. Dependency injection without a framework. Descriptors, the mechanism under `@property`. `__init_subclass__`, class decorators, metaclasses and when never to use them. Design patterns that Python dissolves. | L5 E6 |
| 8 | [13 Milestone Project: Plugin Document Pipeline](course/part-2-oop/13-project-plugin-pipeline/README.md) | A polymorphic processing pipeline with a plugin registry, protocol-based extensibility, serialization, and a full pytest suite. | P12 |

---

## Part 3 — Idiomatic and Advanced Python (Weeks 9-13)

Goal: write Python that a senior engineer would approve in review, and that
survives contact with real data and real users.

| Wk | Module | Topics | Time |
|---|---|---|---|
| 9 | [14 Iterators, Generators, and Lazy Pipelines](course/part-3-advanced/14-iterators-and-generators/README.md) | The iterator protocol. Writing `__iter__`/`__next__`. Generator functions and generator expressions. `yield from`. Generators as coroutines (`send`, `throw`, `close`). `itertools` as a composable toolkit. Streaming a file larger than RAM. | L5 E8 |
| 9-10 | [15 Decorators, Closures, and functools](course/part-3-advanced/15-decorators-closures-functools/README.md) | Closures and cell variables. Decorators with and without arguments. `functools.wraps` and why bare decorators break introspection. `lru_cache`/`cache`, `partial`, `singledispatch`, `cached_property`, `reduce`. Class decorators. `contextlib` and `@contextmanager`. Stacking order. | L5 E7 |
| 10-11 | [16 Error Handling and Robustness](course/part-3-advanced/16-error-handling-and-robustness/README.md) | The exception hierarchy. `try/except/else/finally` semantics precisely. Custom exception design. Chaining with `raise ... from`. EAFP vs LBYL. `ExceptionGroup` and `except*`. Context managers for cleanup. `logging` done properly. Retries, timeouts, and backoff. What never to catch. | L5 E7 |
| 11-12 | [17 Typing and Static Analysis](course/part-3-advanced/17-typing-and-static-analysis/README.md) | Gradual typing strategy. Built-in generics, `Optional`, unions, `Literal`, `Final`. `TypeVar`, generic classes, PEP 695 syntax. `Protocol`, `overload`, `TypedDict`, `NewType`, `Self`. Variance in one page. mypy and pyright configuration. Runtime validation vs static types. Typing a real codebase incrementally. | L5 E7 |
| 12 | [18 Testing, Debugging, and Quality](course/part-3-advanced/18-testing-and-quality/README.md) | pytest: assertions, fixtures, scope, `parametrize`, markers, `conftest.py`. Test doubles: `unittest.mock`, `monkeypatch`, fakes vs mocks. Coverage and what it does not tell you. Property-based testing with Hypothesis. `pdb`/`breakpoint()`. `ruff`, formatting, pre-commit. Designing code for testability. | L5 E8 |
| 12-13 | [19 The Standard Library, Files, and Serialization](course/part-3-advanced/19-stdlib-files-serialization/README.md) | `pathlib` over `os.path`. Text vs binary I/O and encodings. `json`, `csv`, `sqlite3`, `pickle` (and its dangers), `struct`, `tomllib`. `datetime`, timezones, and the aware/naive rule. `re` at working depth. `subprocess` safely. `argparse`. `random` vs `secrets`. | L5 E7 |
| 13 | [20 Milestone Project: A Packaged Library and CLI](course/part-3-advanced/20-project-library-and-cli/README.md) | Build a real library end to end: a streaming log-analysis engine with a plugin API, full type coverage, 90 percent test coverage, a CLI front end, and a publishable `pyproject.toml`. | P14 |

---

## Part 4 — Concurrency, Performance, and Internals (Weeks 14-15)

Goal: reason about parallelism and about speed with evidence rather than
folklore.

| Wk | Module | Topics | Time |
|---|---|---|---|
| 14 | [21 The GIL, Threads, and Processes](course/part-4-concurrency/21-gil-threads-processes/README.md) | What the GIL actually locks. Why threads still help for I/O. `threading`, `Lock`, `RLock`, `Event`, `Queue`. Race conditions and atomicity in Python. `multiprocessing`, pickling boundaries, shared memory. `concurrent.futures` as the unified front end. Free-threaded CPython (PEP 703) and what changes. | L5 E7 |
| 14 | [22 Asyncio](course/part-4-concurrency/22-asyncio/README.md) | The event loop as a scheduler. Coroutines, awaitables, tasks. `gather` vs `TaskGroup`. Cancellation and timeouts. Async context managers and iterators. Blocking the loop: the number one asyncio bug. `run_in_executor`. Async clients (`httpx`, `asyncpg`). Structured concurrency. Debugging async. | L5 E8 |
| 15 | [23 Performance and Profiling](course/part-4-concurrency/23-performance-and-profiling/README.md) | Measure before you change. `timeit` correctly. `cProfile`, `pstats`, flame graphs, `py-spy`. Memory: `tracemalloc`, `__slots__`, generators. Algorithmic vs interpreter overhead. Vectorising with NumPy. When to reach for C, Cython, or Rust. Caching strategies. Knowing when to stop. | L4 E6 |
| 15 | [24 CPython Internals](course/part-4-concurrency/24-cpython-internals/README.md) | `dis` and reading bytecode. Frames, code objects, the eval loop. How attribute lookup really resolves (type, MRO, descriptors, `__dict__`). Memory layout, arenas, and why an `int` is 28 bytes. Interning. What the 3.11+ specialising adaptive interpreter does. Reading CPython source. | L4 E5 |

---

## Part 5 — Applied Python (Weeks 16-18)

Goal: use Python for the three things you actually want it for — backends, data,
and automation — with production habits from the first line.

| Wk | Module | Topics | Time |
|---|---|---|---|
| 16 | [25 Automation, Scripting, and the OS](course/part-5-applied/25-automation-and-os/README.md) | Robust scripts: exit codes, signals, idempotency, dry-run. `pathlib` recipes, atomic writes, file locking, temp files. `subprocess` pipelines. Environment and config. Building real CLIs with `argparse` and Typer. Scheduling with cron and systemd timers. Watching filesystems. Writing scripts other people can run. | L4 E7 |
| 16 | [26 HTTP, APIs, and Scraping](course/part-5-applied/26-http-and-scraping/README.md) | HTTP as a protocol, not a library call. `httpx` sessions, timeouts, retries, connection pooling. REST and pagination. Auth: API keys, bearer tokens, OAuth2 flow. Rate limiting and politeness. Parsing HTML with selectolax/BeautifulSoup. `robots.txt`, ToS, and the ethics line. Caching responses. | L4 E7 |
| 17 | [27 Databases and Persistence](course/part-5-applied/27-databases-and-persistence/README.md) | SQL you must know: joins, indexes, `EXPLAIN`. DB-API 2.0 and `sqlite3`. Parameterised queries and SQL injection. Transactions and isolation levels. SQLAlchemy Core vs ORM. Sessions, the identity map, and the N+1 problem. Migrations with Alembic. Connection pooling. When Redis or a document store is the right answer. | L5 E8 |
| 17 | [28 Building APIs with FastAPI](course/part-5-applied/28-apis-with-fastapi/README.md) | ASGI. Routing, path/query/body params. Pydantic v2 models as the contract. Dependency injection. Async endpoints and the sync escape hatch. Errors and consistent error shape. Auth with JWT. Middleware and CORS. Background tasks. Testing with `TestClient`. Auto-generated OpenAPI. Project structure that survives growth. | L5 E9 |
| 18 | [29 Data and ML Foundations](course/part-5-applied/29-data-and-ml-foundations/README.md) | NumPy: ndarray, dtypes, broadcasting, views vs copies, vectorised thinking. pandas: Series/DataFrame, indexing, `groupby`, joins, reshaping, time series, the memory traps. Cleaning real data. Plotting for insight. scikit-learn: the estimator API, pipelines, train/test discipline, leakage, metrics that match the problem. Reproducibility. | L6 E10 |
| 18 | [30 Packaging, Deployment, and Ops](course/part-5-applied/30-packaging-and-deployment/README.md) | `pyproject.toml` in full. Build backends, wheels vs sdists, editable installs. Dependency resolution and lockfiles. Versioning and changelogs. Publishing to PyPI. Dockerising Python properly (multi-stage, non-root, layer caching). 12-factor config and secrets. CI with GitHub Actions. Health checks and graceful shutdown. | L5 E7 |

---

## Part 6 — System Design with Python (Weeks 19-20)

Goal: build systems, not just programs. Every module ends with a design
exercise written the way an interview or a design doc would pose it.

| Wk | Module | Topics | Time |
|---|---|---|---|
| 19 | [31 Design Fundamentals](course/part-6-system-design/31-design-fundamentals/README.md) | Requirements: functional, non-functional, and the questions to ask. Back-of-envelope estimation and the latency numbers to memorise. Throughput vs latency vs concurrency (Little's Law). CAP and PACELC honestly. Consistency models. Availability math. The design interview framework, step by step. | L4 E5 |
| 19 | [32 Service Architecture and Concurrency Models](course/part-6-system-design/32-service-architecture/README.md) | WSGI vs ASGI. Process and worker models: gunicorn, uvicorn, workers vs threads vs async. Where Python's concurrency model constrains architecture. Load balancing, statelessness, sticky sessions. Backpressure and queueing theory in practice. Graceful shutdown and zero-downtime deploys. Monolith, modular monolith, microservices. | L4 E7 |
| 19-20 | [33 Caching, Queues, and Background Jobs](course/part-6-system-design/33-caching-queues-jobs/README.md) | Cache layers and where to put them. Cache-aside, write-through, write-behind. Invalidation, TTLs, stampedes, and the thundering herd. Redis data structures beyond GET/SET. Task queues: Celery, RQ, arq, and the tradeoffs. Idempotency keys, retries, dead-letter queues, exactly-once as a myth. Scheduled work at scale. | L4 E7 |
| 20 | [34 Data at Scale](course/part-6-system-design/34-data-at-scale/README.md) | Scaling a relational database: indexes, read replicas, partitioning, then sharding. Consistent hashing. Replication lag and read-your-writes. Choosing SQL vs document vs key-value vs column vs search. Event streaming with Kafka: log semantics, partitions, consumer groups. Batch vs stream pipelines. Schema evolution. | L4 E7 |
| 20 | [35 Reliability, Observability, and Security](course/part-6-system-design/35-reliability-observability-security/README.md) | Failure modes and blast radius. Timeouts, retries with jitter, circuit breakers, bulkheads. Rate limiting algorithms with real implementations. Logs, metrics, traces, and what each answers. SLIs, SLOs, error budgets. AuthN vs AuthZ. OWASP Top 10 in Python. Supply chain: pinning, auditing, SBOMs. Secrets handling. | L4 E6 |
| 20 | [36 Capstone](course/part-6-system-design/36-capstone/README.md) | Design, build, instrument, load-test, and document a complete service end to end. Written up as a design doc, defended against a review checklist. | P20 |

---

## Appendix (use throughout)

| Doc | Purpose |
|---|---|
| [Glossary](course/appendix/glossary.md) | Every term of art used in this course |
| [Idioms and Pitfalls](course/appendix/idioms-and-pitfalls.md) | 45 traps that bite every Python newcomer, with fixes |
| [Debugging and Tooling](course/appendix/debugging-and-tooling.md) | pdb, tracebacks, ruff, mypy, uv, profilers, and how to read them |
| [Testing Reference](course/appendix/testing.md) | pytest patterns, fixtures, mocking, and test design |
| [Interview Question Bank](course/appendix/interview-questions.md) | 120 questions with answers, sorted by topic and difficulty |
| [Resources](course/appendix/resources.md) | Books, docs, talks, and sites worth your time |
| [Cheatsheets](course/appendix/cheatsheets.md) | Complexity tables, dunder index, f-string formats, CLI one-liners |
| [Visual Guide](course/VISUAL-GUIDE.md) | How to turn each module into a NotebookLM video, mind map, and study guide |

---

## Checkpoints

Do not advance past these until you can do the thing described.

- **End of Part 1**: Write a multi-module CLI application that reads and writes
  files, validates input, exits with meaningful codes, and can be run with
  `python -m`. Explain aliasing to someone else using `id()`.
- **End of Part 2**: Design a class that supports `==`, `hash()`, ordering,
  iteration, `len()`, `in`, `with`, and a useful `repr`, and justify every
  dunder you implemented. Explain the MRO of a diamond without running it.
- **End of Part 3**: Ship a typed, tested, packaged library with a generator
  pipeline at its core and a decorator in its public API. mypy clean, 90 percent
  coverage.
- **End of Part 4**: Take a slow program, profile it, produce a hypothesis, fix
  it, and prove the fix with a benchmark. Correctly choose between thread, pool,
  and async for three different workloads.
- **End of Part 5**: Ship a FastAPI service with a real database, migrations,
  tests, a Dockerfile, and CI, and separately produce a reproducible analysis
  notebook that another person can rerun.
- **End of Part 6**: Present a design doc for a system with a stated load
  target, defend the storage choice, name three failure modes and their
  mitigations, and show load-test numbers from your own implementation.
