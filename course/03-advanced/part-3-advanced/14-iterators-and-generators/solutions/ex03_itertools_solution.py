"""Solution 14.3 — Twenty problems, and six hand-built lazy tools."""

from __future__ import annotations

import itertools as it
from collections import defaultdict, deque
from collections.abc import Iterable, Iterator
from typing import Any, TypeVar

T = TypeVar("T")
_MISSING = object()


# --- Part A -------------------------------------------------------------------
def p01_flatten(nested: Iterable[Iterable[T]]) -> list[T]:
    return list(it.chain.from_iterable(nested))
    # sum(nested, []) is O(n^2): it builds a new list per concatenation.


def p02_first_n(iterable: Iterable[T], n: int) -> list[T]:
    return list(it.islice(iterable, n))


def p03_chunks(iterable: Iterable[T], size: int) -> Iterator[tuple[T, ...]]:
    """3.12 has itertools.batched. This is the 3.10-compatible version.

    The iter(callable, sentinel) two-argument form is the trick: it calls the
    callable repeatedly until it returns the sentinel. Combined with islice
    over a shared iterator, it chunks lazily with no index arithmetic.
    """
    iterator = iter(iterable)
    return iter(lambda: tuple(it.islice(iterator, size)), ())


def p04_running_total(nums: Iterable[float]) -> list[float]:
    return list(it.accumulate(nums))


def p05_consecutive_pairs(iterable: Iterable[T]) -> list[tuple[T, T]]:
    return list(it.pairwise(iterable))          # 3.10+


def p06_until_negative(nums: Iterable[float]) -> list[float]:
    return list(it.takewhile(lambda n: n >= 0, nums))
    # takewhile STOPS at the first failure; filter would skip and continue.
    # [1, 2, -1, 3] gives [1, 2] with takewhile and [1, 2, 3] with filter.


def p07_skip_header(lines: Iterable[str]) -> Iterator[str]:
    return it.dropwhile(lambda line: line.startswith("#"), lines)
    # dropwhile stops testing after the first failure, so later '#' lines are
    # kept. filterfalse would remove them all -- a different question.


def p08_group_by_key(rows: list[dict[str, Any]], key: str) -> dict[Any, list[dict]]:
    """Two implementations. SHIP THE SECOND.

    groupby requires sorting first (O(n log n) plus a full materialisation of
    each group), only groups CONSECUTIVE equal keys, and produces sub-iterators
    that are invalidated as soon as you advance to the next group -- so
    list(g) inside the loop is mandatory and easy to forget.

    defaultdict is O(n), needs no sort, works on unsortable keys, and cannot be
    silently wrong. groupby earns its place only when the input is ALREADY
    sorted (a sorted file, a database result with ORDER BY) and you want to
    stream without materialising.
    """
    with_groupby: dict[Any, list[dict]] = {
        k: list(g)                      # list(g) is REQUIRED, not optional
        for k, g in it.groupby(sorted(rows, key=lambda r: r[key]),
                               key=lambda r: r[key])
    }
    with_defaultdict: dict[Any, list[dict]] = defaultdict(list)
    for row in rows:
        with_defaultdict[row[key]].append(row)

    assert with_groupby == dict(with_defaultdict)
    return dict(with_defaultdict)


def p09_round_robin(*iterables: Iterable[T]) -> Iterator[T]:
    """Stops at the shortest, which is what the test wants."""
    return (x for group in zip(*iterables) for x in group)


def p10_all_pairs(items: Iterable[T]) -> list[tuple[T, T]]:
    return list(it.combinations(items, 2))


def p11_cartesian(a: Iterable[T], b: Iterable[T]) -> list[tuple[T, T]]:
    return list(it.product(a, b))


def p12_cycle_n(items: Iterable[T], total: int) -> list[T]:
    return list(it.islice(it.cycle(items), total))
    # cycle() is infinite; islice bounds it. This is the standard shape for
    # "infinite generator + limit" and it is why cycle is safe to use at all.


def p13_zip_padded(a: Iterable[T], b: Iterable[T], fill: Any) -> list[tuple]:
    return list(it.zip_longest(a, b, fillvalue=fill))


def p14_dedupe_consecutive(iterable: Iterable[T]) -> Iterator[T]:
    return (k for k, _ in it.groupby(iterable))
    # Consecutive only, like Unix uniq. set() would remove ALL duplicates and
    # lose the ordering; dict.fromkeys removes all duplicates but keeps order.
    # Three different questions, three different answers.


def p15_select(items: Iterable[T], flags: Iterable[bool]) -> list[T]:
    return list(it.compress(items, flags))


def p16_split_at(iterable: Iterable[T], n: int) -> tuple[list[T], Iterator[T]]:
    """The shared-iterator subtlety.

    islice ADVANCES the underlying iterator, so after materialising the head,
    the SAME iterator object is positioned exactly at item n. Returning it
    gives a lazy tail with no buffering and no second pass.

    Doing this with tee() instead would buffer the entire head in memory for
    the second branch -- correct, and needlessly expensive.
    """
    iterator = iter(iterable)
    head = list(it.islice(iterator, n))
    return head, iterator


def p17_nth(iterable: Iterable[T], n: int, default: Any = None) -> Any:
    return next(it.islice(iterable, n, None), default)


def p18_last(iterable: Iterable[T]) -> T:
    """deque(maxlen=1) keeps only the most recent item: constant memory, one
    pass, and it works on an iterator you cannot index or reverse."""
    d = deque(iterable, maxlen=1)
    if not d:
        raise ValueError("last() of an empty iterable")
    return d[0]


def p19_count_items(iterable: Iterable[Any]) -> int:
    """CONSUMES the iterator. There is no way to count a one-shot iterable
    without exhausting it, which is why len() is not defined for them --
    a silently-consuming len() would be far worse than a TypeError."""
    return sum(1 for _ in iterable)


def p20_interleave_longest(*iterables: Iterable[T]) -> list[T]:
    return [x for group in it.zip_longest(*iterables, fillvalue=_MISSING)
            for x in group if x is not _MISSING]


# --- Part B: six built by hand, lazily ----------------------------------------
def my_chain(*iterables: Iterable[T]) -> Iterator[T]:
    for iterable in iterables:
        yield from iterable


def my_islice(iterable: Iterable[T], stop: int) -> Iterator[T]:
    for i, item in enumerate(iterable):
        if i >= stop:
            return
        yield item


def my_takewhile(predicate: Any, iterable: Iterable[T]) -> Iterator[T]:
    for item in iterable:
        if not predicate(item):
            return
        yield item


def my_pairwise(iterable: Iterable[T]) -> Iterator[tuple[T, T]]:
    iterator = iter(iterable)
    previous = next(iterator, _MISSING)
    if previous is _MISSING:
        return
    for current in iterator:
        yield (previous, current)       # type: ignore[misc]
        previous = current


def my_accumulate(iterable: Iterable[Any], func: Any = None) -> Iterator[Any]:
    import operator
    func = func or operator.add
    iterator = iter(iterable)
    total = next(iterator, _MISSING)
    if total is _MISSING:
        return
    yield total
    for item in iterator:
        total = func(total, item)
        yield total


def my_groupby(iterable: Iterable[T], key: Any = None) -> Iterator[tuple[Any, Iterator[T]]]:
    """Much harder than the others, and the reason is worth understanding.

    THE PROBLEM: the caller may advance to the next group WITHOUT consuming the
    current group's sub-iterator. The outer generator therefore has to be able
    to skip the rest of the current group itself -- which means the two
    generators share mutable state (the current key, the current item, and
    whether the group is exhausted).

    This is why the real itertools.groupby documents that a group is invalid
    once you advance past it, and why `list(g)` inside the loop is mandatory.
    That is not an API wart; it is the only way to avoid buffering an
    arbitrarily large group.
    """
    key = key or (lambda x: x)
    iterator = iter(iterable)
    current_value = next(iterator, _MISSING)
    if current_value is _MISSING:
        return
    current_key = key(current_value)

    while current_value is not _MISSING:
        group_key = current_key
        # a mutable cell shared between this frame and the sub-generator
        state: dict[str, Any] = {"value": current_value, "done": False}

        def group() -> Iterator[T]:
            while not state["done"]:
                yield state["value"]
                nxt = next(iterator, _MISSING)
                if nxt is _MISSING or key(nxt) != group_key:
                    state["done"] = True
                    state["next"] = nxt
                else:
                    state["value"] = nxt

        yield group_key, group()

        # if the caller did not consume the group, skip the rest of it here
        while not state["done"]:
            nxt = next(iterator, _MISSING)
            if nxt is _MISSING or key(nxt) != group_key:
                state["done"] = True
                state["next"] = nxt
        current_value = state.get("next", _MISSING)
        if current_value is not _MISSING:
            current_key = key(current_value)


def verify() -> None:
    assert p01_flatten([[1, 2], [3], [4, 5]]) == [1, 2, 3, 4, 5]
    assert p02_first_n(iter(range(1000)), 3) == [0, 1, 2]
    assert list(p03_chunks([1, 2, 3, 4, 5], 2)) == [(1, 2), (3, 4), (5,)]
    assert p04_running_total([1, 2, 3]) == [1, 3, 6]
    assert p05_consecutive_pairs("abcd") == [("a", "b"), ("b", "c"), ("c", "d")]
    assert p06_until_negative([1, 2, -1, 3]) == [1, 2]
    assert list(p07_skip_header(["#a", "#b", "x", "#c", "y"])) == ["x", "#c", "y"]

    rows = [{"k": "a", "v": 1}, {"k": "b", "v": 2}, {"k": "a", "v": 3}]
    assert len(p08_group_by_key(rows, "k")["a"]) == 2

    assert list(p09_round_robin("abc", "de")) == ["a", "d", "b", "e"]
    assert p10_all_pairs([1, 2, 3]) == [(1, 2), (1, 3), (2, 3)]
    assert len(p11_cartesian([1, 2], "ab")) == 4
    assert p12_cycle_n([1, 2], 5) == [1, 2, 1, 2, 1]
    assert p13_zip_padded([1, 2, 3], "ab", None) == [(1, "a"), (2, "b"), (3, None)]
    assert list(p14_dedupe_consecutive([1, 1, 2, 2, 2, 1])) == [1, 2, 1]
    assert p15_select("abcd", [1, 0, 1, 0]) == ["a", "c"]

    head, tail = p16_split_at(iter(range(10)), 3)
    assert head == [0, 1, 2] and list(tail) == list(range(3, 10))

    assert p17_nth(iter(range(10)), 5) == 5
    assert p17_nth(iter(range(3)), 99, "none") == "none"
    assert p18_last(iter(range(10))) == 9
    assert p19_count_items(iter(range(42))) == 42
    assert p20_interleave_longest("abc", "de") == ["a", "d", "b", "e", "c"]

    # Part B
    assert list(my_chain([1, 2], [3])) == [1, 2, 3]
    assert list(my_islice(it.count(), 4)) == [0, 1, 2, 3]     # infinite input
    assert list(my_takewhile(lambda x: x < 3, it.count())) == [0, 1, 2]
    assert list(my_pairwise("abc")) == [("a", "b"), ("b", "c")]
    assert list(my_pairwise([])) == []
    assert list(my_accumulate([1, 2, 3])) == [1, 3, 6]
    assert list(my_accumulate([])) == []

    grouped = [(k, list(g)) for k, g in my_groupby([1, 1, 2, 2, 2, 3])]
    assert grouped == [(1, [1, 1]), (2, [2, 2, 2]), (3, [3])], grouped

    # the hard case: the caller does NOT consume the groups
    keys_only = [k for k, _ in my_groupby([1, 1, 2, 2, 3])]
    assert keys_only == [1, 2, 3], keys_only

    print("all 20 + 6 checks passed")


if __name__ == "__main__":
    verify()
