"""Exercise 08.4 — Does __slots__ actually matter?

Measure, do not assume. Find the instance count at which the memory saving
stops being a rounding error and starts being a decision.

Run:  python ex04_slots_bench.py
"""

from __future__ import annotations

import sys
import timeit
import tracemalloc


class PointDict:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x, self.y, self.z = x, y, z


class PointSlots:
    __slots__ = ("x", "y", "z")

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x, self.y, self.z = x, y, z


# TODO 1 -----------------------------------------------------------------------
def measure_single_instance() -> None:
    """Report sys.getsizeof for one instance of each, AND for its __dict__.

    TRAP: sys.getsizeof(obj) does NOT include the __dict__ it points at. Add
    them. Getting this wrong makes __slots__ look like it saves 8 bytes.

    Then answer: what does sys.getsizeof miss even after you add the dict?
    (Hint: what do the x, y and z attributes point AT?)
    """
    raise NotImplementedError


# TODO 2 -----------------------------------------------------------------------
def measure_at_scale(counts: tuple[int, ...] = (1_000, 10_000, 100_000, 1_000_000)) -> None:
    """Use tracemalloc to measure ACTUAL allocated memory for a list of N
    instances of each class. Print a table with the saving in MB and as a
    percentage.

    Use tracemalloc, not sum(getsizeof(...)): getsizeof is per-object and
    ignores allocator overhead, shared references, and the list holding them.
    tracemalloc measures what the process really allocated, which is the number
    you actually care about.
    """
    raise NotImplementedError


# TODO 3 -----------------------------------------------------------------------
def measure_access_speed() -> None:
    """Time attribute reads, writes, and instance creation for both.

    Predict the direction of each result BEFORE running. Then answer:
      - is the speed difference large enough to be a reason on its own?
      - which of the three operations differs most, and why?
    """
    raise NotImplementedError


# TODO 4 -----------------------------------------------------------------------
def what_breaks() -> None:
    """Demonstrate, with a try/except around each, the five things __slots__
    takes away:

      1. assigning a new attribute
      2. having a __dict__ at all
      3. weakref.ref(instance)          -- unless '__weakref__' is in __slots__
      4. functools.cached_property      -- it needs somewhere to store the value
      5. multiple inheritance from two classes that both define non-empty
         __slots__

    For each, print what happened, and write down whether it would matter for:
      (a) a Point in a physics engine
      (b) a User in a web application
      (c) a Node in a parser
    """
    raise NotImplementedError


# TODO 5 -----------------------------------------------------------------------
def with_dataclass() -> None:
    """Compare a hand-written __slots__ class with @dataclass(slots=True).

    Show they use the same memory, and count the lines of code each took.
    Then say which you would write, and why the answer changed in 3.10.
    """
    raise NotImplementedError


if __name__ == "__main__":
    measure_single_instance()
    measure_at_scale()
    measure_access_speed()
    what_breaks()
    with_dataclass()
