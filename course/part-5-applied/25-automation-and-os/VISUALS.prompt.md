# NotebookLM Visual Prompts — Module 25: Automation and the OS

---

## Sources to add

| Source | Type |
|---|---|
| `25-automation-and-os/README.md` | Upload |
| `07-project-inventory-cli/README.md` | Upload |
| https://clig.dev/ | Website |
| https://docs.python.org/3/library/signal.html | Website |
| https://docs.python.org/3/library/subprocess.html | Website |

---

## 1. Cinematic Video Overview

**Format:** Explanation
**Visual style:** Retro Print, or Custom:

```
Clean technical schematic on a dark background. A running script drawn as a
process box with a timeline beneath it. Failures drawn as an interruption at a
specific point on that timeline, with the resulting state shown before and
after. Terminal output in monospace. No characters, no mascots.
```

**Steering prompt (paste this whole block):**

```
Audience: a programmer who writes scripts that work when they run them by hand,
and who is about to have one of those scripts scheduled in cron by a colleague.

Thesis: a script becomes infrastructure the moment someone else depends on it,
and the properties that matter then -- idempotency, resumability, dry-run,
observability, clean interruption -- are all design decisions made before the
first failure, not after.

1. THE 3AM FAILURE. Open with a backup script's timeline: it copies 4,000 of
   10,000 files and the machine dies. Show three possible next mornings:
     - not idempotent: rerunning duplicates the 4,000 already copied
     - not resumable: rerunning starts from zero, taking six hours
     - both: rerunning finishes the remaining 6,000 in twenty minutes
   Put the operator's recovery time on screen for each. This frames every
   property that follows as a cost avoided rather than a virtue.

2. THE FIVE PROPERTIES. Present each as a scenario rather than a definition:
   idempotency as the rerun above; resumability as a checkpoint file; dry-run
   as the operator seeing what would happen before it does; observability as
   the log line that tells you it reached item 4,000; interruptibility as
   Ctrl-C stopping between items rather than during one.

3. SIGNALS. Draw the process receiving SIGTERM. Show the WRONG handler doing
   real work -- writing a file -- being interrupted at an arbitrary bytecode
   mid-write, with a corrupted result. Then the right handler setting a single
   boolean, and the main loop noticing it after the current item and stopping
   cleanly. Then show SIGKILL arriving with NO handler possible at all, and
   state the conclusion: your data must survive an abrupt death regardless,
   which is what atomic writes are for.
   Then the Docker/systemd sequence: SIGTERM, a ten-second grace period, then
   SIGKILL -- with a shutdown that takes fifteen seconds being killed mid-work
   every single time.

4. THE PIPE DEADLOCK. Animate Popen with stdout and stderr both piped. The
   parent reads stdout. The child writes to stderr until the 64 KB kernel
   buffer fills, then BLOCKS. The parent waits for more stdout that will never
   come. Draw both processes frozen, pointing at each other. Then show
   communicate() reading both, and the redirect-stderr-into-stdout alternative.

5. WHY CRON JOBS FAIL. Show the same script run two ways side by side: in an
   interactive shell with a full environment, PATH, virtualenv and working
   directory; and under cron with a nearly empty environment, no PATH beyond a
   minimum, no virtualenv, and $HOME as the working directory. Animate each of
   the four failures in turn -- python not found, an import failing, a relative
   path resolving elsewhere, output vanishing into unread mail. Then show
   `env -i` reproducing it locally in one command.

6. LOCKING. Show two scheduled runs overlapping because the first took longer
   than the interval, both writing the same file, and the result being
   interleaved garbage. Then flock: the second instance failing to acquire and
   exiting cleanly. Then the crucial detail -- the lock being released
   automatically when a process is SIGKILLed, which a PID file cannot do.

7. CLI QUALITY. Close on the composability rules from clig.dev, shown as
   pipelines: data on stdout flowing into the next command while messages go to
   the terminal, a --json flag feeding jq, an exit code branching a CI script,
   and a --dry-run showing an operator what a destructive command would do.

Do not cover: web frameworks or async. Modules 28 and 22.
```

---

## 2. Mind Map

**Prompt:**

```
Build a mind map titled "Scripts That Can Be Trusted".

Branch 1 "The five properties": idempotent, resumable, dry-runnable,
observable, interruptible -- each with the failure it prevents.

Branch 2 "Structure": main(argv), exit codes, logging setup, the exception
boundary, and the __main__ guard.

Branch 3 "Signals": SIGINT, SIGTERM, SIGHUP, SIGKILL; set a flag never do work;
grace periods in Docker and systemd; and why atomic writes are still required.

Branch 4 "Files": atomic write, exclusive create, flock and why it beats a PID
file, and path resolution for untrusted input.

Branch 5 "subprocess": list form, check, timeout, streaming output, the
two-pipe deadlock, and communicate().

Branch 6 "Config": precedence order, injecting env, and printing the resolved
configuration.

Branch 7 "CLI design": stdout vs stderr, --json, exit codes, --dry-run,
confirmation, progress, NO_COLOR and TTY detection.

Branch 8 "Scheduling": cron, systemd timers, APScheduler, Celery beat, Airflow
-- with the four cron failure modes and how to reproduce them.

Branch 9 "Watching files": polling vs watchfiles, debouncing multiple events per
save, and the partially-written-file trap.
```

---

## 3. Study Guide, Quiz, and Flashcards

**Study Guide prompt:**

```
Produce a study guide for someone whose script is about to be scheduled in
production.

Include a pre-deployment checklist: idempotency, resumability, dry-run,
logging, exit codes, timeouts, locking, atomic writes, absolute paths,
environment independence, and signal handling. For each: how to verify it, and
the failure if it is missing.

Include a cron troubleshooting table: for each of eight symptoms (nothing runs,
runs but fails immediately, import error, file not found, works by hand not in
cron, runs twice, output missing, wrong timezone), the cause and the fix.

Include a subprocess reference: run vs Popen, when to stream, the pipe
deadlock, timeouts, and reading exit codes.

Include a signal-handling guide: which signals matter, what a handler may
safely do, grace periods, and what to do about SIGKILL.

End with five scripts described by what they do, each with the specific
idempotency strategy it needs.
```

**Quiz prompt:**

```
Generate 14 questions.

At least four should present a script and a failure point on its timeline and
ask what state the system is left in, and what rerunning would do.

Include: a signal handler that writes a file, a Popen with two pipes reading
one, a crontab entry using a bare `python`, a script using a relative path, two
overlapping scheduled runs with no lock, a shutdown that takes longer than the
grace period, and a file-watcher acting on a creation event.

For each answer, state the operator's recovery cost in time, not just the
technical fault.
```

**Flashcards prompt:**

```
20 flashcards. Front: a term or scenario. Back: the rule and the failure it
prevents.

Include: idempotent, resumable, dry-run, SIGTERM, SIGINT, SIGKILL, signal
handler safety, grace period, flock, PID file, atomic write, exclusive create,
subprocess check=True, timeout, pipe deadlock, communicate, cron PATH, cron
working directory, env -i, systemd timer, Persistent=true, NO_COLOR, debounce.
```

---

## The specific visuals to insist on

1. **Three next-mornings** after a 40-percent-complete failure, with recovery
   times.
2. **A signal handler interrupted mid-write** versus one setting a flag.
3. **The SIGTERM → 10s → SIGKILL sequence** with a 15-second shutdown being
   killed every time.
4. **The pipe deadlock**: both processes frozen, each waiting on the other.
5. **The same script under a shell and under cron**, environments side by side,
   with the four failures.
6. **Two overlapping runs interleaving writes**, then `flock` preventing it.
7. **A pipeline with data on stdout and messages on stderr**, both visible.

---

## Analogies that work

- **A checkpoint in a long journey.** Resumability is knowing which town you
  reached; idempotency is being able to walk the same stretch twice without
  harm.
- **A polite tap on the shoulder versus unplugging the machine** for SIGTERM
  versus SIGKILL. You can respond to the first; the second is why your work must
  already be saved.
- **A single key for a shared room** for `flock` — and the key falls out of the
  lock automatically if the holder collapses, which a signed-out clipboard (a
  PID file) does not.

## Analogies to refuse

- **"Just add a try/except."** Robustness here is a set of design properties,
  not a handler. A `try` around a non-idempotent operation does not make rerunning
  safe.
- **"Cron is unreliable."** Cron is extremely reliable; the *environment* is
  different from your shell, and that difference is the bug.
- **Describing a dry-run as a "preview".** It must run identical logic, with
  side effects disabled — otherwise the preview can diverge from reality, which
  is worse than having none.

---

## Accuracy guardrails

```
Accuracy requirements:
- A signal handler runs between bytecodes in the main thread. It must only set
  a flag or write to a self-pipe. Doing real work there is a race.
- SIGKILL cannot be caught, blocked or handled. Therefore durability must come
  from atomic writes, not from cleanup handlers.
- Docker sends SIGTERM then SIGKILL after a grace period (10 seconds by
  default); Kubernetes uses terminationGracePeriodSeconds (30 by default).
- flock is advisory and local-filesystem only. It is unreliable over NFS.
- Popen with both stdout and stderr as pipes deadlocks if only one is read and
  the other fills its buffer (typically 64 KB). communicate() reads both.
- subprocess.run without check=True does NOT raise on a non-zero exit.
- cron provides a minimal environment and $HOME as the working directory. It
  does not source shell profiles.
- systemd timers with Persistent=true run a missed job after a reboot; cron
  does not.
- A filesystem "created" event fires when the file is created, not when writing
  finishes.
- Do not present exit code conventions as universal beyond 0 = success. State
  the common ones (1 general, 2 usage, 130 SIGINT) as conventions.
```

---

## After watching, you should be able to

- [ ] Name the five properties and the failure each prevents.
- [ ] Say what a signal handler may safely do, and why.
- [ ] Explain why atomic writes are required even with a SIGTERM handler.
- [ ] Describe the `Popen` deadlock and two ways to avoid it.
- [ ] Give the four reasons cron jobs fail, and the command that reproduces
      them.
- [ ] Say why `flock` beats a PID file.
- [ ] Explain what a dry-run must do to be trustworthy.
