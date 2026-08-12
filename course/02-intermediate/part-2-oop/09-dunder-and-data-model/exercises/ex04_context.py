"""Exercise 09.4 — Four context managers, two ways each.

Write each as a class with __enter__/__exit__, then again with
@contextlib.contextmanager, and note which you would ship.

Run:  python ex04_context.py
"""

from __future__ import annotations

import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any


# TODO 1 -----------------------------------------------------------------------
class Timer:
    """Measures the wall time of a block.

    Requirements:
      - `with Timer() as t:` then t.elapsed afterwards
      - must record the time EVEN IF the block raises (that is the whole point
        of __exit__ over a plain function call)
      - must not swallow the exception
      - optional label, printed on exit only if one was given
      - use time.perf_counter, not time.time. Say why in a comment.
    """


@contextmanager
def timer(label: str = ""):  # type: ignore[no-untyped-def]
    """The same thing with @contextmanager. Note where the try/finally goes and
    why a bare try/except would be wrong."""
    raise NotImplementedError


# TODO 2 -----------------------------------------------------------------------
class Transaction:
    """A fake transaction with commit and rollback.

    Requirements:
      - on clean exit: commit
      - on exception:  rollback, then let the exception propagate
      - nested transactions become SAVEPOINTS: an inner rollback must not
        discard the outer transaction's work
      - .operations records what happened, in order, so tests can assert on it

    Then answer in a comment: why must __exit__ re-raise rather than return
    True, even though "the rollback handled it" sounds reasonable?
    """

    def __init__(self, name: str = "tx") -> None:
        self.name = name
        self.operations: list[str] = []


# TODO 3 -----------------------------------------------------------------------
@contextmanager
def temporary_directory(prefix: str = "tmp"):  # type: ignore[no-untyped-def]
    """Create a temp directory, yield its Path, remove it afterwards.

    Requirements:
      - removal happens even if the block raises
      - removal happens even if the block CREATED files inside it
      - if removal itself fails, do not mask the block's exception

    That last requirement is subtle and is where most hand-rolled cleanup goes
    wrong. Work out what happens if both the body and the cleanup raise, and
    write down which exception a caller sees and which is lost.
    """
    raise NotImplementedError


# TODO 4 -----------------------------------------------------------------------
class suppress_and_log:
    """Like contextlib.suppress, but records what it swallowed.

    Requirements:
      - suppress ONLY the listed exception types
      - record each suppressed exception in .caught
      - anything not listed propagates untouched
      - be reusable and REENTRANT: the same instance used in two nested with
        blocks must work

    Then answer: contextlib.suppress is one of the very few legitimate uses of
    returning True from __exit__. What makes it legitimate, and what makes
    almost every other use of it a bug?
    """

    def __init__(self, *exceptions: type[BaseException]) -> None:
        self.exceptions = exceptions
        self.caught: list[BaseException] = []


def verify() -> None:
    with Timer() as t:
        time.sleep(0.01)
    assert t.elapsed >= 0.01

    try:
        with Timer() as t2:
            raise ValueError("boom")
    except ValueError:
        pass
    assert t2.elapsed > 0, "timer must record even when the block raises"

    tx = Transaction()
    with tx:
        tx.operations.append("insert")
    assert tx.operations[-1] == "commit", tx.operations

    tx2 = Transaction()
    try:
        with tx2:
            tx2.operations.append("insert")
            raise RuntimeError("fail")
    except RuntimeError:
        pass
    else:
        raise AssertionError("exception must propagate")
    assert tx2.operations[-1] == "rollback", tx2.operations

    with temporary_directory() as d:
        assert d.is_dir()
        (d / "file.txt").write_text("data", encoding="utf-8")
        kept = d
    assert not kept.exists(), "temp directory survived"

    try:
        with temporary_directory() as d2:
            kept2 = d2
            raise ValueError("boom")
    except ValueError:
        pass
    assert not kept2.exists(), "temp directory survived an exception"

    s = suppress_and_log(ValueError, KeyError)
    with s:
        raise ValueError("swallowed")
    assert len(s.caught) == 1

    with s:
        raise KeyError("also swallowed")
    assert len(s.caught) == 2

    try:
        with s:
            raise TypeError("not listed")
    except TypeError:
        pass
    else:
        raise AssertionError("unlisted exceptions must propagate")

    print("all context manager checks passed")


if __name__ == "__main__":
    verify()
