"""Uses an ABSOLUTE import. Compare with core.py."""

VERSION = "1.0"


def helper(x: int) -> int:
    return x * 2


if __name__ == "__main__":
    print(helper(21))
