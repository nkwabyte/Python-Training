"""Solution 01.3 — __name__ and the import guard.

Run:     python ex03_name_main_solution.py Ada Grace
Import:  python -c "import ex03_name_main_solution"   # prints only the __name__ line
"""

from __future__ import annotations

import sys
from pathlib import Path

# TODO 1 solved. Instructive while learning; delete it in real code.
print(f"[module loaded, __name__ == {__name__!r}]", file=sys.stderr)

CONFIG_PATH = Path(__file__).parent / "greeting.txt"
FALLBACK_GREETING = "Hello"


def load_config(path: Path = CONFIG_PATH) -> str:
    """Read the configured greeting, falling back to a default.

    TODO 3 solved: this touches the filesystem only when CALLED. Importing a
    module must never do I/O. A module that reads a file at import time cannot
    be imported by a test suite, cannot be imported in an environment where
    that file is absent, and makes import order significant -- three bugs for
    the price of one convenience.

    The path is a parameter with a default rather than a hardcoded global,
    which is what makes this function testable with tmp_path (Module 18).
    """
    try:
        text = path.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeDecodeError):
        return FALLBACK_GREETING
    return text or FALLBACK_GREETING


def greet(name: str, greeting: str = FALLBACK_GREETING) -> str:
    """Return a greeting. TODO 2 solved: returns, does not print.

    Separating computation from I/O is the difference between a function you
    can test with `assert greet("Ada") == "Hello, Ada!"` and one you can only
    test by capturing stdout.
    """
    return f"{greeting}, {name}!"


def main(argv: list[str]) -> int:
    """TODO 4 solved.

    argv is a PARAMETER, not sys.argv read from inside. That single choice is
    what lets a test call main(["Ada"]) and assert on the return code without
    monkeypatching the interpreter's global state.
    """
    if not argv:
        print("usage: ex03_name_main_solution.py NAME [NAME ...]", file=sys.stderr)
        return 2

    greeting = load_config()
    for name in argv:
        print(greet(name, greeting))
    return 0


if __name__ == "__main__":  # TODO 5 solved
    raise SystemExit(main(sys.argv[1:]))
