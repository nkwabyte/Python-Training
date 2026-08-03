"""Exercise 03.4 — The wrong container.

Six functions, each using a container whose complexity is wrong for the access
pattern. For each:

  1. Name the access pattern (membership? ordered append? lookup by key?
     dedupe? front removal?).
  2. Name the complexity of the current implementation and of the fix.
  3. Rewrite it.
  4. Run benchmark() and record the measured ratio.

Predicting the ratio before measuring is the point. Complexity you can only
recite is complexity you do not yet believe.

Run:  python ex04_container_choice.py
"""

from __future__ import annotations

import random
import time
from collections.abc import Iterable, Iterator


# --- 1: membership in a loop --------------------------------------------------
def filter_blocked(events: list[str], blocklist: list[str]) -> list[str]:
    """Access pattern: ? | current: ? | fixed: ?"""
    return [e for e in events if e not in blocklist]


# --- 2: deduplication ---------------------------------------------------------
def unique_preserving_order(items: list[str]) -> list[str]:
    """Access pattern: ? | current: ? | fixed: ?

    Careful: the naive set() fix loses ordering. Preserve it."""
    result: list[str] = []
    for item in items:
        if item not in result:
            result.append(item)
    return result


# --- 3: queue ------------------------------------------------------------------
def process_queue(tasks: list[str]) -> list[str]:
    """Access pattern: ? | current: ? | fixed: ?

    list.pop(0) is O(n): every remaining element shifts down one slot."""
    done: list[str] = []
    while tasks:
        done.append(tasks.pop(0))
    return done


# --- 4: counting ---------------------------------------------------------------
def word_frequencies(words: list[str]) -> dict[str, int]:
    """Access pattern: ? | current: ? | fixed: ?"""
    counts: dict[str, int] = {}
    for word in words:
        if word in counts.keys():          # two problems in one line
            counts[word] = counts[word] + 1
        else:
            counts[word] = 1
    return counts


# --- 5: lookup by attribute ----------------------------------------------------
RECORDS = [{"id": i, "name": f"user{i}"} for i in range(10_000)]


def find_by_id(records: list[dict[str, object]], target: int) -> dict[str, object] | None:
    """Access pattern: ? | current: ? | fixed: ?

    Note the fix has a SETUP cost. When is it worth paying? Express the answer
    as an inequality involving the number of lookups."""
    for record in records:
        if record["id"] == target:
            return record
    return None


# --- 6: top-k ------------------------------------------------------------------
def top_k(scores: Iterable[int], k: int) -> list[int]:
    """Access pattern: ? | current: ? | fixed: ?

    Sorting everything to take k is O(n log n). There is an O(n log k) answer
    in the standard library."""
    return sorted(scores, reverse=True)[:k]


# --- benchmark -----------------------------------------------------------------
def timed(label: str, fn, *args) -> float:  # type: ignore[no-untyped-def]
    start = time.perf_counter()
    fn(*args)
    elapsed = time.perf_counter() - start
    print(f"  {label:<44} {elapsed * 1000:8.2f} ms")
    return elapsed


def benchmark() -> None:
    """TODO: after fixing each function, add a before/after pair here and
    record the ratio. One is provided as a template."""
    random.seed(0)
    events = [f"e{random.randint(0, 50_000)}" for _ in range(20_000)]
    blocklist = [f"e{i}" for i in range(5_000)]

    print("\n1. membership")
    timed("list blocklist (before)", filter_blocked, events, blocklist)
    # timed("set blocklist  (after)", filter_blocked_fixed, events, blocklist)

    # TODO: 2 through 6


if __name__ == "__main__":
    benchmark()
