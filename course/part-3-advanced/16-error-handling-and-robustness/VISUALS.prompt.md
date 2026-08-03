# NotebookLM Visual Prompts — Module 16: Error Handling and Robustness

---

## Sources to add

| Source | Type |
|---|---|
| `16-error-handling-and-robustness/README.md` | Upload |
| `01-runtime-and-toolchain/README.md` (traceback reading) | Upload |
| https://docs.python.org/3/library/exceptions.html | Website |
| https://docs.python.org/3/howto/logging.html | Website |
| https://peps.python.org/pep-0654/ | Website |

---

## 1. Cinematic Video Overview

**Format:** Explanation
**Visual style:** Custom, with this description:

```
Clean technical schematic on a dark background. The exception hierarchy drawn
as a tree. An exception propagating drawn as a token rising up a stack of
frames, with each frame's except clauses shown as filters it either passes
through or is caught by. Retry timing drawn as a timeline with clients as dots.
Monospace type for all code and tracebacks. No characters, no mascots.
```

**Steering prompt (paste this whole block):**

```
Audience: a programmer who writes try/except and has been bitten by a silent
failure they could not diagnose. They have written `except Exception: pass` at
least once.

Thesis: error handling is a design activity, not a syntax one. Every rule here
comes from a specific failure that costs a specific amount of time.

1. THE HIERARCHY, AND WHY THE TOP THREE ARE SEPARATE. Draw the tree with
   BaseException at the root and KeyboardInterrupt, SystemExit and
   GeneratorExit as siblings of Exception rather than children. Then animate
   Ctrl-C during a retry loop: with `except Exception`, the interrupt passes
   through and the program stops. With a bare `except:`, the interrupt is
   CAUGHT, the loop continues, and the user presses Ctrl-C repeatedly with no
   effect. Show that -- it is the most visceral argument against a bare except
   and everyone has experienced it from the user side.

2. PROPAGATION. Show an exception raised deep in a call stack rising frame by
   frame, each frame's except clauses acting as a filter. Show a narrow filter
   letting it pass and a broad one catching it. Then show the specific bug: a
   try block containing TWO lines, where the second line's KeyError is caught
   by a handler intended for the first line's, and the program takes the
   "key not found" branch for a completely different reason. Then show the same
   code with `else`, and the second KeyError propagating correctly.

3. FINALLY. Show finally running on four different exits from the block:
   normal completion, an exception, a return, and a break. Then show the trap:
   a `return` inside finally, with an in-flight exception being visibly
   DISCARDED.

4. CHAINING. Show two tracebacks joined by each of the three connective
   sentences, and what each tells a reader:
     "direct cause"        -> deliberate translation, from exc
     "during handling"     -> usually an accident
     (nothing)             -> from None, information deliberately destroyed
   Then a realistic scenario: a JSONDecodeError translated to a ConfigError.
   With `from exc`, the reader sees the file, the line and the column. Without
   it, they see a ConfigError and a second traceback that looks like a bug in
   the error handler.

5. THE MESSAGE. Two error messages side by side for the same failure:
   "ValueError: invalid input" and
   "ValueError: line 4210: expected 3 fields, got 2: 'grace,45'".
   Then show a developer's actual workflow with each: with the first, they add
   logging, redeploy, wait for it to recur. With the second, they open the file
   at line 4210. Put a time cost on screen for both.

6. TOCTOU. Animate the check-then-act race: process A calls exists() and gets
   True, process B deletes the file, process A calls open() and crashes. Then
   show EAFP, where the open either succeeds or fails atomically with no window.
   State that this is a security vulnerability class, not merely a flake.

7. RETRY, BACKOFF AND JITTER. This is the section to make visual, because the
   argument is entirely about timing. Draw a timeline with a thousand client
   dots. A backend fails; all thousand retry after exactly 1 second, in one
   spike, and knock the recovering backend down again. Loop it two or three
   times so the viewer sees the outage sustaining itself. Then add jitter and
   show the same thousand dots spread across the interval, load staying under
   the line, and the backend recovering.
   Then the idempotency point: a charge request that times out, drawn with the
   request having ARRIVED and the response having been lost. Show the retry
   charging a second time. Then show an idempotency key making the second
   request return the first result instead.

8. WHAT NEVER TO DO. Close on `except Exception: pass`, and show the downstream
   consequence rather than the code: a program in an inconsistent state, an
   engineer three days later with no log line, no traceback, and no way to know
   the failure ever happened.

Do not cover: asyncio error handling or typing. Those are Modules 22 and 17.
```

---

## 2. Mind Map

**Prompt:**

```
Build a mind map titled "Failing Well".

Branch 1 "The hierarchy": BaseException vs Exception, the three siblings and
why they are separate, the main Exception subtrees, and what to catch.

Branch 2 "try/except/else/finally": what each clause is for, the minimal-try
rule, everything that triggers finally, and the return-in-finally trap.

Branch 3 "Chaining": from exc, implicit chaining, from None, and what each
traceback tells a reader.

Branch 4 "Designing exceptions": one base per package, carry data not strings,
messages that identify the input, !r, and never subclass BaseException.

Branch 5 "EAFP vs LBYL": the TOCTOU race, double lookups, and the three cases
where LBYL is better.

Branch 6 "ExceptionGroup": concurrent failures, except* being non-exclusive,
and the connection to TaskGroup.

Branch 7 "Logging": getLogger(__name__), lazy % formatting, logger.exception,
NullHandler in libraries, never logging secrets, and when to go structured.

Branch 8 "Retries": transient only, idempotent only, exponential backoff,
jitter and the thundering herd, budgets, circuit breakers, and timeouts on
everything.

Branch 9 "Never": bare except, except-pass, assert for validation, bare
Exception, return in finally, catching to re-raise unchanged.
```

---

## 3. Study Guide, Quiz, and Flashcards

**Study Guide prompt:**

```
Produce a study guide for someone on call for a Python service tonight.

Include a "what to catch" decision table: given a situation (a file may not
exist, a network call may time out, user input may be malformed, a key may be
missing, a third-party library may raise anything, a background worker must not
die), which exception types to catch and what to do in the handler.

Include a retry decision table: for each of about twelve failure kinds (HTTP
400, 401, 403, 404, 409, 422, 429, 500, 502, 503, 504, connection reset, DNS
failure, timeout), whether to retry, how many times, and why.

Include a logging reference: which level for which situation, what must never
appear in a log, and the difference between logger.error and logger.exception.

Include a message-quality rubric: for five bad error messages, the rewritten
version and what a debugger can now do that they could not before.

End with five production incidents described by symptom, each with the
error-handling mistake that caused it.
```

**Quiz prompt:**

```
Generate 16 questions.

At least six predict-the-output on control flow: finally with return, finally
with an exception in flight, else running or not, a nested try where the inner
finally raises, an exception raised inside an except block, and a bare except
catching KeyboardInterrupt.

At least four on retry decisions: given a failure and an operation, should it
be retried, and what could go wrong if it is.

Include: a try block containing two lines where the second's exception is
caught by mistake, a chained exception where the reader must say which is the
root cause, and an f-string in a debug log call at a level that is disabled.

For each answer, name the specific production consequence, not just the rule.
```

**Flashcards prompt:**

```
20 flashcards. Front: a term or fragment. Back: what it means and the failure
it prevents.

Include: BaseException vs Exception, bare except, except Exception: pass, else
clause, finally, return in finally, raise from, implicit chaining, from None,
EAFP, LBYL, TOCTOU, ExceptionGroup, except*, logger.exception,
getLogger(__name__), lazy % formatting, NullHandler, exponential backoff,
jitter, idempotency key, thundering herd.
```

---

## The specific visuals to insist on

1. **Ctrl-C caught by a bare `except`** inside a retry loop, with the user
   pressing it repeatedly and nothing happening.
2. **The two-line `try` block** catching the wrong `KeyError`, next to the
   `else` version.
3. **`finally` running on four different exits**, and a `return` in `finally`
   discarding an in-flight exception.
4. **Three joined tracebacks** with the three connective sentences and what each
   implies.
5. **Two error messages and two debugging workflows**, with time costs.
6. **The TOCTOU race animated** across two processes.
7. **A thousand retry dots spiking in unison**, sustaining an outage, then
   spread by jitter and recovering. This is the single most persuasive image in
   the module.
8. **The timed-out charge**: request arrived, response lost, retry charging
   twice, then an idempotency key preventing it.

---

## Analogies that work

- **A net with a specific mesh size.** A narrow `except` catches only what you
  meant to catch; a bare `except` is a net that also catches the fire alarm.
- **A stampede at a doorway** for the thundering herd: everyone waiting exactly
  one second and surging together, versus everyone waiting a random interval and
  filing through.
- **A signed-for delivery** for idempotency keys: the courier records the
  tracking number, so presenting the same number twice does not deliver a second
  parcel.

## Analogies to refuse

- **"Exceptions are like return values for errors."** They propagate
  automatically through frames that know nothing about them; that is the whole
  point, and the return-value framing hides it.
- **"Catch everything so the program does not crash."** Crashing loudly is
  usually better than continuing in an unknown state. This instinct is what
  produces `except Exception: pass`.
- **Describing retries as "making it more reliable" without qualification.**
  Retrying a non-idempotent operation makes it *less* reliable, and retrying
  without jitter can turn a blip into an outage.

---

## Accuracy guardrails

```
Accuracy requirements:
- KeyboardInterrupt, SystemExit and GeneratorExit inherit from BaseException,
  NOT Exception. That is deliberate, and it is why `except Exception` is the
  broadest thing you should ever write.
- finally runs on normal completion, on an exception, on return, and on
  break/continue. A return inside finally REPLACES any in-flight exception or
  return value.
- `raise X from Y` sets __cause__ and prints "direct cause". Raising inside an
  except block without `from` sets __context__ and prints "during handling".
  `from None` suppresses the display entirely. Name all three precisely.
- except* clauses are NOT mutually exclusive; several may run for one
  ExceptionGroup. ExceptionGroup and except* require 3.11+.
- assert statements are removed by python -O. Never use them for validation or
  security checks.
- logging with %s defers formatting until the record is emitted; an f-string is
  formatted immediately regardless of level.
- Retrying is only safe for IDEMPOTENT operations. State this every time retries
  are mentioned.
- Backoff without jitter causes synchronised retry storms. This is not a minor
  refinement.
- Most network libraries default to NO timeout. Do not imply there is a
  sensible default.
- Do not present EAFP as universally correct. Give the cases where LBYL wins.
```

---

## After watching, you should be able to

- [ ] Say why `KeyboardInterrupt` is not under `Exception`, with the
      consequence.
- [ ] Explain what `else` prevents, with the two-line example.
- [ ] Name three things that trigger `finally`, and what `return` in it does.
- [ ] Choose between the three chaining forms and justify the choice.
- [ ] Rewrite a vague error message so that it identifies the input.
- [ ] Describe the TOCTOU race and which style avoids it.
- [ ] Explain why backoff needs jitter, in terms of a thousand clients.
- [ ] State the three conditions that must hold before retrying anything.
