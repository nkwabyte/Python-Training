"""Exercise 05.1 — Predict, then measure.

Fill in the PREDICTION column of the table below BEFORE running. Then run and
compare. The goal is not to memorise the table; it is to notice which of your
intuitions are wrong.

Run:  python ex01_complexity.py
"""

from __future__ import annotations

import timeit
from collections import deque

PREDICTIONS = """
Operation                          | Your prediction (O(?)) | Measured growth
-----------------------------------|------------------------|----------------
list[i]                            |                        |
list.append                        |                        |
list.insert(0, x)                  |                        |
list.pop()                         |                        |
list.pop(0)                        |                        |
x in list                          |                        |
x in set                           |                        |
x in dict                          |                        |
dict[k] = v                        |                        |
deque.appendleft                   |                        |
sorted(list)                       |                        |
list[:] (full slice copy)          |                        |
"""


# TODO 1 -----------------------------------------------------------------------
def measure(setup: str, stmt: str, sizes: list[int]) -> list[float]:
    """Time `stmt` at each size and return per-operation times in microseconds.

    Use timeit.timeit with a `number` chosen so each measurement takes roughly
    a tenth of a second -- too few repetitions and the timer noise dominates,
    too many and you wait forever.

    Hint: timeit.timeit(stmt, setup, number=N) returns TOTAL seconds for N
    repetitions.
    """
    raise NotImplementedError


# TODO 2 -----------------------------------------------------------------------
def growth_ratio(times: list[float]) -> list[float]:
    """Given timings at sizes n, 2n, 4n, 8n..., return the ratio between
    consecutive measurements.

    Interpreting the ratios is the whole exercise:
      ~1.0  -> O(1)        the size did not matter
      ~2.0  -> O(n)        doubling the input doubled the time
      ~2.2  -> O(n log n)  slightly worse than doubling
      ~4.0  -> O(n^2)      doubling the input quadrupled the time
    """
    raise NotImplementedError


# TODO 3 -----------------------------------------------------------------------
def run_all() -> None:
    """Measure all twelve operations across at least four sizes and print a
    table of times and growth ratios.

    Watch out for these measurement traps -- each one will give you a wrong
    answer if you miss it:

    a) DESTRUCTIVE operations. Timing `lst.pop()` a million times empties the
       list, and then you are timing IndexError handling. Rebuild the structure
       in the setup, or measure a fixed number of pops against a fresh copy.

    b) The SETUP is not timed, so building the list in setup is free. Make sure
       the work you want to measure is in stmt and nothing else is.

    c) MEMBERSHIP tests need a MISSING element to measure the worst case. `0 in
       lst` finds it immediately and measures nothing. Search for something that
       is not there.

    d) SORTING an already-sorted list is O(n) with Timsort, not O(n log n) --
       Timsort detects existing runs. Shuffle first, and use a fresh shuffled
       copy per repetition.
    """
    raise NotImplementedError


# TODO 4 -----------------------------------------------------------------------
def amortization_demo() -> None:
    """Show that append is amortized O(1) by finding the resize events.

    Append to a list one element at a time, recording sys.getsizeof(lst) after
    each append. Print only the sizes at which the allocated size CHANGED.

    Then answer:
      - what is the pattern of the growth?  (compute each jump as a ratio)
      - how many resizes happen in a million appends? Roughly.
      - therefore, what fraction of appends pay the copy cost?
      - and so: why is "amortized O(1)" honest rather than a fudge?
    """
    raise NotImplementedError


# TODO 5 -----------------------------------------------------------------------
def crossover_point() -> None:
    """Find where `set` beats `list` for membership.

    For n = 1, 2, 4, 8, ... 4096, time k membership tests against a list of n
    items and against a set of n items, INCLUDING the cost of building the set.

    Report the n at which the set version becomes faster.

    The answer is smaller than most people guess, and it is the practical
    justification for "just use a set".
    """
    raise NotImplementedError


if __name__ == "__main__":
    print(PREDICTIONS)
    run_all()
    amortization_demo()
    crossover_point()
