# Curriculum Map

The course is organised into four levels. Each level is a complete unit of
study with its own entry requirements, its own milestone, and its own exit
test. Learn them in the numbered order, or start at the level that matches
what you already know.

```
course/
├── 01-beginner/        12 modules   B01-B12   No prior programming assumed
├── 02-intermediate/    13 modules   01-13     Parts 1 and 2
├── 03-advanced/        17 modules   14-30     Parts 3, 4 and 5
├── 04-system-design/   16 modules   D01-D10, 31-36   Parts 6 and 7
└── 05-machine-learning/ 19 modules  M01-M19          Parts 8, 9, 10 and 11
```

Legend: **L** = lesson hours, **E** = exercise hours, **P** = project hours.

---

## Which level should you start in?

| If this describes you | Start at |
|---|---|
| You have never written code, or only copied snippets | 01 Beginner, Module B01 |
| You can write a loop and a function in some language, but not Python | 02 Intermediate, Module 01 |
| You write Python scripts daily but could not explain what `b = a` does to the object | 02 Intermediate, Module 02 |
| You are comfortable with classes, generators, and decorators | 03 Advanced, Module 14 |
| You write production Python and want scale, structure, and interview readiness | 04 System Design, Module D01 |
| You write production Python and want to build models, not call them | 05 Machine Learning, Module M01 |

Two honest self-tests before skipping a level. If you cannot explain why
`a = [1,2]; b = a; b.append(3)` changes `a` in terms of names and objects, do
not skip Intermediate. If you cannot say what `functools.wraps` protects, do
not skip Advanced.

---

## Time budget

| Level | Duration | Weekly load | Cumulative |
|---|---|---|---|
| 01 Beginner | 10 weeks | 6 to 8 hours | Week 10 |
| 02 Intermediate | 8 weeks | 10 to 15 hours | Week 18 |
| 03 Advanced | 12 weeks | 10 to 15 hours | Week 30 |
| 04 System Design | 10 weeks | 10 to 15 hours | Week 40 |
| 05 Machine Learning | 16 weeks | 10 to 15 hours | Week 56 |

Starting from zero, the full path is roughly fourteen months. Starting at
Intermediate it is nine months, and the original five-month shape of this
course is Levels 02 and 03 together.

Level 05 can be taken directly after Level 03. Level 04 is not a strict
prerequisite for it, though Modules M18 and M19 use its vocabulary.

---

# Level 01 — Beginner

**Folder:** [`course/01-beginner/`](course/01-beginner/README.md)

Goal: turn someone who has never programmed into someone who can write, run,
debug, and finish a small program on their own. No prior experience assumed and
nothing hand-waved. Every idea here is taught in a way that stays true when the
Intermediate level makes it precise.

| Wk | Module | Topics | Time |
|---|---|---|---|
| 1 | [B01 Your First Program and How Python Runs It](course/01-beginner/b01-first-program-and-the-interpreter/README.md) | What a program is. Installing Python. Terminal basics. The REPL, files, and the editor. print. First traceback, read bottom up. | L2 E3 |
| 1-2 | [B02 Data, Names, and Types](course/01-beginner/b02-data-names-and-types/README.md) | Names as labels, not boxes. int, float, str, bool, None. Conversion. input always gives text. f-strings. Naming well. | L3 E5 |
| 2-3 | [B03 Making Decisions](course/01-beginner/b03-making-decisions/README.md) | Comparisons. if, elif, else. Indentation as syntax. and, or, not, short-circuiting. Truthiness. Flattening nested conditions. A first look at match. | L3 E5 |
| 3-4 | [B04 Repeating Work: Loops](course/01-beginner/b04-loops-and-repetition/README.md) | for over items, not indexes. range. while. The accumulator pattern. break, continue, enumerate, zip. Nested loops. | L3 E6 |
| 4-5 | [B05 Collections](course/01-beginner/b05-collections/README.md) | list, dict, set, tuple, each with a job description. Choosing a container. Nesting. A first look at aliasing. | L4 E6 |
| 5-6 | [B06 Functions](course/01-beginner/b06-functions/README.md) | def, parameters, return versus print. Defaults and keyword arguments. Docstrings. Local scope. Type hints as documentation. Designing small functions. | L4 E6 |
| 6-7 | [B07 Working with Text](course/01-beginner/b07-working-with-text/README.md) | Strings are immutable. The method toolkit. split and join. Slicing. Formatted output. Escapes and raw strings. | L3 E5 |
| 7-8 | [B08 Files and Folders](course/01-beginner/b08-files-and-folders/README.md) | Reading and writing with `with`. pathlib. CSV as a list of dicts. JSON round trips. Failing safely and atomic writes. | L3 E5 |
| 8 | [B09 Errors and Debugging](course/01-beginner/b09-errors-and-debugging/README.md) | The six exceptions you will meet. Reading a traceback. Narrow try and except. Raising your own. breakpoint. Shrinking a bug. | L3 E5 |
| 9 | [B10 Organising Code](course/01-beginner/b10-organising-code/README.md) | Splitting files. import. The main guard. A stdlib tour. Virtual environments. Installing packages safely. | L3 E5 |
| 9-10 | [B11 A First Look at Objects and Classes](course/01-beginner/b11-first-look-at-classes/README.md) | You have used objects all along. class, `__init__`, self, methods, `__repr__`. When not to use a class. A first dataclass. | L3 E5 |
| 10 | [B12 Milestone Project: Expense Tracker CLI](course/01-beginner/b12-project-expense-tracker/README.md) | A complete program in six runnable stages: memory, persistence, validation, reporting, argparse, package layout. | P10 |

**Exit test.** Build a small program of your own choosing that takes input,
stores it in a file, survives a restart, validates every input, and prints a
report. Explain each of your functions in one sentence.

---

# Level 02 — Intermediate

**Folder:** [`course/02-intermediate/`](course/02-intermediate/README.md)

Goal: understand what the interpreter is actually doing, and model problems
with types the Python way. This level assumes you can already write a loop and
a function, whether you learned that here or elsewhere.

## Part 1 — Foundations (Weeks 1-4 of this level)

| Wk | Module | Topics | Time |
|---|---|---|---|
| 1 | [01 The Runtime and the Toolchain](course/02-intermediate/part-1-foundations/01-runtime-and-toolchain/README.md) | CPython vs Python. Source to bytecode to eval loop. `__pycache__`. Interpreters (CPython, PyPy, MicroPython). Virtual environments, `pip`, `uv`, lockfiles. Script vs module vs package. `sys.path`. The REPL as a laboratory. Reading a traceback. | L3 E4 |
| 1-2 | [02 Objects, Names, and the Data Model](course/02-intermediate/part-1-foundations/02-objects-names-data-model/README.md) | Everything is an object. Names are bindings, not boxes. Identity vs equality. Mutability and aliasing. Reference counting and the cycle collector. Small-int and string interning. Shallow vs deep copy. Truthiness. `None`. | L5 E6 |
| 2 | [03 Core Types and Their Behaviour](course/02-intermediate/part-1-foundations/03-core-types/README.md) | `int` (arbitrary precision), `float` (IEEE 754 traps), `Decimal`, `Fraction`, `bool`. `str` vs `bytes` and the encoding boundary. f-strings and the format mini-language. Slicing. Hashability. `list`, `tuple`, `dict`, `set` at a glance. | L5 E6 |
| 2-3 | [04 Control Flow, Functions, and Scope](course/02-intermediate/part-1-foundations/04-control-flow-and-functions/README.md) | Statements vs expressions. `for`/`else`, `while`/`else`, the walrus operator, `match`. Functions as objects. Positional-only and keyword-only params, `*args`/`**kwargs`, defaults and the mutable-default trap. LEGB scope, `global`, `nonlocal`, closures. Type hints as documentation that runs. | L5 E7 |
| 3 | [05 Collections in Depth and Comprehensions](course/02-intermediate/part-1-foundations/05-collections-and-comprehensions/README.md) | `list` growth and complexity. `dict` insertion order and hashing. `set` algebra. Comprehensions and generator expressions. Sorting with `key`, stability, `operator`. `collections`: `Counter`, `defaultdict`, `deque`, `namedtuple`, `ChainMap`. Choosing the right container. | L4 E7 |
| 3-4 | [06 Modules, Packages, and Project Layout](course/02-intermediate/part-1-foundations/06-modules-packages-projects/README.md) | The import system end to end. Absolute vs relative imports. `__init__.py`, namespace packages. `__main__` and `python -m`. Circular imports and how to break them. The src layout. `pyproject.toml` first contact. Where config and secrets go. | L4 E5 |
| 4 | [07 Milestone Project: Inventory CLI](course/02-intermediate/part-1-foundations/07-project-inventory-cli/README.md) | A complete multi-module command-line application: `argparse`, JSON persistence, input validation, structured errors, exit codes, and a test script. | P12 |

## Part 2 — Object-Oriented Python (Weeks 5-8 of this level)

| Wk | Module | Topics | Time |
|---|---|---|---|
| 5 | [08 Classes and Encapsulation](course/02-intermediate/part-2-oop/08-classes-and-encapsulation/README.md) | The class body as executable code. Instance vs class attributes and the shared-mutable trap. `self`. Bound methods. `@property`, setters, computed attributes. `_private` convention and `__name` mangling. `@classmethod` factories, `@staticmethod`. `__slots__`. | L5 E7 |
| 5-6 | [09 The Data Model: Dunder Methods](course/02-intermediate/part-2-oop/09-dunder-and-data-model/README.md) | `__repr__` vs `__str__`. `__eq__` and `__hash__` as a pair. Ordering and `functools.total_ordering`. Container protocol: `__len__`, `__getitem__`, `__contains__`, `__iter__`. `__call__`. Arithmetic and reflected operators. Context managers: `__enter__`/`__exit__`. `__getattr__` vs `__getattribute__`. | L6 E8 |
| 6-7 | [10 Inheritance, Composition, and the MRO](course/02-intermediate/part-2-oop/10-inheritance-composition-mro/README.md) | Has-a vs is-a. `super()` is not "the parent class". C3 linearisation and the diamond. Cooperative multiple inheritance and mixins. Abstract base classes. `Protocol` and structural typing. Duck typing and when to stop using `isinstance`. | L6 E8 |
| 7 | [11 Dataclasses, Enums, and Value Semantics](course/02-intermediate/part-2-oop/11-dataclasses-and-value-semantics/README.md) | `@dataclass`, `field`, `frozen`, `slots`, `__post_init__`, ordering. `NamedTuple` vs `TypedDict` vs `dataclass` vs `dict`. `Enum`, `IntEnum`, `StrEnum`, `auto`. Pydantic as validating dataclasses. Copy semantics and immutability as a design tool. | L4 E6 |
| 8 | [12 Design Principles in Python](course/02-intermediate/part-2-oop/12-design-principles-in-python/README.md) | SOLID translated into a language with first-class functions. Composition over inheritance in practice. Dependency injection without a framework. Descriptors, the mechanism under `@property`. `__init_subclass__`, class decorators, metaclasses and when never to use them. Design patterns that Python dissolves. | L5 E6 |
| 8 | [13 Milestone Project: Plugin Document Pipeline](course/02-intermediate/part-2-oop/13-project-plugin-pipeline/README.md) | A polymorphic processing pipeline with a plugin registry, protocol-based extensibility, serialization, and a full pytest suite. | P12 |

**Exit test.** Write a multi-module CLI application that reads and writes files,
validates input, exits with meaningful codes, and runs with `python -m`. Design
a class that supports `==`, `hash()`, ordering, iteration, `len()`, `in`, `with`,
and a useful `repr`, and justify every dunder you implemented. Explain the MRO
of a diamond without running it.

---

# Level 03 — Advanced

**Folder:** [`course/03-advanced/`](course/03-advanced/README.md)

Goal: write Python a senior engineer would approve in review, reason about
concurrency and speed with evidence, and ship real applications.

## Part 3 — Idiomatic and Advanced Python (Weeks 1-5 of this level)

| Wk | Module | Topics | Time |
|---|---|---|---|
| 1 | [14 Iterators, Generators, and Lazy Pipelines](course/03-advanced/part-3-advanced/14-iterators-and-generators/README.md) | The iterator protocol. Writing `__iter__`/`__next__`. Generator functions and generator expressions. `yield from`. Generators as coroutines (`send`, `throw`, `close`). `itertools` as a composable toolkit. Streaming a file larger than RAM. | L5 E8 |
| 1-2 | [15 Decorators, Closures, and functools](course/03-advanced/part-3-advanced/15-decorators-closures-functools/README.md) | Closures and cell variables. Decorators with and without arguments. `functools.wraps` and why bare decorators break introspection. `lru_cache`/`cache`, `partial`, `singledispatch`, `cached_property`, `reduce`. Class decorators. `contextlib` and `@contextmanager`. Stacking order. | L5 E7 |
| 2-3 | [16 Error Handling and Robustness](course/03-advanced/part-3-advanced/16-error-handling-and-robustness/README.md) | The exception hierarchy. `try/except/else/finally` semantics precisely. Custom exception design. Chaining with `raise ... from`. EAFP vs LBYL. `ExceptionGroup` and `except*`. Context managers for cleanup. `logging` done properly. Retries, timeouts, and backoff. What never to catch. | L5 E7 |
| 3-4 | [17 Typing and Static Analysis](course/03-advanced/part-3-advanced/17-typing-and-static-analysis/README.md) | Gradual typing strategy. Built-in generics, `Optional`, unions, `Literal`, `Final`. `TypeVar`, generic classes, PEP 695 syntax. `Protocol`, `overload`, `TypedDict`, `NewType`, `Self`. Variance in one page. mypy and pyright configuration. Runtime validation vs static types. Typing a real codebase incrementally. | L5 E7 |
| 4 | [18 Testing, Debugging, and Quality](course/03-advanced/part-3-advanced/18-testing-and-quality/README.md) | pytest: assertions, fixtures, scope, `parametrize`, markers, `conftest.py`. Test doubles: `unittest.mock`, `monkeypatch`, fakes vs mocks. Coverage and what it does not tell you. Property-based testing with Hypothesis. `pdb`/`breakpoint()`. `ruff`, formatting, pre-commit. Designing code for testability. | L5 E8 |
| 4-5 | [19 The Standard Library, Files, and Serialization](course/03-advanced/part-3-advanced/19-stdlib-files-serialization/README.md) | `pathlib` over `os.path`. Text vs binary I/O and encodings. `json`, `csv`, `sqlite3`, `pickle` (and its dangers), `struct`, `tomllib`. `datetime`, timezones, and the aware/naive rule. `re` at working depth. `subprocess` safely. `argparse`. `random` vs `secrets`. | L5 E7 |
| 5 | [20 Milestone Project: A Packaged Library and CLI](course/03-advanced/part-3-advanced/20-project-library-and-cli/README.md) | Build a real library end to end: a streaming log-analysis engine with a plugin API, full type coverage, 90 percent test coverage, a CLI front end, and a publishable `pyproject.toml`. | P14 |

## Part 4 — Concurrency, Performance, and Internals (Weeks 6-7 of this level)

| Wk | Module | Topics | Time |
|---|---|---|---|
| 6 | [21 The GIL, Threads, and Processes](course/03-advanced/part-4-concurrency/21-gil-threads-processes/README.md) | What the GIL actually locks. Why threads still help for I/O. `threading`, `Lock`, `RLock`, `Event`, `Queue`. Race conditions and atomicity in Python. `multiprocessing`, pickling boundaries, shared memory. `concurrent.futures` as the unified front end. Free-threaded CPython (PEP 703) and what changes. | L5 E7 |
| 6 | [22 Asyncio](course/03-advanced/part-4-concurrency/22-asyncio/README.md) | The event loop as a scheduler. Coroutines, awaitables, tasks. `gather` vs `TaskGroup`. Cancellation and timeouts. Async context managers and iterators. Blocking the loop: the number one asyncio bug. `run_in_executor`. Async clients (`httpx`, `asyncpg`). Structured concurrency. Debugging async. | L5 E8 |
| 7 | [23 Performance and Profiling](course/03-advanced/part-4-concurrency/23-performance-and-profiling/README.md) | Measure before you change. `timeit` correctly. `cProfile`, `pstats`, flame graphs, `py-spy`. Memory: `tracemalloc`, `__slots__`, generators. Algorithmic vs interpreter overhead. Vectorising with NumPy. When to reach for C, Cython, or Rust. Caching strategies. Knowing when to stop. | L4 E6 |
| 7 | [24 CPython Internals](course/03-advanced/part-4-concurrency/24-cpython-internals/README.md) | `dis` and reading bytecode. Frames, code objects, the eval loop. How attribute lookup really resolves (type, MRO, descriptors, `__dict__`). Memory layout, arenas, and why an `int` is 28 bytes. Interning. What the 3.11+ specialising adaptive interpreter does. Reading CPython source. | L4 E5 |

## Part 5 — Applied Python (Weeks 8-12 of this level)

| Wk | Module | Topics | Time |
|---|---|---|---|
| 8 | [25 Automation, Scripting, and the OS](course/03-advanced/part-5-applied/25-automation-and-os/README.md) | Robust scripts: exit codes, signals, idempotency, dry-run. `pathlib` recipes, atomic writes, file locking, temp files. `subprocess` pipelines. Environment and config. Building real CLIs with `argparse` and Typer. Scheduling with cron and systemd timers. Watching filesystems. Writing scripts other people can run. | L4 E7 |
| 8-9 | [26 HTTP, APIs, and Scraping](course/03-advanced/part-5-applied/26-http-and-scraping/README.md) | HTTP as a protocol, not a library call. `httpx` sessions, timeouts, retries, connection pooling. REST and pagination. Auth: API keys, bearer tokens, OAuth2 flow. Rate limiting and politeness. Parsing HTML with selectolax/BeautifulSoup. `robots.txt`, ToS, and the ethics line. Caching responses. | L4 E7 |
| 9-10 | [27 Databases and Persistence](course/03-advanced/part-5-applied/27-databases-and-persistence/README.md) | SQL you must know: joins, indexes, `EXPLAIN`. DB-API 2.0 and `sqlite3`. Parameterised queries and SQL injection. Transactions and isolation levels. SQLAlchemy Core vs ORM. Sessions, the identity map, and the N+1 problem. Migrations with Alembic. Connection pooling. When Redis or a document store is the right answer. | L5 E8 |
| 10-11 | [28 Building APIs with FastAPI](course/03-advanced/part-5-applied/28-apis-with-fastapi/README.md) | ASGI. Routing, path/query/body params. Pydantic v2 models as the contract. Dependency injection. Async endpoints and the sync escape hatch. Errors and consistent error shape. Auth with JWT. Middleware and CORS. Background tasks. Testing with `TestClient`. Auto-generated OpenAPI. Project structure that survives growth. | L5 E9 |
| 11-12 | [29 Data and ML Foundations](course/03-advanced/part-5-applied/29-data-and-ml-foundations/README.md) | NumPy: ndarray, dtypes, broadcasting, views vs copies, vectorised thinking. pandas: Series/DataFrame, indexing, `groupby`, joins, reshaping, time series, the memory traps. Cleaning real data. Plotting for insight. scikit-learn: the estimator API, pipelines, train/test discipline, leakage, metrics that match the problem. Reproducibility. | L6 E10 |
| 12 | [30 Packaging, Deployment, and Ops](course/03-advanced/part-5-applied/30-packaging-and-deployment/README.md) | `pyproject.toml` in full. Build backends, wheels vs sdists, editable installs. Dependency resolution and lockfiles. Versioning and changelogs. Publishing to PyPI. Dockerising Python properly (multi-stage, non-root, layer caching). 12-factor config and secrets. CI with GitHub Actions. Health checks and graceful shutdown. | L5 E7 |

**Exit test.** Ship a typed, tested, packaged library with a generator pipeline
at its core and a decorator in its public API, mypy clean at 90 percent
coverage. Profile a slow program, form a hypothesis, fix it, and prove the fix
with a benchmark. Ship a FastAPI service with a real database, migrations,
tests, a Dockerfile, and CI.

---

# Level 04 — System Design

**Folder:** [`course/04-system-design/`](course/04-system-design/README.md)

Goal: build systems, not just programs. This level starts with data structures
and algorithms, because you cannot estimate a system whose primitives you
cannot cost, and then moves to architecture. Every design module ends with an
exercise written the way an interview or a design doc would pose it.

## Part 6 — Data Structures and Algorithms (Weeks 1-5 of this level)

| Wk | Module | Topics | Time |
|---|---|---|---|
| 1 | [D01 Complexity and Measuring Cost](course/04-system-design/part-6-data-structures-and-algorithms/d01-complexity-and-measurement/README.md) | Counting operations. The common growth classes. Worst, average, and amortised. Space complexity. Measuring with timeit instead of assuming. When theory misleads at small n. Turning complexity into a capacity statement. | L4 E5 |
| 1 | [D02 Arrays and Dynamic Arrays](course/04-system-design/part-6-data-structures-and-algorithms/d02-arrays-and-dynamic-arrays/README.md) | Contiguous memory. What a Python list really is. Growth policy and over-allocation. Why the front end is linear. Slicing copies. array and NumPy. Two pointers, sliding window, prefix sums. | L3 E5 |
| 2 | [D03 Hash Tables](course/04-system-design/part-6-data-structures-and-algorithms/d03-hash-tables/README.md) | Hashing and slots. Collisions, chaining vs open addressing, the compact dict. Load factor and resizing. Hashability. The eq and hash contract. Sets. When a sorted structure beats a dict. | L4 E6 |
| 2 | [D04 Linked Lists, Stacks, and Queues](course/04-system-design/part-6-data-structures-and-algorithms/d04-linked-structures/README.md) | Nodes and sentinels. Singly and doubly linked operations. Cycle detection. Array versus linked, honestly. Stacks and queues. Building an LRU cache. | L3 E5 |
| 3 | [D05 Trees and Heaps](course/04-system-design/part-6-data-structures-and-algorithms/d05-trees-and-heaps/README.md) | BST invariant, insert, search, the three delete cases. The four traversals. Balance and what it guarantees. Heaps and heapq. B-trees and why a database index is shallow and wide. | L4 E6 |
| 3 | [D06 Graphs](course/04-system-design/part-6-data-structures-and-algorithms/d06-graphs/README.md) | Modelling with graphs. Three representations and their costs. BFS and DFS. Topological sort and cycle detection. Dijkstra with a heap. Graphs in deployment, tracing, and hashing rings. | L5 E7 |
| 4 | [D07 Sorting and Searching](course/04-system-design/part-6-data-structures-and-algorithms/d07-sorting-and-searching/README.md) | The n log n lower bound. Merge, quick, and heap sort. Timsort and why Python chose it. key functions and stability. Binary search and bisect. Counting and radix. External and distributed sorting. | L4 E5 |
| 4 | [D08 Recursion, Backtracking, and Divide and Conquer](course/04-system-design/part-6-data-structures-and-algorithms/d08-recursion-and-divide-and-conquer/README.md) | The recursive contract. The call stack and RecursionError. Divide and conquer. Recursion on trees and graphs. Backtracking with pruning. Converting to iteration. Why naive recursion goes exponential. | L4 E6 |
| 5 | [D09 Dynamic Programming and Greedy](course/04-system-design/part-6-data-structures-and-algorithms/d09-dynamic-programming-and-greedy/README.md) | Optimal substructure and overlapping subproblems. Memoisation then tabulation. The classic problem set as state plus recurrence. Space optimisation. Reconstructing the answer. The exchange argument and where greedy fails. | L5 E7 |
| 5 | [D10 Patterns, Drills, and the Bridge to System Design](course/04-system-design/part-6-data-structures-and-algorithms/d10-patterns-and-design-bridge/README.md) | The pattern catalogue and how to recognise each. Communicating a solution. The structures behind hash rings, indexes, LSM trees, tries, and inverted indexes. Bloom filters and sketches. Union find. | L3 E8 |

## Part 7 — System Design with Python (Weeks 6-10 of this level)

| Wk | Module | Topics | Time |
|---|---|---|---|
| 6 | [31 Design Fundamentals](course/04-system-design/part-7-system-design/31-design-fundamentals/README.md) | Requirements: functional, non-functional, and the questions to ask. Back-of-envelope estimation and the latency numbers to memorise. Throughput vs latency vs concurrency (Little's Law). CAP and PACELC honestly. Consistency models. Availability math. The design interview framework, step by step. | L4 E5 |
| 7 | [32 Service Architecture and Concurrency Models](course/04-system-design/part-7-system-design/32-service-architecture/README.md) | WSGI vs ASGI. Process and worker models: gunicorn, uvicorn, workers vs threads vs async. Where Python's concurrency model constrains architecture. Load balancing, statelessness, sticky sessions. Backpressure and queueing theory in practice. Graceful shutdown and zero-downtime deploys. Monolith, modular monolith, microservices. | L4 E7 |
| 8 | [33 Caching, Queues, and Background Jobs](course/04-system-design/part-7-system-design/33-caching-queues-jobs/README.md) | Cache layers and where to put them. Cache-aside, write-through, write-behind. Invalidation, TTLs, stampedes, and the thundering herd. Redis data structures beyond GET/SET. Task queues: Celery, RQ, arq, and the tradeoffs. Idempotency keys, retries, dead-letter queues, exactly-once as a myth. Scheduled work at scale. | L4 E7 |
| 8-9 | [34 Data at Scale](course/04-system-design/part-7-system-design/34-data-at-scale/README.md) | Scaling a relational database: indexes, read replicas, partitioning, then sharding. Consistent hashing. Replication lag and read-your-writes. Choosing SQL vs document vs key-value vs column vs search. Event streaming with Kafka: log semantics, partitions, consumer groups. Batch vs stream pipelines. Schema evolution. | L4 E7 |
| 9 | [35 Reliability, Observability, and Security](course/04-system-design/part-7-system-design/35-reliability-observability-security/README.md) | Failure modes and blast radius. Timeouts, retries with jitter, circuit breakers, bulkheads. Rate limiting algorithms with real implementations. Logs, metrics, traces, and what each answers. SLIs, SLOs, error budgets. AuthN vs AuthZ. OWASP Top 10 in Python. Supply chain: pinning, auditing, SBOMs. Secrets handling. | L4 E6 |
| 10 | [36 Capstone](course/04-system-design/part-7-system-design/36-capstone/README.md) | Design, build, instrument, load-test, and document a complete service end to end. Written up as a design doc, defended against a review checklist. | P20 |

**Exit test.** Present a design doc for a system with a stated load target,
defend the storage choice, name three failure modes and their mitigations, and
show load-test numbers from your own implementation. Separately, solve a timed
algorithm problem while stating the pattern, the complexity, and the trade
before writing code.

---

# Level 05 — Machine Learning

**Folder:** [`course/05-machine-learning/`](course/05-machine-learning/README.md)

Goal: build models rather than call them. Every architecture is implemented from
parts and verified against the library version before the library is allowed to
do the work. PyTorch throughout, with the Hugging Face stack layered on from
Module M16. Advanced Module 29 supplies the NumPy and pandas groundwork and is
the prerequisite.

## Part 8 — Foundations of Learning (Weeks 1-3 of this level)

| Wk | Module | Topics | Time |
|---|---|---|---|
| 1 | [M01 What Learning Is](course/05-machine-learning/part-8-ml-foundations/m01-what-learning-is/README.md) | Hypothesis space, loss, optimiser. What a loss encodes. Generalisation and the three splits. Bias and variance from learning curves. Splitting honestly. Leakage. When not to use machine learning. | L4 E5 |
| 1-2 | [M02 The Maths You Will Actually Use](course/05-machine-learning/part-8-ml-foundations/m02-the-maths-you-will-use/README.md) | Shapes and matmul. The dot product as similarity. Chain rule and gradients of the operations you use. Probability, maximum likelihood, and where squared error and cross entropy come from. Optimisation geometry. Build a scalar autodiff engine. | L5 E6 |
| 2 | [M03 Linear Models and Gradient Descent](course/05-machine-learning/part-8-ml-foundations/m03-linear-models-and-gradient-descent/README.md) | Linear and logistic regression implemented from scratch. Gradient descent, learning rates, and the three loss-curve failures. Batch, stochastic, mini-batch. Feature scaling. L1 and L2. | L4 E6 |
| 3 | [M04 Evaluation and the Experimental Loop](course/05-machine-learning/part-8-ml-foundations/m04-evaluation-and-the-experimental-loop/README.md) | Metrics as decisions. Imbalance and thresholds. Calibration. Cross validation including grouped and temporal. Error analysis. Baselines and ablations. Reproducibility and an experiment harness. | L4 E6 |

## Part 9 — Deep Learning with PyTorch (Weeks 4-8 of this level)

| Wk | Module | Topics | Time |
|---|---|---|---|
| 4 | [M05 Tensors and Autograd](course/05-machine-learning/part-9-deep-learning/m05-tensors-and-autograd/README.md) | Tensors, dtypes, devices, views, broadcasting. The autograd graph, backward, gradient accumulation. no_grad and detach. The training loop written out line by line. | L4 E6 |
| 4-5 | [M06 Neural Networks, Derived and Built](course/05-machine-learning/part-9-deep-learning/m06-neural-networks/README.md) | Why a non-linearity. Activations. Backpropagation derived by hand and implemented in NumPy. nn.Module. Initialisation. Optimisers from SGD to AdamW. Parameter counts from shapes. | L5 E7 |
| 5-6 | [M07 Training That Actually Works](course/05-machine-learning/part-9-deep-learning/m07-training-that-works/README.md) | The overfitting toolkit. Batch, layer, and RMS norm. Learning rate schedules and warmup. The ordered checklist for a stuck run. Vanishing and exploding gradients. Data pipelines. Mixed precision and speed. | L5 E7 |
| 6-7 | [M08 Convolutional Networks and Vision](course/05-machine-learning/part-9-deep-learning/m08-convolutional-networks-and-vision/README.md) | Convolution as a prior. Stride, padding, channels, receptive field. Pooling. LeNet to ResNet and the residual connection. Transfer learning and fine tuning. Augmentation that respects the label. | L4 E7 |
| 7 | [M09 Sequences, Recurrence, and the Road to Attention](course/05-machine-learning/part-9-deep-learning/m09-sequences-and-attention/README.md) | RNNs and backpropagation through time. Vanishing gradients and LSTM gates. The two walls recurrence hits. Embeddings. Scaled dot-product attention derived as the fix. | L4 E6 |
| 8 | [M10 The Transformer, Built from Parts](course/05-machine-learning/part-9-deep-learning/m10-the-transformer/README.md) | Multi-head attention from scratch. Causal and padding masks. The block, residuals, pre-norm versus post-norm. Positional encodings including rotary. Encoder, decoder, and both. The quadratic cost. Verified against PyTorch and run with real pretrained weights. | L5 E8 |

## Part 10 — Generative Models (Weeks 9-11 of this level)

| Wk | Module | Topics | Time |
|---|---|---|---|
| 9 | [M11 Autoencoders and VAEs](course/05-machine-learning/part-10-generative-models/m11-autoencoders-and-vaes/README.md) | Encoder, bottleneck, decoder. Why sampling from a plain autoencoder fails. The ELBO derived. The reparameterisation trick. Latent interpolation and the beta trade. Posterior collapse and blurriness. | L4 E6 |
| 10 | [M12 Generative Adversarial Networks](course/05-machine-learning/part-10-generative-models/m12-gans/README.md) | The minimax game and the learned loss. DCGAN. Mode collapse, discriminator dominance, oscillation. Wasserstein loss, gradient penalty, spectral norm. Conditional generation. FID and honest evaluation. | L5 E7 |
| 11 | [M13 Diffusion Models](course/05-machine-learning/part-10-generative-models/m13-diffusion-models/README.md) | Many small denoising steps instead of one leap. The forward process and its closed form. Predicting the noise. U-Net with timestep conditioning. DDPM and DDIM sampling. Classifier-free guidance. Latent diffusion. | L5 E7 |

## Part 11 — Language Models and LLMs (Weeks 12-16 of this level)

| Wk | Module | Topics | Time |
|---|---|---|---|
| 12 | [M14 Tokenisation and Language Modelling](course/05-machine-learning/part-11-language-models/m14-tokenisation-and-language-modelling/README.md) | Byte pair encoding implemented from scratch. Special tokens and chat templates. Why tokenisation explains the famous failures. Next-token prediction and teacher forcing. Perplexity. Temperature, top-k, top-p. | L4 E6 |
| 12-13 | [M15 Build a Mini LLM from Scratch](course/05-machine-learning/part-11-language-models/m15-build-a-mini-llm/README.md) | A decoder-only transformer specified in full. Corpus cleaning, deduplication, packing. A stable pretraining run with checkpointing and resumption. Scaling laws applied to your budget. KV cache generation. An honest evaluation. | P16 |
| 14 | [M16 Pretrained Models and the Open Ecosystem](course/05-machine-learning/part-11-language-models/m16-pretrained-models-and-the-ecosystem/README.md) | Base versus instruction-tuned. Memory arithmetic before loading. The library mapped onto what you built. Batching, padding side, streaming. 8-bit and 4-bit quantisation measured. Datasets, licences, and reading a model card critically. | L4 E6 |
| 15 | [M17 Fine-tuning and Alignment](course/05-machine-learning/part-11-language-models/m17-fine-tuning-and-alignment/README.md) | The cost ladder: prompt, few-shot, retrieval, fine-tune. Building an instruction dataset. Full fine-tuning memory computed explicitly. LoRA and QLoRA. Prompt masking. RLHF in outline and DPO in detail. Regression suites and catastrophic forgetting. | L5 E9 |
| 16 | [M18 Serving, Evaluation, and Cost](course/05-machine-learning/part-11-language-models/m18-serving-evaluation-and-cost/README.md) | Prefill versus decode. KV cache memory, continuous batching, paged attention, speculative decoding. A streaming FastAPI service. Retrieval augmentation and its limits. Evaluation suites that gate a release. Monitoring and drift. Cost per thousand requests. | L4 E7 |
| 16 | [M19 Capstone](course/05-machine-learning/part-11-language-models/m19-capstone/README.md) | One project end to end: specification, dataset, evaluation before model, the modelling ladder, a deployed service with monitoring, and a design document defended against a review checklist. | P24 |

**Exit test.** Implement attention and a transformer block from tensors and match
the reference numerically. Pretrain a small language model on a corpus you
prepared and account for where the compute went. Fine-tune a larger model under
a fixed memory budget, prove the gain against a baseline you set beforehand, and
show what capability it lost. Serve it with a latency budget and a cost model.

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
