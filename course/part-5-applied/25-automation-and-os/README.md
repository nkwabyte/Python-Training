# Module 25 — Automation, Scripting, and the OS

**Time budget:** 4 hours lesson, 7 hours exercises
**Prerequisite:** Modules 07 (CLI), 16, 19

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

The scripts you write for yourself become the scripts your team depends on,
usually without anyone deciding that. This module is about the difference
between a script that works when you run it and one that works at 3am, in cron,
on a machine you have never seen, when the disk is full.

---

## 1. The anatomy of a robust script

```python
#!/usr/bin/env python3
"""One-line description. Longer explanation, and an example invocation."""

from __future__ import annotations

import logging
import signal
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

EXIT_OK, EXIT_FAILURE, EXIT_USAGE, EXIT_INTERRUPTED = 0, 1, 2, 130


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    configure_logging(args.verbose)
    try:
        return run(args)
    except KeyboardInterrupt:
        logger.warning("interrupted")
        return EXIT_INTERRUPTED
    except AppError as exc:
        logger.error("%s", exc)
        return EXIT_FAILURE


if __name__ == "__main__":
    raise SystemExit(main())
```

Everything here has appeared before: `main(argv)` from Module 01, exit codes
from Module 07, exception handling from Module 16. What is new is treating them
as the *minimum* for anything another person or a scheduler will run.

**The five properties that make a script trustworthy:**

| Property | Why |
|---|---|
| **Idempotent** | Running it twice is harmless, so recovery is "run it again" |
| **Resumable** | It can continue after a partial failure |
| **Dry-runnable** | You can see what it would do before it does it |
| **Observable** | Its logs say what happened and how far it got |
| **Interruptible** | Ctrl-C stops it cleanly, without corrupting state |

**Idempotency is the most valuable of the five.** Every other property reduces
the chance of a bad outcome; idempotency makes recovery trivial.

---

## 2. Signals and clean shutdown

```python
import signal

class GracefulExit:
    def __init__(self) -> None:
        self.should_stop = False
        signal.signal(signal.SIGTERM, self._handle)
        signal.signal(signal.SIGINT, self._handle)

    def _handle(self, signum: int, frame: object) -> None:
        logger.info("received %s, finishing the current item", signal.Signals(signum).name)
        self.should_stop = True

exit_flag = GracefulExit()
for item in items:
    process(item)
    if exit_flag.should_stop:
        logger.info("stopping cleanly after %s", item.id)
        break
```

**Set a flag; do not do the work in the handler.** A signal handler interrupts
the main thread at an arbitrary bytecode, so anything non-trivial there is a
race. Setting a boolean is safe; writing a file is not.

| Signal | Meaning | Catchable |
|---|---|---|
| `SIGINT` | Ctrl-C | yes |
| `SIGTERM` | Polite "please stop" — what Docker and systemd send | yes |
| `SIGKILL` | `kill -9` | **no** |
| `SIGHUP` | Terminal closed; conventionally "reload config" | yes |

Because `SIGKILL` cannot be caught, **your data must survive an abrupt death**
regardless — which is what atomic writes (Module 07) are for. Docker sends
`SIGTERM`, waits ten seconds, then `SIGKILL`; if your shutdown takes longer than
that grace period, you are being killed mid-work.

---

## 3. Files, safely

```python
# atomic write -- Module 07
tmp = path.with_suffix(path.suffix + ".tmp")
tmp.write_text(data, encoding="utf-8")
tmp.replace(path)

# exclusive create -- fails rather than clobbering
with path.open("x", encoding="utf-8") as fh: ...

# a lock file, so two copies do not run at once
import fcntl
with open("/tmp/myjob.lock", "w") as lock:
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        logger.error("another instance is running")
        return EXIT_FAILURE
    run()
```

`flock` is released automatically when the process dies, including on `kill -9`,
which is why it beats a "is there a PID file" check. It is local-filesystem only
— on NFS it is unreliable, and distributed locking is a genuinely hard problem
(Module 37 territory).

**Never build paths from user input without resolving** (Module 19).

---

## 4. `subprocess`, in practice

```python
result = subprocess.run(
    ["rsync", "-a", str(src), str(dst)],
    capture_output=True, text=True, check=True, timeout=3600,
)
```

`check=True` and `timeout=` should be reflexive. Never `shell=True` with
anything interpolated (Module 19).

Streaming output from a long-running command, so you see progress rather than a
wall of text at the end:

```python
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                        text=True, bufsize=1)
assert proc.stdout is not None
for line in proc.stdout:
    logger.info("%s", line.rstrip())
if proc.wait() != 0:
    raise CommandFailed(cmd, proc.returncode)
```

**The deadlock to know about:** using `Popen` with both `stdout=PIPE` and
`stderr=PIPE` and reading only one of them will hang when the other pipe's
buffer fills (typically 64 KB). Use `communicate()`, or redirect stderr into
stdout as above.

---

## 5. Configuration and environment

Module 06's rules, applied to scripts: environment for what varies per
deployment, a file for structured defaults, flags for what varies per run.

```python
def get_config(argv, env=os.environ):        # both injected, both testable
    ...
```

**Precedence, highest first: command-line flag, environment variable, config
file, built-in default.** Print the resolved configuration under `--verbose`;
the gap between what someone wrote and what actually took effect is where
support time goes.

---

## 6. Building a real CLI

`argparse` is in the standard library and sufficient. **Typer** (built on Click)
is what you would choose for anything with more than a few subcommands.

```python
import typer
app = typer.Typer(help="Sync files between two locations.")

@app.command()
def sync(
    source: Path = typer.Argument(..., exists=True, help="Source directory"),
    dest: Path = typer.Argument(..., help="Destination"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would happen"),
    workers: int = typer.Option(4, min=1, max=32),
) -> None:
    """Sync SOURCE to DEST."""
```

Typer derives parsing, validation, help text and shell completion **from the
type hints** (Module 17). `exists=True` on a `Path` means a missing directory is
a usage error with a clear message, not a traceback three functions later.

The CLI design rules that matter, from [clig.dev](https://clig.dev/):

- Data to stdout, messages to stderr (Module 07)
- `--json` for machine consumption
- Exit codes that mean something
- `--dry-run` on anything destructive
- Confirm before irreversible actions, with `--yes` to skip
- Show progress for anything over a few seconds
- Respect `NO_COLOR` and detect whether stdout is a TTY

---

## 7. Scheduling

| Tool | Best for |
|---|---|
| `cron` | Simple recurring jobs on one machine |
| `systemd` timers | The same, with logging, dependencies and resource limits |
| APScheduler | In-process scheduling inside a long-running app |
| Celery beat / arq | Distributed scheduled tasks (Module 33) |
| Airflow / Dagster / Prefect | Data pipelines with dependencies and retries |

```cron
# m h dom mon dow  command
0 2 * * *  /opt/venv/bin/python /opt/jobs/nightly.py >> /var/log/nightly.log 2>&1
```

**The four things that break cron jobs, in order of frequency:**

1. **`PATH` is minimal.** Use absolute paths for the interpreter and every
   binary. `python` will not be found.
2. **The environment is not your shell's.** No `.bashrc`, no virtualenv, none of
   your exports. Set what you need explicitly in the crontab.
3. **The working directory is `$HOME`.** Relative paths resolve somewhere you
   did not expect.
4. **Output goes to mail nobody reads.** Redirect it to a file, or log properly.

Test with `env -i /usr/bin/env -` to reproduce cron's empty environment — that
one command finds most cron bugs before deployment.

`systemd` timers are better than cron for anything important: real logging via
journald, `OnFailure` hooks, dependency ordering, resource limits, and
`Persistent=true` so a missed run fires after a reboot.

---

## 8. Watching the filesystem

```python
from watchfiles import watch          # pip install watchfiles

for changes in watch("./src"):
    for change_type, path in changes:
        rebuild(path)
```

Polling with `os.stat` works and is fine for a handful of files. Beyond that,
use `watchfiles` (Rust-backed, cross-platform).

Two traps that catch everyone: editors write **several events per save**
(temp file, rename, chmod), so debounce; and a "file created" event fires when
the file is created, **not when it is finished being written**, so a naive
handler reads a half-written file.

---

## Common mistakes in this module

| Mistake | Symptom | Fix |
|---|---|---|
| Non-idempotent script | Rerunning after a partial failure duplicates work | Design for reruns |
| No `--dry-run` | Nobody dares run it | Add one |
| Real work in a signal handler | Rare corruption | Set a flag |
| Assuming `SIGTERM` grace | Killed mid-write | Atomic writes |
| Relative paths in cron | "Works when I run it" | Absolute paths |
| `python` in a crontab | `command not found` | Full interpreter path |
| `Popen` with two pipes, reading one | Hangs at 64 KB | `communicate()` |
| No `timeout=` | A hung subprocess hangs the job forever | Always set one |
| No locking | Two overlapping runs corrupt state | `flock` |
| Progress only at the end | Looks hung | Log as you go |
| Handling a file on creation | Reads a partial file | Wait for stability |

---

## Self-check quiz

1. Name the five properties of a trustworthy script, and which matters most.
2. Why must a signal handler only set a flag?
3. Which signal cannot be caught, and what does that imply for your data?
4. Why is `flock` better than a PID file?
5. What is the `Popen` deadlock and how do you avoid it?
6. Give the four things that break cron jobs.
7. How do you reproduce cron's environment locally?
8. What does Typer derive from type hints?
9. Give the config precedence order.
10. Why is a file-created event not a safe trigger to read the file?

---

## Exercises

1. **[`ex01_robust.py`](exercises/ex01_robust.py)** — Take a fragile backup
   script and add all five properties, one at a time, testing each.
2. **[`ex02_signals.py`](exercises/ex02_signals.py)** — Graceful shutdown with a
   deadline, plus a demonstration of why work in a handler is unsafe.
3. **[`ex03_cli.py`](exercises/ex03_cli.py)** — Build the same CLI twice, in
   `argparse` and Typer, and compare.
4. **[`ex04_cron.md`](exercises/ex04_cron.md)** — Deploy a job to cron and to a
   systemd timer. Break it four ways deliberately and fix each.

---

## Going deeper

- [Command Line Interface Guidelines](https://clig.dev/) — read it once, entirely
- [`signal`](https://docs.python.org/3/library/signal.html), [`subprocess`](https://docs.python.org/3/library/subprocess.html)
- [Typer](https://typer.tiangolo.com/) and [Rich](https://rich.readthedocs.io/) for progress bars and tables
- `man 5 crontab`, `man systemd.timer`

---

**Next:** [Module 26 — HTTP, APIs, and Scraping](../26-http-and-scraping/README.md)
