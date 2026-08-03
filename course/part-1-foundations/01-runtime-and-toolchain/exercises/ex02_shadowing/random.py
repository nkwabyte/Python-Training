"""Project-local helpers for randomised sampling.

Written by a well-meaning developer who did not know this name was taken.
"""


def coin_flip(seed: int) -> bool:
    """A deterministic pseudo-'random' flip, for reproducible tests."""
    return (seed * 1103515245 + 12345) % 2 == 0


def spread(n: int) -> list[int]:
    """Return n values spread across a range, deterministically."""
    return [(i * 37) % 100 for i in range(n)]
