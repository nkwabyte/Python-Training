"""Exercise 14.1 — The protocol, by hand and by yield.

Run:  python ex01_protocol.py
"""
from __future__ import annotations

from collections.abc import Iterator


# TODO 1: implement the protocol BY HAND, correctly ---------------------------
class Fibonacci:
    """Yield the first n Fibonacci numbers.

    Write TWO classes: Fibonacci (the iterable) and FibonacciIterator (the
    cursor). Fibonacci.__iter__ must return a FRESH cursor each call.

    Then write BrokenFibonacci, whose __iter__ returns self, and demonstrate
    with an assertion that two consecutive for loops over it disagree.
    """


# TODO 2: the same thing with yield -------------------------------------------
class FibonacciGen:
    """One class, one method, three lines. Two loops both work, because each
    call to __iter__ creates a new generator with its own locals."""


# TODO 3: an iterable that is expensive to produce -----------------------------
class Countdown:
    """Print something in __iter__ AND in the body, then show:
      - creating the object prints nothing
      - calling iter() prints nothing (why not? think about what a generator
        function call does)
      - the first next() prints both
    """


# TODO 4: infinite ------------------------------------------------------------
def primes() -> Iterator[int]:
    """An infinite generator of primes. Must work with islice and takewhile,
    and must not precompute a bound."""
    raise NotImplementedError


# TODO 5: the exhaustion bug, deliberately -------------------------------------
def average_and_max(numbers) -> tuple[float, float]:  # type: ignore[no-untyped-def]
    """Currently iterates its argument TWICE. Given a generator, the second
    pass sees nothing and max() raises on an empty sequence.

    Fix it THREE ways and say when each is right:
      (a) materialise with list() at the top
      (b) one pass, tracking both values
      (c) change the signature to Sequence and let the type checker enforce it
    """
    total = sum(numbers)
    count = sum(1 for _ in numbers)          # already empty
    return total / count, max(numbers)


def verify() -> None:
    fib = FibonacciGen(10)                                # type: ignore[name-defined]
    assert list(fib) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert list(fib) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34], "must be reusable"

    from itertools import islice, takewhile
    assert list(islice(primes(), 5)) == [2, 3, 5, 7, 11]
    assert list(takewhile(lambda p: p < 20, primes())) == [2, 3, 5, 7, 11, 13, 17, 19]

    assert average_and_max([1, 2, 3]) == (2.0, 3)
    assert average_and_max(x for x in [1, 2, 3]) == (2.0, 3), (
        "must work on a one-shot iterable"
    )
    print("all protocol checks passed")


if __name__ == "__main__":
    verify()
