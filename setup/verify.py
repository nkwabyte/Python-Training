#!/usr/bin/env python3
"""Verify that the course environment is set up correctly.

Run this before Module 01:

    python setup/verify.py

It checks four things, in the order that they break:

1. The interpreter version.
2. That you are inside a virtual environment (the single most common problem).
3. That the development toolchain is importable.
4. That a tiny end-to-end example actually runs.

Deliberately written with no third-party imports at module level, so that it
can report a missing toolchain instead of crashing on it.
"""

from __future__ import annotations

import importlib.util
import platform
import sys
from pathlib import Path

MIN_VERSION = (3, 12)
RECOMMENDED_TOOLS = ["ruff", "mypy", "pytest", "hypothesis", "IPython", "rich"]

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
DIM = "\033[2m"
RESET = "\033[0m"


def ok(msg: str) -> None:
    print(f"{GREEN}  PASS{RESET}  {msg}")


def warn(msg: str) -> None:
    print(f"{YELLOW}  WARN{RESET}  {msg}")


def fail(msg: str) -> None:
    print(f"{RED}  FAIL{RESET}  {msg}")


def hint(msg: str) -> None:
    print(f"{DIM}        -> {msg}{RESET}")


def check_version() -> bool:
    print("\n[1/4] Interpreter")
    v = sys.version_info
    actual = f"{v.major}.{v.minor}.{v.micro}"
    print(f"        {platform.python_implementation()} {actual} at {sys.executable}")
    if (v.major, v.minor) >= MIN_VERSION:
        ok(f"Python {actual} meets the 3.12+ requirement")
        return True
    if (v.major, v.minor) >= (3, 10):
        warn(f"Python {actual}: most of the course works, some modules flag 3.12+")
        hint("Install 3.12 with: uv python install 3.12")
        return True
    fail(f"Python {actual} is too old for this course")
    hint("See SETUP.md section 2")
    return False


def check_virtualenv() -> bool:
    print("\n[2/4] Virtual environment")
    in_venv = sys.prefix != sys.base_prefix
    if in_venv:
        ok(f"Running inside a virtual environment: {sys.prefix}")
        return True
    fail("You are using the system interpreter, not a virtual environment")
    hint("uv venv --python 3.12 && source .venv/bin/activate")
    hint("or: python3.12 -m venv .venv && source .venv/bin/activate")
    return False


def check_tools() -> bool:
    print("\n[3/4] Development toolchain")
    missing: list[str] = []
    for name in RECOMMENDED_TOOLS:
        if importlib.util.find_spec(name) is not None:
            ok(f"{name} importable")
        else:
            fail(f"{name} not found")
            missing.append(name)
    if missing:
        hint("uv pip install -r requirements-dev.txt")
        return False
    return True


def check_example() -> bool:
    """Run a tiny typed function and a tiny test, in-process."""
    print("\n[4/4] End-to-end sanity check")

    def mean(values: list[float]) -> float:
        if not values:
            raise ValueError("mean() of empty sequence")
        return sum(values) / len(values)

    try:
        assert mean([1.0, 2.0, 3.0]) == 2.0
    except AssertionError:
        fail("arithmetic sanity check failed (this should be impossible)")
        return False

    try:
        mean([])
    except ValueError:
        ok("functions, exceptions, and assertions all behave")
    else:
        fail("expected ValueError was not raised")
        return False

    root = Path(__file__).resolve().parent.parent
    curriculum = root / "CURRICULUM.md"
    if curriculum.exists():
        ok(f"course tree found at {root}")
    else:
        warn("could not locate CURRICULUM.md; are you running from the repo root?")
    return True


def main() -> int:
    print("=" * 62)
    print(" Python Training - environment verification")
    print("=" * 62)

    results = [
        check_version(),
        check_virtualenv(),
        check_tools(),
        check_example(),
    ]

    print("\n" + "=" * 62)
    if all(results):
        print(f"{GREEN} ALL CHECKS PASSED{RESET}  Open Module 01 and begin.")
        print("=" * 62)
        return 0
    print(f"{RED} SOME CHECKS FAILED{RESET}  Fix the items above, then re-run.")
    print(" See SETUP.md section 9 for the common causes.")
    print("=" * 62)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
