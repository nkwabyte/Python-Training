"""Summary statistics over a list of numbers."""

from __future__ import annotations


def mean(values: list[float]) -> float:
    if not values:
        raise ValueError("mean() of empty sequence")
    return sum(values) / len(values)


def spread_of(values: list[float]) -> float:
    if not values:
        raise ValueError("spread_of() of empty sequence")
    return max(values) - min(values)
