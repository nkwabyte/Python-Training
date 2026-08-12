# Level 03 — Advanced

**Start here if you are comfortable with classes, the data model, and packages,
and you now want code that survives review, load, and other people.**

Three parts: the idioms that make Python code good, the internals that make it
fast or slow, and the applied work that makes it useful.

| | |
|---|---|
| Modules | 14 to 30, in Parts 3, 4, and 5 |
| Duration | 12 weeks |
| Weekly load | 10 to 15 hours |
| Prerequisite | Level 02, or fluency with classes, generators, and imports |
| Ends with | A packaged library, a profiled optimisation, and a deployed API |

---

## Part 3 — Idiomatic and Advanced Python

| Module | Title |
|---|---|
| [14](part-3-advanced/14-iterators-and-generators/README.md) | Iterators, Generators, and Lazy Pipelines |
| [15](part-3-advanced/15-decorators-closures-functools/README.md) | Decorators, Closures, and functools |
| [16](part-3-advanced/16-error-handling-and-robustness/README.md) | Error Handling and Robustness |
| [17](part-3-advanced/17-typing-and-static-analysis/README.md) | Typing and Static Analysis |
| [18](part-3-advanced/18-testing-and-quality/README.md) | Testing, Debugging, and Quality |
| [19](part-3-advanced/19-stdlib-files-serialization/README.md) | The Standard Library, Files, and Serialization |
| [20](part-3-advanced/20-project-library-and-cli/README.md) | Milestone Project: A Packaged Library and CLI |

## Part 4 — Concurrency, Performance, and Internals

| Module | Title |
|---|---|
| [21](part-4-concurrency/21-gil-threads-processes/README.md) | The GIL, Threads, and Processes |
| [22](part-4-concurrency/22-asyncio/README.md) | Asyncio |
| [23](part-4-concurrency/23-performance-and-profiling/README.md) | Performance and Profiling |
| [24](part-4-concurrency/24-cpython-internals/README.md) | CPython Internals |

## Part 5 — Applied Python

| Module | Title |
|---|---|
| [25](part-5-applied/25-automation-and-os/README.md) | Automation, Scripting, and the OS |
| [26](part-5-applied/26-http-and-scraping/README.md) | HTTP, APIs, and Scraping |
| [27](part-5-applied/27-databases-and-persistence/README.md) | Databases and Persistence |
| [28](part-5-applied/28-apis-with-fastapi/README.md) | Building APIs with FastAPI |
| [29](part-5-applied/29-data-and-ml-foundations/README.md) | Data and ML Foundations |
| [30](part-5-applied/30-packaging-and-deployment/README.md) | Packaging, Deployment, and Ops |

---

## The rule that governs this level

Every performance claim is measured, never estimated. Every concurrency choice
is defended against the GIL. Every applied module ships something that runs,
with tests, because applied Python that is not tested is a demo rather than
software.

## When you are ready to move on

You are ready for [Level 04 System Design](../04-system-design/README.md) when
you can profile a slow program and prove your fix with a benchmark, choose
correctly between threads, processes, and asyncio for three different
workloads, and ship a FastAPI service with a database, migrations, tests, and
CI.
