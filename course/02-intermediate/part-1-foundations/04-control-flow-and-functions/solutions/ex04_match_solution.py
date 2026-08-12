"""Solution 04.4 — Structural pattern matching."""

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


def run_command(line: str) -> str:
    match line.split():
        case ["go", direction]:                 # fixed-length sequence, capture
            return f"moving {direction}"
        case ["take", *items] if items:         # star pattern + guard
            return "taking: " + ", ".join(items)
        case ["take"]:
            return "take what?"
        case ["look"]:
            return "you see nothing"
        case ["quit"] | ["exit"]:               # alternation
            return "goodbye"
        case []:
            return "say something"
        case _:
            return f"I do not understand '{line}'"


def describe_event(event: dict[str, Any]) -> str:
    """Mapping patterns match a SUBSET of keys.

    {"type": "click", "pos": (1,2), "timestamp": 999} still matches
    case {"type": "click", "pos": (x, y)} -- the extra key is ignored.

    IS THAT WHAT YOU WANT FOR AN EVENT ROUTER? Yes, and it is the right default.
    Events gain fields over time (a timestamp, a trace ID, a schema version),
    and a router that broke whenever a producer added a field would be
    unusable. It is the same reasoning as tolerant reading in protocol design:
    ignore what you do not understand.

    The cost is that a typo'd or extra key is silently accepted, so this is NOT
    validation. Validate at the boundary with a schema (Module 28); route on
    shape here.
    """
    match event:
        case {"type": "click", "pos": (0, 0)}:              # literal inside
            return "click at origin"
        case {"type": "click", "pos": (int(x), int(y))}:    # type + capture
            return f"click at {x},{y}"
        case {"type": "key", "code": 27}:
            return "escape"
        case {"type": "key", "code": int(code)}:            # int() is a CLASS
            return f"key {code}"                            # pattern, not a call
        case {"type": "key"}:
            return "bad key event"
        case {"type": "scroll", "delta": int(d)} if d < 0:  # guard
            return f"scroll up {abs(d)}"
        case {"type": "scroll", "delta": int(d)} if d > 0:
            return f"scroll down {d}"
        case _:
            return "unknown event"


def classify_point(p: Point) -> str:
    """@dataclass generates __match_args__ = ('x', 'y'), which is what makes
    the POSITIONAL form Point(0, 0) work. Without it you get:

        TypeError: Point() accepts 0 positional sub-patterns

    and must write the keyword form Point(x=0, y=0). NamedTuple and dataclass
    both provide it; a plain class does not unless you set it yourself.
    """
    match p:
        case Point(0, 0):
            return "origin"
        case Point(_, 0):
            return "on the x axis"
        case Point(0, _):
            return "on the y axis"
        case Point(x=a, y=b) if a == b:
            return "on the diagonal"
        case Point(x=a, y=b):
            return f"at {a},{b}"
        case _:
            return "not a point"


def check_status_BROKEN(status: Status) -> str:
    """WHY THIS RETURNS "all good" FOR Status.PENDING.

    `case OK:` is a CAPTURE pattern, not a comparison. A bare identifier in a
    pattern position means "match anything and bind it to this name". So the
    second case matches EVERY value that did not match the first, and rebinds
    the local OK to it. Status.PENDING falls through to it and reports
    "all good".

    Only these COMPARE rather than capture:
      - dotted names        case Status.OK:
      - literals            case 27:  case "quit":  case None:
      - class patterns      case Point(0, 0):
      - a guard             case x if x is Status.OK:

    The single underscore _ is the one bare name that does not bind; it is the
    wildcard.

    A GENUINELY USEFUL SAFETY NET: if a bare-name capture is followed by any
    further cases, CPython refuses to compile the file at all:

        SyntaxError: name capture 'OK' makes remaining patterns unreachable

    So the compiler catches the trap whenever it makes later branches dead.
    It cannot catch it when the capture is the LAST case, which is exactly the
    version written here -- and exactly the version that ships to production.
    Both mypy and ruff can flag the remaining form; turn that rule on.
    """
    OK = Status.OK  # noqa: N806
    match status:
        case Status.ERROR:
            return "failed"
        case OK:
            return "all good"


def check_status(status: Status) -> str:
    match status:
        case Status.OK:              # dotted name: COMPARED
            return "all good"
        case Status.ERROR:
            return "failed"
        case Status.PENDING:
            return "pending"
        case _:
            return "unknown"


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
        "the capture trap has been fixed in the BROKEN version; restore it"
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
