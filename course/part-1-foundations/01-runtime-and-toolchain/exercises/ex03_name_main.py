"""Exercise 01.3 — __name__ and the import guard.

Goal: understand exactly what changes between importing a file and running it,
and write a module that behaves correctly in both situations.

Run this file directly:      python ex03_name_main.py
Import it from a REPL:       import ex03_name_main

TODO 1
------
Add a module-level print showing the value of __name__ (leave it in while you
experiment; it is instructive, and you will remove it in TODO 5).

TODO 2
------
`greet` currently prints. That makes it untestable and unusable as a library
function. Change it to RETURN the string, and have the caller print. This is a
general principle: functions that compute should not also do I/O.

TODO 3
------
`load_config` reads a file at import time. That is wrong: importing a module
should not touch the filesystem. Move the work so that it happens only when
someone calls the function.

TODO 4
------
Write `main(argv)` that:
  - takes a list of command line arguments (do not read sys.argv inside it)
  - greets each name given on the command line
  - if no names are given, prints usage to stderr and returns exit code 2
  - returns 0 on success
Taking argv as a parameter rather than reading the global is what makes main()
testable. You will use this pattern in every CLI in this course.

TODO 5
------
Add the __main__ guard at the bottom that calls main with sys.argv[1:] and
exits with its return code.

VERIFY
------
  python ex03_name_main.py Ada Grace     -> greets both, exit code 0
  python ex03_name_main.py               -> usage on stderr, exit code 2
  echo $?                                -> check the exit code
  python -c "import ex03_name_main"      -> prints NOTHING except the __name__
                                            line from TODO 1

That last one is the real test. If importing your module does anything visible,
the guard is wrong.
"""

from __future__ import annotations

import sys
from pathlib import Path

# TODO 1: print __name__ here


CONFIG_PATH = Path(__file__).parent / "greeting.txt"

# TODO 3: this runs at import time. It should not.
DEFAULT_GREETING = "Hello"
if CONFIG_PATH.exists():
    DEFAULT_GREETING = CONFIG_PATH.read_text(encoding="utf-8").strip()


def greet(name: str, greeting: str = DEFAULT_GREETING) -> None:
    # TODO 2: return the string instead of printing it
    print(f"{greeting}, {name}!")


def load_config() -> str:
    # TODO 3: move the file reading in here, with a sensible fallback
    return DEFAULT_GREETING


# TODO 4: def main(argv: list[str]) -> int: ...


# TODO 5: the guard
