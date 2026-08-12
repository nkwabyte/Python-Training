"""Exercise 02.5 — Reference counting, cycles, and weakref.

Observation exercise with code. Fill in the TODOs, run it, and answer the
questions in the ANSWERS block.

Everything here is CPython-specific. Note that as you go: on PyPy, none of the
refcount observations hold, and the destruction timing is completely different.

Run:  python ex05_refcount_lab.py
"""

from __future__ import annotations

import gc
import sys
import weakref
from typing import Any


class Tracked:
    """An object that announces its own destruction."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.ref: Tracked | None = None

    def __repr__(self) -> str:
        return f"Tracked({self.name!r})"

    def __del__(self) -> None:
        print(f"    [{self.name} destroyed]")


# TODO 1 -----------------------------------------------------------------------
def part1_refcounts() -> None:
    """Observe refcounts rising and falling.

    Create a list, print sys.getrefcount for it, bind a second name, print
    again, delete one, print again.

    QUESTION: sys.getrefcount always reports one MORE than you expect. Why?
    (Hint: what happened to the object in order to be passed to the function?)
    """
    raise NotImplementedError


# TODO 2 -----------------------------------------------------------------------
def part2_deterministic_destruction() -> None:
    """Show that the last name going away destroys the object immediately.

    Create Tracked("solo"), print "before del", del it, print "after del".

    QUESTION: which order did the three lines print in, and what does that tell
    you about WHEN __del__ ran relative to the `del` statement?
    """
    raise NotImplementedError


# TODO 3 -----------------------------------------------------------------------
def part3_cycle() -> None:
    """Build a cycle and show it is NOT freed by refcounting alone.

    Create Tracked("A") and Tracked("B"), point each one's .ref at the other,
    then delete both names. Print "names deleted". Then call gc.collect() and
    print how many objects it collected.

    QUESTION: between "names deleted" and the gc.collect() line, were A and B
    reachable from any name? Were they freed? What does that gap represent in
    a long-running server?
    """
    raise NotImplementedError


# TODO 4 -----------------------------------------------------------------------
def part4_weakref() -> None:
    """Break the cycle with a weak reference.

    Build the same A/B pair, but make B's back-reference a weakref.ref(A)
    instead of a strong reference. Delete both names. Show that both are freed
    WITHOUT calling gc.collect().

    QUESTION: what does calling a dead weakref return, and how should code that
    holds weakrefs be written as a result?
    """
    raise NotImplementedError


# TODO 5 -----------------------------------------------------------------------
def part5_finding_the_leak() -> None:
    """Diagnose what is keeping an object alive.

    Create a Tracked object, stash it in a list, a dict, and an attribute of
    another object. Then use gc.get_referrers() to find everything pointing at
    it, and print them.

    This is the actual technique for debugging "why is my memory growing" in a
    real service. It is worth doing once now so you remember it exists.

    QUESTION: name a common real-world cause of an unintended strong reference
    keeping large objects alive in a long-running Python process.
    """
    raise NotImplementedError


if __name__ == "__main__":
    for part in (
        part1_refcounts,
        part2_deterministic_destruction,
        part3_cycle,
        part4_weakref,
        part5_finding_the_leak,
    ):
        print(f"\n=== {part.__name__} ===")
        part()


ANSWERS = """
1. Why does getrefcount report one extra?

2. When exactly did __del__ run in part 2, and what mechanism caused it?

3. In part 3, between the deletion and gc.collect(), what was the state of A
   and B? What does that gap cost a long-running process?

4. What does calling a dead weakref return, and how must holders be written?

5. Name a real-world cause of unintended strong references in a server, and how
   weakref (or an explicit eviction policy) fixes it.

6. Which observations in this file would be FALSE on PyPy, and why?
"""
