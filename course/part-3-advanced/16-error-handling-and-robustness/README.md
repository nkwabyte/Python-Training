# Module 16 — Error Handling and Robustness

**Time budget:** 5 hours lesson, 7 hours exercises
**Prerequisite:** Modules 09, 14, 15

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

Error handling is where the difference between working code and production code
lives. Most Python codebases get it wrong in the same four ways: catching too
broadly, losing the original cause, raising messages that do not identify the
input, and retrying operations that must not be retried.

---

## 1. The exception hierarchy

```
BaseException
├── SystemExit              raised by sys.exit() and SystemExit
├── KeyboardInterrupt       Ctrl-C
├── GeneratorExit           generator.close()
└── Exception               <- everything you should ever catch
    ├── ArithmeticError → ZeroDivisionError, OverflowError
    ├── LookupError      → IndexError, KeyError
    ├── OSError          → FileNotFoundError, PermissionError,
    │                        ConnectionError, TimeoutError, IsADirectoryError
    ├── ValueError       → UnicodeDecodeError
    ├── TypeError, AttributeError, NameError, ImportError
    ├── RuntimeError     → RecursionError, NotImplementedError
    └── StopIteration, StopAsyncIteration
```

**The three under `BaseException` and not `Exception` are there deliberately.**
`except Exception:` does not catch `KeyboardInterrupt` or `SystemExit`, which
is exactly what you want — Ctrl-C should stop your program even inside a retry
loop, and `sys.exit()` should exit.

Which is why:

```python
except:                     # NEVER. Catches Ctrl-C and SystemExit.
except BaseException:       # almost never. Same problem, more explicit.
except Exception:           # the outermost handler of a long-running process
except (OSError, ValueError):   # what you should usually write
```

**Catch the narrowest exception you can actually handle.** "Handle" means: you
can do something about it. Logging and re-raising is not handling; it is
duplicating what the traceback already says.

---

## 2. `try/except/else/finally`, precisely

```python
try:
    result = risky()
except ValueError as exc:
    handle(exc)
else:
    use(result)          # runs ONLY if no exception was raised
finally:
    cleanup()            # runs ALWAYS: success, exception, return, break
```

**`else` exists to keep the `try` block minimal.** Compare:

```python
try:
    value = d[key]
    process(value)          # if THIS raises KeyError, it is caught by mistake
except KeyError:
    ...

try:
    value = d[key]
except KeyError:
    ...
else:
    process(value)          # its KeyErrors are NOT caught here
```

The first version silently swallows an unrelated `KeyError` from deep inside
`process`, and you get the "key not found" branch for a completely different
reason. **Put exactly the line that can raise inside the `try`.**

**`finally` runs even on `return`**, which produces one genuine surprise:

```python
def f():
    try:
        return "from try"
    finally:
        return "from finally"     # this WINS, and discards the exception too
```

A `return` in `finally` swallows any in-flight exception. Never do it; linters
flag it (`ruff` rule `B012`).

---

## 3. Exception chaining

```python
try:
    config = json.loads(raw)
except json.JSONDecodeError as exc:
    raise ConfigError(f"{path} is not valid JSON") from exc      # EXPLICIT
```

| Form | Traceback says | Meaning |
|---|---|---|
| `raise New() from exc` | "The above exception was the **direct cause**" | Deliberate translation |
| `raise New()` inside `except` | "During handling ... **another exception occurred**" | Usually accidental |
| `raise New() from None` | Nothing about the original | Deliberately hidden |

**Always use `from exc` when translating an exception.** Without it the reader
sees two tracebacks with no stated relationship, and the message implies the
second one was a bug in your handler.

`from None` is right in exactly one situation: when the original is noise the
caller cannot act on, and exposing it would leak an implementation detail. Use
it sparingly and deliberately — it destroys information.

---

## 4. Designing your own exceptions

```python
class AppError(Exception):
    """Base for everything this application raises deliberately."""

class ValidationError(AppError):
    def __init__(self, field: str, value: object, reason: str) -> None:
        super().__init__(f"{field}={value!r}: {reason}")
        self.field = field
        self.value = value
        self.reason = reason
```

**Four rules.**

**1. One base class per package.** A caller can then write
`except AppError:` and catch everything you raise deliberately, while still
seeing bugs (a `TypeError` from your own code) propagate.

**2. Carry data, not just a string.** An exception with only a message forces
every handler to parse English to react. Carrying `field`, `value` and `reason`
lets a caller decide, and lets a web layer render JSON.

**3. The message must identify the input.** Compare:

```
ValueError: invalid input
ValueError: line 4210: expected 3 fields, got 2: 'grace,45'
```

The second one costs eight extra characters to write and saves an hour. **Use
`!r`** — it shows quotes and whitespace, which is exactly what matters when the
bug is a trailing space or an empty string.

**4. Do not inherit from `BaseException`.** Ever.

---

## 5. EAFP and LBYL

```python
# LBYL -- Look Before You Leap
if os.path.exists(path):
    with open(path) as f: ...      # the file may be deleted in between

# EAFP -- Easier to Ask Forgiveness than Permission
try:
    with open(path) as f: ...
except FileNotFoundError:
    ...
```

EAFP is preferred in Python for two concrete reasons, not stylistic ones:

- **The check-then-act race is real.** Between `exists()` and `open()`, another
  process can delete the file. Every LBYL check on external state has this bug,
  and it is called TOCTOU (time of check to time of use). It is a security
  vulnerability class, not just a flake.
- **One lookup instead of two.** `if k in d: return d[k]` hashes twice.

LBYL is better when the check is cheap and local (`if not items: return`), when
failure is expected and frequent (exceptions are relatively expensive), or when
you must validate several things and report them all at once (Module 06).

---

## 6. `ExceptionGroup` and `except*` (3.11+)

When several things fail concurrently, one exception cannot represent them.

```python
raise ExceptionGroup("upload failed", [
    ConnectionError("shard 1"),
    TimeoutError("shard 2"),
])

try:
    upload_all()
except* ConnectionError as eg:      # handles ALL ConnectionErrors in the group
    retry(eg.exceptions)
except* TimeoutError as eg:         # and this ALSO runs, for its subgroup
    log(eg.exceptions)
```

`except*` clauses are **not** exclusive — each one handles its matching subgroup
and several can run for one group. This is the machinery behind
`asyncio.TaskGroup` (Module 22), which is the main place you will meet it.

---

## 7. Logging

```python
import logging
logger = logging.getLogger(__name__)      # __name__, so the hierarchy matches
                                          # your package structure

logger.debug("cache miss for %s", key)    # %s LAZILY, not an f-string
logger.info("processed %d records", n)
logger.warning("retrying after %s", exc)
logger.error("failed to process %s", record_id)
logger.exception("unexpected failure")    # inside `except`: adds the traceback
logger.critical("shutting down")
```

**Five rules that matter in production:**

1. **`logger = logging.getLogger(__name__)` at module level.** Never
   `logging.info(...)`, which uses the root logger and cannot be configured
   per module.
2. **`%s` placeholders, not f-strings.** The formatting is deferred until the
   record is actually emitted, so a `debug` call costs nothing when debug
   logging is off. With an f-string you pay the formatting cost always.
3. **`logger.exception(...)` inside an `except` block** — it is `error()` plus
   the traceback, and it is what you want almost every time.
4. **Libraries must not configure logging.** Add a `NullHandler` and let the
   application decide. A library that calls `basicConfig` hijacks the whole
   process's logging.
5. **Never log secrets.** Tokens, passwords, connection strings, full request
   bodies. Logs go to aggregators with different access policies than your
   database (Module 08).

Structured logging (`structlog`, or `json.dumps` in a formatter) is worth it as
soon as you have more than one machine, because grep does not scale and fields
are queryable.

---

## 8. Retries, timeouts, and backoff

```python
def with_retry(fn, attempts=3, base_delay=0.1, max_delay=10.0):
    for attempt in range(attempts):
        try:
            return fn()
        except (ConnectionError, TimeoutError) as exc:
            if attempt == attempts - 1:
                raise
            delay = min(base_delay * 2**attempt, max_delay)
            delay *= 0.5 + random.random()          # JITTER -- see below
            time.sleep(delay)
```

**Four rules.**

**Only retry transient failures.** A `ValidationError` will fail identically
every time; retrying it wastes time and hides the real problem. Retry
`ConnectionError`, `TimeoutError`, and HTTP 429/502/503/504. Never retry 400,
401, 403, 404, or 422.

**Only retry idempotent operations.** If `charge_card()` times out you do not
know whether the charge happened. Retrying may charge twice. The fix is an
**idempotency key**: the caller generates a unique ID, the server records it,
and a repeat with the same key returns the original result. Module 33.

**Exponential backoff with jitter.** Without jitter, a thousand clients that
failed together retry together, forever — the thundering herd. Randomising the
delay spreads them out. This is not a refinement; it is the difference between
recovery and a self-sustaining outage.

**Always set a timeout.** Every network call, every lock acquisition, every
queue `get`. A call with no timeout is a hang waiting for a bad day, and the
default for most libraries is *no timeout*.

```python
httpx.get(url, timeout=5.0)       # not httpx.get(url)
lock.acquire(timeout=1.0)
queue.get(timeout=30)
```

---

## 9. What never to do

```python
try:
    do_something()
except Exception:
    pass                    # the single worst four lines in any codebase
```

This discards the error, the traceback, and any chance of diagnosing it. When
the program later behaves strangely, there is no evidence at all. If you must
continue past a failure, **log it**:

```python
except Exception:
    logger.exception("continuing past a failure in do_something")
```

And in a loop, count them and stop if there are too many — 40,000 failures is a
configuration problem, not a data problem (Module 13).

Other things not to do: `assert` for validation (it vanishes under `-O`,
Module 01); raising a bare `Exception` (uncatchable except by
`except Exception`, which catches everything else too); using exceptions for
ordinary control flow across module boundaries; and catching an exception only
to re-raise it unchanged.

---

## Common mistakes in this module

| Mistake | Symptom | Fix |
|---|---|---|
| `except:` or `except BaseException:` | Ctrl-C does not work | `except Exception:` at most |
| `except Exception: pass` | Silent failure, no evidence | Log it, or do not catch it |
| Too much inside `try` | Unrelated errors caught by mistake | One risky line; use `else` |
| Missing `from exc` | The cause is lost | `raise New(...) from exc` |
| Message without the input | Cannot reproduce the failure | Include the value with `!r` |
| `return` in `finally` | Swallows exceptions silently | Never |
| Retrying non-idempotent calls | Duplicate charges, duplicate emails | Idempotency keys |
| Retrying a 400 | Wasted time, same failure | Retry only transient errors |
| Backoff without jitter | Thundering herd, self-sustaining outage | Randomise the delay |
| No timeout | Hangs forever | Timeout on every external call |
| f-strings in log calls | Formatting cost paid even when disabled | `%s` placeholders |
| `assert` for validation | Vanishes under `-O` | `if not x: raise` |

---

## Self-check quiz

1. Why is `KeyboardInterrupt` not under `Exception`?
2. What does `else` do in a `try` statement, and what bug does it prevent?
3. Name three things that make `finally` run.
4. What are the three chaining forms and what does each traceback say?
5. Give four rules for designing an exception class.
6. What is TOCTOU, and which of EAFP/LBYL avoids it?
7. Why are `except*` clauses not mutually exclusive?
8. Why `%s` rather than an f-string in a log call?
9. Give three conditions that must hold before retrying an operation.
10. Why does backoff need jitter?

---

## Exercises

1. **[`ex01_hierarchy.py`](exercises/ex01_hierarchy.py)** — Twelve predictions
   about what is caught, in what order, and what `finally` does.
2. **[`ex02_design.py`](exercises/ex02_design.py)** — Design an exception
   hierarchy for a payments library, with data-carrying errors and a mapping to
   HTTP status codes.
3. **[`ex03_retry.py`](exercises/ex03_retry.py)** — Build a production-grade
   retry with backoff, jitter, a budget, a circuit breaker and idempotency.
4. **[`ex04_robust.py`](exercises/ex04_robust.py)** — Take a fragile script and
   make it survive every failure mode in a provided list.

---

## Going deeper

- [Built-in exceptions](https://docs.python.org/3/library/exceptions.html) — read the hierarchy once, properly
- [`logging` HOWTO](https://docs.python.org/3/howto/logging.html) and the Cookbook
- [PEP 654 — Exception Groups](https://peps.python.org/pep-0654/)
- AWS Architecture Blog, "Exponential Backoff and Jitter" — the definitive treatment, with simulations

---

**Next:** [Module 17 — Typing and Static Analysis](../17-typing-and-static-analysis/README.md)
