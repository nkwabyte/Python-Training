"""Uses a RELATIVE import. Try running this file directly."""

from .util import helper


def run(x: int) -> int:
    return helper(x) + 1


if __name__ == "__main__":
    print(f"__package__ = {__package__!r}")
    print(run(20))
