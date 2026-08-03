# Solutions — Module 16

## Exercise 16.1 — Twelve predictions

| # | Result | Mechanism |
|---|---|---|
| q01 | `finally ran`, then returns `"try"` | `finally` runs before the return completes |
| q02 | Returns `"finally wins"`; **the ValueError vanishes** | A `return` in `finally` replaces the in-flight exception |
| q03 | present: `else` then `finally`; absent: `caught` then `finally` | `else` runs only when nothing was raised |
| q04 | Catches a `KeyError` from *inside* `process` | Two lines in one `try` |
| q05 | `__context__` set, `__cause__` `None` | Implicit chaining |
| q06 | Both set | `from exc` sets `__cause__` as well |
| q07 | `__cause__` `None`, `__suppress_context__` `True` | `from None` hides the original from display |
| q08 | `NameError` — `exc` was deleted | See below |
| q09 | Only `ValueError` caught by `except Exception` | The other three are `BaseException` siblings |
| q10 | inner, middle, then caught | `finally` runs innermost-first as the exception unwinds |
| q11 | `RuntimeError` surfaces; the original is at `__context__` | The `finally`'s exception replaces the in-flight one |
| q12 | Three attempts; `finally` on every iteration | `continue` triggers `finally` too |

**q02 and q11 are the two that lose information.** In q02 the `ValueError`
disappears completely — no traceback, no log, nothing. In q11 the original is at
least preserved on `__context__`, but the exception a caller *sees* is the
cleanup failure, not the failure that caused the cleanup. That is backwards:
"disk full while rolling back" is far less useful than "the transaction failed
because of X". Wrap risky cleanup in its own `try` and log rather than raise.

**q04 is the argument for `else`.** The handler was written for `data["k"]` and
catches a `KeyError` raised deep inside `process`. The program then takes the
"key was missing" branch for a completely unrelated reason, and no test will
find it because the test's `process` does not raise.

**q08 — why Python deletes the exception variable.** The exception holds a
traceback, which references every frame in the stack, which references every
local in each of them. Keeping `exc` bound after the block would keep that entire
graph alive — including large objects the frames happened to hold. Python deletes
the name at the end of the `except` block specifically to break that. If you need
the exception afterwards, bind it to another name first.

**q09 is the whole argument against a bare `except`.** `KeyboardInterrupt`
passing through is what makes Ctrl-C work.

---

## Exercise 16.2 — A payments exception hierarchy

```
PaymentError                      one base -> callers write one except clause
├── PaymentDeclined               .code, .issuer_message  -> 402
├── InsufficientFunds             .available, .required   -> 402
├── CardExpired                   .expiry                 -> 402
├── InvalidRequest                .field, .value, .reason -> 400   NOT retryable
├── AuthenticationError                                   -> 401
├── RateLimited                   .retry_after            -> 429   retryable
└── GatewayError                  .status, .attempt       -> 502   retryable
```

Three design points:

**`retryable` belongs on the exception, not in a lookup table.** A caller should
be able to write `if exc.retryable: schedule_retry(exc.retry_after)` without
knowing every subclass. Adding a new error type then cannot forget to declare its
retry semantics — the same reasoning as `exit_code` in Module 07.

**Never expose the issuer's raw decline reason to the customer.** "Insufficient
funds" told to the wrong person is a privacy problem, and card networks
deliberately return vague codes. Carry the detail for your logs; render something
generic for the user. Two attributes: `message` and `user_message`.

**`InvalidRequest` must not be retryable, and this is the one people get wrong.**
It looks like a transient gateway problem when it arrives as an HTTP 400 from the
provider, and retrying it burns your rate limit while failing identically every
time.

---

## Exercise 16.3 — Production-grade retry

The five things that separate a real retry from a `for` loop:

**Jitter.** Full jitter (`random.uniform(0, delay)`) beats "equal jitter"
(`delay/2 + random.uniform(0, delay/2)`) in AWS's published simulations, on both
completion time and server load. Without any jitter, a thousand clients that
failed together retry together forever.

**A budget, not just a count.** Three attempts with exponential backoff can take
half an hour if the base delay is large. The caller cares about *total elapsed
time*, so the loop must check a deadline as well as an attempt count. This is
also what makes retries composable — an outer timeout can bound an inner retry.

**A circuit breaker.** After N consecutive failures, stop trying for a cooldown
period and fail fast. Without one, a dead dependency means every request waits
the full retry budget before failing, so your latency becomes the retry budget
and your thread pool fills with requests waiting on a corpse. Three states:
closed, open, half-open — where half-open lets exactly one probe through.

**Idempotency keys.** Generated by the *caller*, once per logical operation, and
reused across every retry of that operation. Generating a new key per attempt
defeats the entire mechanism, and that is the most common way it is implemented
wrongly.

**Retry only what is transient.** A `ValidationError` fails identically every
time. The classification table (retry 429/502/503/504 and connection errors;
never 400/401/403/404/422) belongs in one place, next to the exception
definitions.

---

## Exercise 16.4 — Making a fragile script robust

The order matters, and it is roughly this:

1. **Timeouts on every external call.** Nothing else helps while a call can hang
   forever. Most libraries default to none.
2. **Narrow the exception handlers.** Replace `except Exception` with the
   specific types, and see what starts propagating — that is the list of things
   you were silently swallowing.
3. **Make the messages identify the input.** Every raise gets the record id, the
   line number, or the value, with `!r`.
4. **Chain with `from exc`** wherever you translate.
5. **Isolate per item.** One bad record must not lose the other 99,999
   (Module 13), with a failure budget so that 40,000 bad records stops the run.
6. **Make writes atomic** (Module 07), so a crash mid-write cannot corrupt.
7. **Make the whole thing idempotent**, so rerunning after a partial failure is
   safe. This is the one that turns a 3am incident into a retry.

The last point is worth stating separately: **the most valuable robustness
property of a batch job is that running it twice is harmless.** Every other
mitigation reduces the chance of failure; idempotency makes recovery from a
failure trivial.
