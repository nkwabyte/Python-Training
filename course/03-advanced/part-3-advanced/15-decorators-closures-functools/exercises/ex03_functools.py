"""Exercise 15.3 — Cache traps, measured.

Each section demonstrates a real bug. Predict, run, then explain.

Run:  python ex03_functools.py
"""
from __future__ import annotations

import functools
import gc
import sys
import weakref
from typing import Any


# --- trap 1: the equal-but-different keys -------------------------------------
def trap_equal_keys() -> None:
    """PREDICT: how many cache entries after f(1), f(1.0), f(True), f(n=1)?

    The answer is not what the README's simple version implies, and finding out
    why is the exercise. Read functools._make_key -- it has a FAST PATH for a
    single argument of certain types. Which types, and what does that do to the
    grouping?

    Then answer the question that matters: write a function where this
    difference produces a WRONG ANSWER, not just a surprising cache size.
    """
    @functools.cache
    def f(n: Any) -> str:
        return f"{n!r} is {type(n).__name__}"

    print("trap 1")
    for call, label in [((1,), "f(1)"), ((1.0,), "f(1.0)"),
                        ((True,), "f(True)")]:
        print(f"    {label:<10} -> {f(*call)}")
    print(f"    f(n=1)     -> {f(n=1)}")
    print(f"    entries: {f.cache_info().currsize}   {f.cache_info()}")


# --- trap 2: the cached method leak -------------------------------------------
class Heavy:
    """Pretend each instance holds 10 MB."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.payload = bytearray(1024 * 1024)     # 1 MB, to keep it quick

    @functools.cache                               # THE BUG
    def expensive(self, factor: int) -> int:
        return len(self.payload) * factor


def trap_method_leak() -> None:
    """PREDICT: after creating and dropping 20 Heavy objects, how many are
    still alive?

    Then answer:
      - why does the cache keep them? What is in the cache KEY?
      - name three fixes, and say what each costs
      - which fix does the standard library provide for exactly this case?
    """
    print("\ntrap 2")
    refs = []
    for i in range(20):
        obj = Heavy(f"h{i}")
        obj.expensive(2)
        refs.append(weakref.ref(obj))
        del obj

    gc.collect()
    alive = sum(1 for r in refs if r() is not None)
    print(f"    created 20, dropped all references, still alive: {alive}")
    print(f"    cache: {Heavy.expensive.cache_info()}")


# --- trap 3: unhashable arguments ---------------------------------------------
def trap_unhashable() -> None:
    """PREDICT: what happens, and is failing the right behaviour?

    Then implement TWO workarounds and say when each is right:
      (a) convert at the boundary (tuple(items)) -- what does the caller lose?
      (b) a custom key function -- what does that cost, and what can go wrong
          if the key is not injective?
    """
    print("\ntrap 3")

    @functools.cache
    def process(items: Any) -> int:
        return sum(items)

    try:
        process([1, 2, 3])
    except TypeError as exc:
        print(f"    TypeError: {exc}")
    print(f"    tuple works: {process((1, 2, 3))}")


# --- trap 4: caching something impure ------------------------------------------
def trap_impure() -> None:
    """PREDICT: how many lines does the log contain after three calls?

    Then answer: this is obvious when the side effect is a print. Name three
    side effects that are NOT obvious in review, where @cache silently breaks
    the function.
    """
    print("\ntrap 4")
    log: list[str] = []

    @functools.cache
    def save(record_id: int) -> str:
        log.append(f"saved {record_id}")
        return f"receipt-{record_id}"

    for _ in range(3):
        save(1)
    print(f"    called 3 times, log has {len(log)} entries: {log}")


# --- trap 5: maxsize ------------------------------------------------------------
def trap_maxsize() -> None:
    """Measure the memory of an unbounded cache over a high-cardinality key.

    Then answer:
      - what is the right maxsize for a function keyed by user id, in a service
        with 10 million users and 50,000 daily actives?
      - what happens to hit rate at maxsize=128 versus 100_000?
      - when is maxsize=None actually correct?
    """
    print("\ntrap 5")

    @functools.cache
    def by_id(user_id: int) -> str:
        return f"user-{user_id}" * 10

    for i in range(50_000):
        by_id(i)
    size = sys.getsizeof(by_id.__wrapped__)  # not the real answer -- find it
    print(f"    entries: {by_id.cache_info().currsize:,}")
    print("    now measure the ACTUAL memory with tracemalloc, not getsizeof")


if __name__ == "__main__":
    trap_equal_keys()
    trap_method_leak()
    trap_unhashable()
    trap_impure()
    trap_maxsize()
