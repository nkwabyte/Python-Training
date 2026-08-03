"""Solution 03.4 — The wrong container, fixed and measured."""

from __future__ import annotations

import heapq
import random
import time
from collections import Counter, deque
from collections.abc import Iterable


# --- 1: membership ------------------------------------------------------------
# Pattern: repeated membership test. Before: O(n*m). After: O(n) + O(m) setup.
def filter_blocked_fixed(events: list[str], blocklist: Iterable[str]) -> list[str]:
    blocked = set(blocklist)          # pay O(m) once
    return [e for e in events if e not in blocked]


# --- 2: dedupe, order preserved -----------------------------------------------
# Pattern: dedupe while preserving order. Before: O(n^2). After: O(n).
def unique_preserving_order_fixed(items: list[str]) -> list[str]:
    return list(dict.fromkeys(items))
    # dict preserves insertion order (guaranteed since 3.7) and rejects
    # duplicate keys, so this is dedupe-with-order in one expression. The
    # explicit-set version is equivalent and marginally clearer to some readers:
    #   seen = set(); return [x for x in items if not (x in seen or seen.add(x))]
    # but that idiom relies on set.add returning None, which is cleverness
    # rather than clarity. Prefer dict.fromkeys.


# --- 3: queue -----------------------------------------------------------------
# Pattern: FIFO. Before: pop(0) is O(n) each, O(n^2) total. After: O(1) each.
def process_queue_fixed(tasks: Iterable[str]) -> list[str]:
    queue = deque(tasks)
    done: list[str] = []
    while queue:
        done.append(queue.popleft())   # O(1): deque is a doubly-linked block list
    return done


# --- 4: counting --------------------------------------------------------------
# Two problems in the original: `in counts.keys()` builds nothing extra in
# Python 3 (keys() is a view, so it is still O(1)) but it is noise -- `in
# counts` is the idiom. The real cost is the branch plus two lookups per item.
def word_frequencies_fixed(words: Iterable[str]) -> dict[str, int]:
    return dict(Counter(words))
    # Counter is implemented in C for the common path and is both faster and
    # clearer. If you need a plain dict with a default:
    #   counts = defaultdict(int)
    #   for w in words: counts[w] += 1


# --- 5: lookup by key ---------------------------------------------------------
RECORDS = [{"id": i, "name": f"user{i}"} for i in range(10_000)]


def build_index(records: list[dict[str, object]]) -> dict[object, dict[str, object]]:
    return {r["id"]: r for r in records}


def find_by_id_fixed(index: dict[object, dict[str, object]], target: int):  # type: ignore[no-untyped-def]
    return index.get(target)


# WHEN IS THE INDEX WORTH BUILDING?
#   linear scans: k lookups * O(n)   = k*n
#   indexed:      O(n) build + k*O(1) = n + k
# so indexing wins when  k*n > n + k, i.e. roughly when k > 1 (for large n).
# In practice: build the index if you will do more than ONE lookup, unless n is
# tiny or the data changes between lookups. The interesting case is a lookup
# inside a loop -- that is always worth indexing, and it is the single most
# common O(n^2) in real Python code.


# --- 6: top-k -----------------------------------------------------------------
# Pattern: k largest of n. Before: O(n log n). After: O(n log k).
def top_k_fixed(scores: Iterable[int], k: int) -> list[int]:
    return heapq.nlargest(k, scores)
    # heapq keeps a k-element heap and streams the input, so it also works on
    # an iterator too large to materialise -- sorted() cannot.


# --- benchmark -----------------------------------------------------------------
def timed(label: str, fn, *args) -> float:  # type: ignore[no-untyped-def]
    start = time.perf_counter()
    fn(*args)
    elapsed = time.perf_counter() - start
    print(f"    {label:<34} {elapsed * 1000:9.2f} ms")
    return elapsed


def pair(name: str, before, after, *args) -> None:  # type: ignore[no-untyped-def]
    print(f"\n  {name}")
    b = timed("before", before, *args)
    a = timed("after", after, *args)
    print(f"    {'speedup':<34} {b / a:9.1f}x")


def benchmark() -> None:
    random.seed(0)

    events = [f"e{random.randint(0, 50_000)}" for _ in range(20_000)]
    blocklist = [f"e{i}" for i in range(5_000)]
    pair("1. membership",
         lambda e, b: [x for x in e if x not in b],
         filter_blocked_fixed, events, blocklist)

    items = [f"i{random.randint(0, 2_000)}" for _ in range(10_000)]
    pair("2. dedupe preserving order",
         lambda xs: [x for i, x in enumerate(xs) if x not in xs[:i]][:0] or
                    _naive_unique(xs),
         unique_preserving_order_fixed, items)

    tasks = [f"t{i}" for i in range(50_000)]
    pair("3. queue",
         lambda ts: _naive_queue(list(ts)),
         process_queue_fixed, tasks)

    words = [f"w{random.randint(0, 500)}" for _ in range(200_000)]
    pair("4. counting", _naive_count, word_frequencies_fixed, words)

    index = build_index(RECORDS)
    targets = [random.randint(0, 9_999) for _ in range(2_000)]
    print("\n  5. lookup by id (2000 lookups over 10000 records)")
    b = timed("linear scan", lambda: [_naive_find(RECORDS, t) for t in targets])
    a = timed("dict index (prebuilt)", lambda: [index.get(t) for t in targets])
    print(f"    {'speedup':<34} {b / a:9.1f}x")

    scores = [random.randint(0, 10**6) for _ in range(500_000)]
    pair("6. top-10", lambda s: sorted(s, reverse=True)[:10],
         lambda s: top_k_fixed(s, 10), scores)

    print(
        "\n  Note the shape of each result. Cases 1, 2, 3 and 5 are asymptotic\n"
        "  wins: the ratio GROWS with n, so the number you measured understates\n"
        "  the problem at production scale. Cases 4 and 6 are constant-factor or\n"
        "  log-factor wins: the ratio is roughly stable. Knowing which kind of\n"
        "  win you are looking at tells you whether the fix is urgent."
    )


def _naive_unique(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item not in result:
            result.append(item)
    return result


def _naive_queue(tasks: list[str]) -> list[str]:
    done: list[str] = []
    while tasks:
        done.append(tasks.pop(0))
    return done


def _naive_count(words: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in words:
        if word in counts:
            counts[word] = counts[word] + 1
        else:
            counts[word] = 1
    return counts


def _naive_find(records: list[dict[str, object]], target: int):  # type: ignore[no-untyped-def]
    for record in records:
        if record["id"] == target:
            return record
    return None


def verify() -> None:
    assert filter_blocked_fixed(["a", "b", "c"], ["b"]) == ["a", "c"]
    assert unique_preserving_order_fixed(["b", "a", "b", "c", "a"]) == ["b", "a", "c"]
    assert process_queue_fixed(["1", "2", "3"]) == ["1", "2", "3"]
    assert word_frequencies_fixed(["a", "b", "a"]) == {"a": 2, "b": 1}
    idx = build_index(RECORDS)
    assert find_by_id_fixed(idx, 42)["name"] == "user42"  # type: ignore[index]
    assert find_by_id_fixed(idx, 99_999) is None
    assert top_k_fixed([5, 1, 9, 3], 2) == [9, 5]
    print("all container checks passed")


if __name__ == "__main__":
    verify()
    benchmark()
