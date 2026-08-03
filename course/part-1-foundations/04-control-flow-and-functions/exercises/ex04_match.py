"""Exercise 04.4 — Structural pattern matching.

Two parsers, built with `match`. Includes the capture-versus-compare trap,
which you will hit at least once whether or not you are warned.

Run:  python ex04_match.py
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class Status(Enum):
    OK = "ok"
    ERROR = "error"
    PENDING = "pending"


@dataclass
class Point:
    x: int
    y: int


# TODO 1 -----------------------------------------------------------------------
def run_command(line: str) -> str:
    """Parse a command line with `match` on line.split().

      "go north"            -> "moving north"
      "take sword shield"   -> "taking: sword, shield"
      "take"                -> "take what?"
      "look"                -> "you see nothing"
      "quit" or "exit"      -> "goodbye"
      "" (empty)            -> "say something"
      anything else         -> "I do not understand 'xyz'"

    Use sequence patterns, a star pattern, and an alternation. Do NOT use
    if/elif -- the point is to practise the patterns.
    """
    raise NotImplementedError


# TODO 2 -----------------------------------------------------------------------
def describe_event(event: dict[str, Any]) -> str:
    """Match on the SHAPE of a dict.

      {"type": "click", "pos": (0, 0)}          -> "click at origin"
      {"type": "click", "pos": (x, y)}          -> "click at 3,4"
      {"type": "key", "code": 27}               -> "escape"
      {"type": "key", "code": <int>}            -> "key 65"
      {"type": "key", "code": <non-int>}        -> "bad key event"
      {"type": "scroll", "delta": <negative>}   -> "scroll up 3"   (use a guard)
      {"type": "scroll", "delta": <positive>}   -> "scroll down 3"
      anything else                             -> "unknown event"

    Note that a mapping pattern matches on a SUBSET of keys -- extra keys in the
    event do not prevent a match. Verify that, then say in a comment whether
    that is the behaviour you want for an event router and why.
    """
    raise NotImplementedError


# TODO 3 -----------------------------------------------------------------------
def classify_point(p: Point) -> str:
    """Class patterns.

      Point(0, 0)    -> "origin"
      Point(x, 0)    -> "on the x axis"
      Point(0, y)    -> "on the y axis"
      Point(x, x)    -> "on the diagonal"      (use a guard: x == y)
      otherwise      -> "at 3,4"

    @dataclass generates __match_args__, which is what makes POSITIONAL class
    patterns like Point(0, 0) work. Try removing @dataclass and see the error;
    that tells you what __match_args__ is for.
    """
    raise NotImplementedError


# TODO 4 -----------------------------------------------------------------------
def check_status_BROKEN(status: Status) -> str:
    """This function is WRONG. Run it with Status.PENDING, see what happens,
    then explain why in a comment before fixing it below.

    This is the single most common `match` bug.

    Bonus experiment: move `case OK:` ABOVE `case Status.ERROR:` and try to run
    the file. CPython refuses to compile it, with a message that tells you
    exactly what is wrong. Why can the compiler catch that arrangement and not
    this one?
    """
    OK = Status.OK  # noqa: N806
    match status:
        case Status.ERROR:
            return "failed"
        case OK:
            return "all good"


def check_status(status: Status) -> str:
    """TODO: the corrected version."""
    raise NotImplementedError


# --- tests --------------------------------------------------------------------
def test_run_command() -> None:
    assert run_command("go north") == "moving north"
    assert run_command("take sword shield") == "taking: sword, shield"
    assert run_command("take") == "take what?"
    assert run_command("look") == "you see nothing"
    assert run_command("quit") == "goodbye"
    assert run_command("exit") == "goodbye"
    assert run_command("") == "say something"
    assert run_command("dance wildly") == "I do not understand 'dance wildly'"


def test_describe_event() -> None:
    assert describe_event({"type": "click", "pos": (0, 0)}) == "click at origin"
    assert describe_event({"type": "click", "pos": (3, 4)}) == "click at 3,4"
    assert describe_event({"type": "key", "code": 27}) == "escape"
    assert describe_event({"type": "key", "code": 65}) == "key 65"
    assert describe_event({"type": "key", "code": "a"}) == "bad key event"
    assert describe_event({"type": "scroll", "delta": -3}) == "scroll up 3"
    assert describe_event({"type": "scroll", "delta": 3}) == "scroll down 3"
    assert describe_event({"type": "mystery"}) == "unknown event"
    # extra keys must not prevent a match
    assert describe_event(
        {"type": "click", "pos": (1, 2), "timestamp": 999}) == "click at 1,2"


def test_classify_point() -> None:
    assert classify_point(Point(0, 0)) == "origin"
    assert classify_point(Point(5, 0)) == "on the x axis"
    assert classify_point(Point(0, 5)) == "on the y axis"
    assert classify_point(Point(3, 3)) == "on the diagonal"
    assert classify_point(Point(3, 4)) == "at 3,4"


def test_status() -> None:
    assert check_status_BROKEN(Status.ERROR) == "failed"
    assert check_status_BROKEN(Status.PENDING) == "all good", (
        "if this fails the trap has been fixed in the BROKEN version; "
        "restore it so you can see the bug"
    )
    assert check_status(Status.OK) == "all good"
    assert check_status(Status.ERROR) == "failed"
    assert check_status(Status.PENDING) == "pending"


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"  PASS  {t.__name__}")
    print(f"\n{len(tests)} tests passed")
