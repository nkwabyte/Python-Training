"""Exercise 05.4 — An LRU cache, twice.

Build it the hard way first (dict + doubly linked list), then the easy way
(OrderedDict), then compare. The hard way is the standard interview question
and, more usefully, it is what teaches you why O(1) requires BOTH structures.

Run:  python ex04_lru.py
"""

from __future__ import annotations

import time
from typing import Any

MISSING = object()


# --- Version 1: dict + doubly linked list -------------------------------------
class Node:
    """TODO: key, value, prev, next. Use __slots__ -- Module 08 explains why,
    but a cache node is exactly the case where it pays."""


class LRUCache:
    """Least-recently-used cache with O(1) get and put.

    THE DESIGN PROBLEM: you need two things at once.
      - find a key in O(1)                     -> a dict gives you this
      - know which key is least recent, and
        move any key to "most recent" in O(1)  -> a linked list gives you this
    Neither alone is enough. A dict has no order you can cheaply reorder; a list
    has order but O(n) lookup. The answer is a dict whose VALUES are nodes in a
    linked list, so you can jump to any node in O(1) and unlink it in O(1).

    Sentinel head and tail nodes remove every None check from the unlink and
    insert code. Use them; the version without sentinels has four edge cases and
    all four are bugs.

    TODO 1  __init__(capacity)
    TODO 2  get(key, default) -- a hit moves the node to the front
    TODO 3  put(key, value)   -- inserts at the front, evicts from the back when
                                 over capacity; updating an existing key must
                                 move it, not duplicate it
    TODO 4  __len__, __contains__ (must NOT count as a use), keys() in
            most-recent-first order
    TODO 5  stats(): hits, misses, evictions
    """

    def __init__(self, capacity: int) -> None:
        raise NotImplementedError


# --- Version 2: OrderedDict ---------------------------------------------------
class LRUCacheOrdered:
    """The same thing in about fifteen lines.

    collections.OrderedDict has move_to_end(key) and popitem(last=False), which
    are exactly the two linked-list operations you just wrote by hand -- because
    OrderedDict IS a dict plus a doubly linked list, implemented in C.

    TODO 6  Implement the same interface.
    TODO 7  Then answer:
            - is a plain dict enough in 3.7+, given that it preserves insertion
              order? What operation does it lack?
            - what does functools.lru_cache use internally? (Read its source --
              it is pure Python and short.)
            - when would you NOT want an LRU policy? Name two workloads where
              it performs badly and say what to use instead.
    """

    def __init__(self, capacity: int) -> None:
        raise NotImplementedError


# --- tests --------------------------------------------------------------------
ABSENT = object()   # a probe distinct from the cache's own MISSING sentinel
                    # -- passing MISSING as the default would mean "no default"
                    # and trigger the KeyError branch. Module 02, exercise 4.


def check(cls: type) -> None:
    c = cls(3)
    c.put("a", 1)
    c.put("b", 2)
    c.put("c", 3)
    assert list(c.keys()) == ["c", "b", "a"], list(c.keys())

    assert c.get("a") == 1                       # a becomes most recent
    assert list(c.keys()) == ["a", "c", "b"]

    c.put("d", 4)                                 # evicts b, the oldest
    assert c.get("b", ABSENT) is ABSENT
    assert len(c) == 3

    c.put("a", 99)                                # update, not duplicate
    assert c.get("a") == 99
    assert len(c) == 3

    assert "c" in c
    before = list(c.keys())
    assert "c" in c
    assert list(c.keys()) == before, "__contains__ must not count as a use"

    hits, misses, evictions = c.stats()
    assert evictions >= 1

    c1 = cls(1)
    c1.put("x", 1)
    c1.put("y", 2)
    assert c1.get("x", ABSENT) is ABSENT
    assert c1.get("y") == 2

    print(f"  PASS  {cls.__name__}")


def benchmark() -> None:
    """TODO 8: time 200_000 mixed get/put operations against both versions and
    report the ratio. Predict the winner first, and predict WHY."""
    raise NotImplementedError


if __name__ == "__main__":
    check(LRUCache)
    check(LRUCacheOrdered)
    benchmark()
