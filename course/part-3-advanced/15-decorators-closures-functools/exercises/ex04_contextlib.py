"""Exercise 15.4 — contextlib, including the case hand-rolling gets wrong.

Run:  python ex04_contextlib.py
"""
from __future__ import annotations

import contextlib
from pathlib import Path
from typing import Any

# TODO 1  @contextmanager-based `chdir` that restores the previous directory
#         even on an exception. (3.11 has contextlib.chdir -- write it anyway,
#         then compare.)
#
# TODO 2  A `transaction` context manager over a fake connection: commit on
#         success, rollback on exception, and NEVER swallow. Support nesting
#         via savepoints.
#
# TODO 3  open_all(paths) using ExitStack: open N files, yield them, close all
#         of them in reverse order on exit.
#         THE POINT: make open() fail on the THIRD of five paths, and assert
#         that the first two were still closed. Write the hand-rolled version
#         first (a list of files and a try/finally loop) and find the bug in
#         it -- it is subtle and it is why ExitStack exists.
#
# TODO 4  A `maybe` helper returning either a real context manager or
#         contextlib.nullcontext(), so a caller can write:
#             with maybe(verbose, timer()):
#                 ...
#         instead of duplicating the body under an if.


def verify() -> None:
    original = Path.cwd()
    with chdir("/tmp"):                              # type: ignore[name-defined]
        assert Path.cwd() == Path("/tmp")
    assert Path.cwd() == original

    try:
        with chdir("/tmp"):                          # type: ignore[name-defined]
            raise ValueError("boom")
    except ValueError:
        pass
    assert Path.cwd() == original, "must restore on an exception too"

    conn = FakeConnection()                          # type: ignore[name-defined]
    with transaction(conn):                          # type: ignore[name-defined]
        conn.execute("INSERT 1")
    assert conn.log[-1] == "COMMIT", conn.log

    conn2 = FakeConnection()                         # type: ignore[name-defined]
    try:
        with transaction(conn2):                     # type: ignore[name-defined]
            conn2.execute("INSERT 1")
            raise RuntimeError("fail")
    except RuntimeError:
        pass
    else:
        raise AssertionError("transaction must not swallow")
    assert conn2.log[-1] == "ROLLBACK", conn2.log

    import tempfile
    with tempfile.TemporaryDirectory() as td:
        paths = [Path(td) / f"f{i}.txt" for i in range(5)]
        for p in paths[:2]:
            p.write_text("data", encoding="utf-8")
        # paths[2] does not exist -> open() raises on the third
        opened: list[Any] = []
        try:
            with open_all(paths, record=opened):     # type: ignore[name-defined]
                raise AssertionError("should not reach the body")
        except FileNotFoundError:
            pass
        assert len(opened) == 2, "two files were opened"
        assert all(f.closed for f in opened), (
            "the first two files must be closed despite the third failing"
        )

    print("all contextlib checks passed")


if __name__ == "__main__":
    verify()
