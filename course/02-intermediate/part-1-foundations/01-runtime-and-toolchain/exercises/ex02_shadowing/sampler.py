"""Draws a sample from a population."""

from __future__ import annotations

import random


def take_sample(population: list[int], k: int) -> list[int]:
    """Return k randomly chosen items from population, without replacement."""
    return random.sample(population, k)


def shuffled(population: list[int]) -> list[int]:
    copy = list(population)
    random.shuffle(copy)
    return copy


if __name__ == "__main__":
    print(take_sample(list(range(100)), 5))
