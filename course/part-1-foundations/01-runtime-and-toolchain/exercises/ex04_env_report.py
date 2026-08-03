"""Exercise 01.4 — Build an environment diagnostic tool.

You will genuinely reuse this. Every time an import misbehaves, running one
script that answers "which interpreter, which environment, which paths" is
faster than remembering four separate commands.

Target output (yours can look different, but must contain this information):

    Interpreter
      implementation : CPython 3.12.4
      executable     : /home/me/proj/.venv/bin/python
      prefix         : /home/me/proj/.venv
      base_prefix    : /usr

    Environment
      virtualenv     : YES (.venv)
      VIRTUAL_ENV    : /home/me/proj/.venv
      site-packages  : /home/me/proj/.venv/lib/python3.12/site-packages
      installed      : 42 distributions

    Import path (sys.path)
      [0] /home/me/proj              <- script directory, searched FIRST
      [1] /usr/lib/python312.zip
      ...

    Shadowing check
      OK   no local files shadow a standard library module

Requirements
------------
TODO 1  Report implementation name and version, executable, prefix, base_prefix.
        Hint: sys.implementation, sys.version_info, sys.executable, sys.prefix,
        sys.base_prefix.

TODO 2  Detect whether you are inside a virtual environment. The reliable test
        is sys.prefix != sys.base_prefix. Explain in a comment why checking the
        VIRTUAL_ENV environment variable alone is NOT reliable.

TODO 3  Print sys.path with indices, and annotate index 0 with what it means.

TODO 4  Write check_shadowing(): for every .py file in the current directory,
        report it if its stem matches the name of a standard library module.
        Hint: sys.stdlib_module_names is a frozenset available since 3.10.
        This is the highest-value function in the tool.

TODO 5  Count installed distributions.
        Hint: importlib.metadata.distributions()

TODO 6  Return exit code 1 if any shadowing is detected, 0 otherwise, so the
        script can be used in a CI check.

STRETCH Report the 5 slowest imports using -X importtime data, or add a --json
        flag that emits the same information as machine-readable JSON.
"""

from __future__ import annotations

import sys

# TODO: everything


def main() -> int:
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
