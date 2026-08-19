"""Core business logic for pkgdemo."""

from __future__ import annotations
import sys


def format_greeting(name: str) -> str:
    """Return a formatted greeting message."""
    clean_name = name.strip()
    if not clean_name:
        raise ValueError("Name cannot be empty")
    return f"Hello, {clean_name}! Welcome to Python Packaging."


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint."""
    args = argv if argv is not None else sys.argv[1:]
    target_name = args[0] if args else "Developer"
    try:
        print(format_greeting(target_name))
        return 0
    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
