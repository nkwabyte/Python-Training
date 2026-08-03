"""Exercise 25.2 — Graceful shutdown, and why handlers must be trivial.

Run:  python ex02_signals.py           then press Ctrl-C partway through
      python ex02_signals.py --unsafe  and press Ctrl-C repeatedly
"""
from __future__ import annotations

import json
import signal
import sys
import time
from pathlib import Path

STATE = Path("/tmp/ex02_state.json")


# TODO 1 -----------------------------------------------------------------------
class GracefulExit:
    """Set a flag on SIGINT/SIGTERM. Nothing else.

    Requirements:
      - handle both signals
      - record WHICH signal arrived
      - a SECOND signal should exit immediately (a user pressing Ctrl-C twice
        means "I meant it") -- decide what "immediately" should do about
        in-flight work, and justify it
      - restore the previous handlers on exit, so this is usable as a context
        manager inside a larger program
    """


# TODO 2 -----------------------------------------------------------------------
def process_items(items: list[int], exit_flag) -> int:  # type: ignore[no-untyped-def]
    """Process items, checking the flag BETWEEN items, never during one.

    Each item must be committed atomically before moving on, so an interruption
    leaves a consistent state. Log progress every N items so an operator can
    see where it stopped.
    """
    raise NotImplementedError


# TODO 3 -----------------------------------------------------------------------
def save_checkpoint(index: int) -> None:
    """Atomically record how far we got (Module 07)."""
    raise NotImplementedError


def load_checkpoint() -> int:
    """Return the resume point, or 0."""
    raise NotImplementedError


# TODO 4: the UNSAFE demonstration ---------------------------------------------
def unsafe_handler(signum: int, frame: object) -> None:
    """DO NOT DO THIS. It is here so you can watch it fail.

    Does real work in the handler: writes a file, sleeps, prints.

    Run with --unsafe and press Ctrl-C several times in quick succession.
    Record what happens. You are looking for at least one of:
      - a handler re-entered while still running
      - a partially written file
      - a traceback from inside the handler
      - output interleaved mid-line

    Then answer: WHY is this unsafe? The handler runs in the main thread,
    between two bytecodes, at a point you did not choose. Name three specific
    things that could be half-finished at that moment.
    """
    print("  handler: starting work...")
    STATE.write_text(json.dumps({"handler": "ran", "at": time.time()}))
    time.sleep(0.5)
    print("  handler: done")


# TODO 5 -----------------------------------------------------------------------
def with_deadline(exit_flag, seconds: float) -> None:  # type: ignore[no-untyped-def]
    """Shutdown with a deadline.

    After the flag is set, finish the current item but give up entirely if
    cleanup exceeds `seconds` -- because a container's grace period is finite
    (Docker: 10s, Kubernetes: 30s by default) and exceeding it means SIGKILL
    mid-work anyway.

    Then answer: how would you find out your real grace period, and what should
    a service do if its clean shutdown genuinely needs longer than it?
    """
    raise NotImplementedError


def main(argv: list[str]) -> int:
    if "--unsafe" in argv:
        signal.signal(signal.SIGINT, unsafe_handler)
        print("UNSAFE mode. Press Ctrl-C repeatedly and watch.")
        for i in range(60):
            print(f"  working {i}", flush=True)
            time.sleep(0.2)
        return 0

    print("Press Ctrl-C to stop cleanly. Then run again to see it resume.")
    raise NotImplementedError("implement the TODOs")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
