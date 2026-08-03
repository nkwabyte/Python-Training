"""Enables `python -m inventory`.

Deliberately a THIN shim. Anything defined here would live in a module called
"__main__", so if another module also imported it by its real name you would
get two distinct classes with the same name and isinstance would fail
mysteriously (Module 06).
"""

from inventory.cli import run

if __name__ == "__main__":
    run()
