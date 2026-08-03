"""Solution 05.4 — An LRU cache, twice."""

from __future__ import annotations

import random
import time
from collections import OrderedDict
from typing import Any

MISSING = object()


class Node:
    __slots__ = ("key", "value", "prev", "next")
    # __slots__ removes the per-instance __dict__. For a cache holding 100k
    # nodes that is roughly a 40 percent memory saving and a measurable speedup
    # on attribute access. This is exactly the case __slots__ is for: many
    # instances, fixed attribute set. (Module 08.)

    def __init__(self, key: Any = None, value: Any = None) -> None:
        self.key = key
        self.value = value
        self.prev: Node | None = None
        self.next: Node | None = None


class LRUCache:
    """dict for O(1) lookup + doubly linked list for O(1) reordering.

    Neither structure alone suffices:
      - a dict finds any key in O(1) but has no order you can cheaply reorder
      - a linked list reorders in O(1) but finds a key in O(n)
    Storing NODES as the dict's values gives you both: jump straight to the
    node, then unlink and relink it in constant time.

    The sentinel head and tail nodes are not decoration. Without them, unlink
    and insert each need to handle "is this the first node", "is this the last
    node", "is this the only node", and "is the list empty" -- four edge cases,
    and in every hand-rolled version I have reviewed, at least one is wrong.
    With sentinels, every real node always has a prev and a next, and the code
    has no branches at all.
    """

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self.capacity = capacity
        self._map: dict[Any, Node] = {}
        self._head = Node()          # sentinel: most-recent side
        self._tail = Node()          # sentinel: least-recent side
        self._head.next = self._tail
        self._tail.prev = self._head
        self._hits = self._misses = self._evictions = 0

    # -- linked list primitives (no edge cases, thanks to the sentinels) ------
    def _unlink(self, node: Node) -> None:
        node.prev.next = node.next    # type: ignore[union-attr]
        node.next.prev = node.prev    # type: ignore[union-attr]

    def _push_front(self, node: Node) -> None:
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node   # type: ignore[union-attr]
        self._head.next = node

    # -- public API -----------------------------------------------------------
    def get(self, key: Any, default: Any = MISSING) -> Any:
        node = self._map.get(key)
        if node is None:
            self._misses += 1
            if default is MISSING:
                raise KeyError(key)
            return default
        self._hits += 1
        self._unlink(node)
        self._push_front(node)        # a hit makes it the most recent
        return node.value

    def put(self, key: Any, value: Any) -> None:
        node = self._map.get(key)
        if node is not None:
            node.value = value        # UPDATE: move, do not duplicate
            self._unlink(node)
            self._push_front(node)
            return

        if len(self._map) >= self.capacity:
            victim = self._tail.prev  # the least recently used
            assert victim is not None and victim is not self._head
            self._unlink(victim)
            del self._map[victim.key]
            self._evictions += 1

        node = Node(key, value)
        self._map[key] = node
        self._push_front(node)

    def __len__(self) -> int:
        return len(self._map)

    def __contains__(self, key: Any) -> bool:
        return key in self._map       # deliberately does NOT count as a use
                                       # and does NOT reorder

    def keys(self) -> list[Any]:
        out, node = [], self._head.next
        while node is not self._tail:
            assert node is not None
            out.append(node.key)
            node = node.next
        return out

    def stats(self) -> tuple[int, int, int]:
        return (self._hits, self._misses, self._evictions)


class LRUCacheOrdered:
    """The same behaviour in a fraction of the code.

    OrderedDict.move_to_end and popitem(last=False) ARE the two linked-list
    operations above -- OrderedDict is literally a dict plus a doubly linked
    list, implemented in C.

    IS A PLAIN DICT ENOUGH IN 3.7+? Almost. A plain dict preserves insertion
    order and gives you eviction of the oldest via next(iter(d)), but it has no
    MOVE-TO-END. You can emulate it with `d[k] = d.pop(k)`, which is O(1) and
    works fine -- so yes, a plain dict is sufficient, and functools.lru_cache's
    real implementation uses a dict plus its own linked list anyway. What you
    lose is the intent being obvious.

    WHAT DOES functools.lru_cache USE? A dict mapping key -> a list-based
    circular doubly linked list node ([prev, next, key, result]), a lock for
    thread safety, and a sentinel-based root node. It is pure Python in
    Lib/functools.py, about 100 lines, and worth reading -- it is the same
    design you just wrote, plus thread safety and a fast path for the
    unbounded case.

    WHEN IS LRU THE WRONG POLICY?
      1. A FULL SCAN over data larger than the cache. Reading a 10 GB table
         through a 1 GB LRU cache evicts everything before it is ever reused --
         the hit rate is zero and you pay the bookkeeping for nothing. Databases
         solve this with scan-resistant policies (LRU-K, ARC, or simply marking
         scan pages as use-once).
      2. WORKLOADS WITH STRONG FREQUENCY SKEW. If one key is requested 1000
         times an hour and a thousand others once each, LRU will happily evict
         the hot key because it was not touched in the last few seconds. LFU
         (least frequently used), or a hybrid like TinyLFU/W-TinyLFU, keeps the
         hot key.
      3. Data with a natural expiry (session tokens, quotes, weather). TTL is
         the correct policy; LRU can serve stale data indefinitely as long as
         it is popular.
    """

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self.capacity = capacity
        self._data: OrderedDict[Any, Any] = OrderedDict()
        self._hits = self._misses = self._evictions = 0

    def get(self, key: Any, default: Any = MISSING) -> Any:
        if key not in self._data:
            self._misses += 1
            if default is MISSING:
                raise KeyError(key)
            return default
        self._hits += 1
        self._data.move_to_end(key, last=False)
        return self._data[key]

    def put(self, key: Any, value: Any) -> None:
        if key in self._data:
            self._data.move_to_end(key, last=False)
            self._data[key] = value
            return
        if len(self._data) >= self.capacity:
            self._data.popitem(last=True)     # drop the least recent
            self._evictions += 1
        self._data[key] = value
        self._data.move_to_end(key, last=False)

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key: Any) -> bool:
        return key in self._data

    def keys(self) -> list[Any]:
        return list(self._data)

    def stats(self) -> tuple[int, int, int]:
        return (self._hits, self._misses, self._evictions)


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

    assert c.get("a") == 1
    assert list(c.keys()) == ["a", "c", "b"], list(c.keys())

    c.put("d", 4)
    assert c.get("b", ABSENT) is ABSENT
    assert len(c) == 3

    c.put("a", 99)
    assert c.get("a") == 99
    assert len(c) == 3

    assert "c" in c
    before = list(c.keys())
    assert "c" in c
    assert list(c.keys()) == before, "__contains__ must not count as a use"

    _hits, _misses, evictions = c.stats()
    assert evictions >= 1

    c1 = cls(1)
    c1.put("x", 1)
    c1.put("y", 2)
    assert c1.get("x", ABSENT) is ABSENT
    assert c1.get("y") == 2

    print(f"  PASS  {cls.__name__}")


def benchmark(n: int = 200_000) -> None:
    """PREDICTION: OrderedDict wins, because its move_to_end and popitem run in
    C while the hand-rolled version does four Python-level attribute
    assignments per reorder. The hand-rolled version teaches the algorithm; the
    C one is what you ship.

    The general lesson, which returns in Module 23: a better algorithm beats a
    faster language, but at equal algorithms the C implementation wins by a
    constant factor of roughly 2-4x. Both facts matter.
    """
    rng = random.Random(1)
    ops = [(rng.randrange(5_000), rng.random() < 0.7) for _ in range(n)]

    print(f"\n{n:,} mixed operations, capacity 1000")
    results = {}
    for cls in (LRUCache, LRUCacheOrdered):
        cache = cls(1000)
        start = time.perf_counter()
        for key, is_get in ops:
            if is_get:
                cache.get(key, None)
            else:
                cache.put(key, key)
        elapsed = time.perf_counter() - start
        results[cls.__name__] = elapsed
        print(f"  {cls.__name__:<20} {elapsed * 1000:8.1f} ms")

    slow, fast = max(results.values()), min(results.values())
    winner = min(results, key=lambda k: results[k])
    print(f"  {'winner':<20} {winner} by {slow / fast:.1f}x")


if __name__ == "__main__":
    check(LRUCache)
    check(LRUCacheOrdered)
    benchmark()
