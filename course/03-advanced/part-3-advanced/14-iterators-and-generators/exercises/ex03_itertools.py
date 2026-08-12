"""Exercise 14.3 — Twenty problems with one-line answers.

Part A: solve each with itertools (or a builtin). One line each.
Part B: implement six of them yourself, lazily, without itertools.

Run:  python ex03_itertools.py
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Any, TypeVar

T = TypeVar("T")


# --- Part A: one line each ----------------------------------------------------
def p01_flatten(nested: Iterable[Iterable[T]]) -> list[T]:
    """[[1,2],[3],[4,5]] -> [1,2,3,4,5]. NOT sum(nested, [])."""
    raise NotImplementedError


def p02_first_n(it: Iterable[T], n: int) -> list[T]:
    """First n items of a possibly-infinite iterable."""
    raise NotImplementedError


def p03_chunks(it: Iterable[T], size: int) -> Iterator[tuple[T, ...]]:
    """[1,2,3,4,5], 2 -> (1,2), (3,4), (5,). Lazily.
    3.12 has itertools.batched. Write it for 3.10 too."""
    raise NotImplementedError


def p04_running_total(nums: Iterable[float]) -> list[float]:
    """[1,2,3] -> [1,3,6]"""
    raise NotImplementedError


def p05_consecutive_pairs(it: Iterable[T]) -> list[tuple[T, T]]:
    """'abcd' -> [('a','b'),('b','c'),('c','d')]"""
    raise NotImplementedError


def p06_until_negative(nums: Iterable[float]) -> list[float]:
    """[1,2,-1,3] -> [1,2]  (stop at the first failure, do not filter)"""
    raise NotImplementedError


def p07_skip_header(lines: Iterable[str]) -> Iterator[str]:
    """Drop leading lines starting with '#', keep everything after -- including
    later '#' lines."""
    raise NotImplementedError


def p08_group_by_key(rows: list[dict[str, Any]], key: str) -> dict[Any, list[dict]]:
    """Group rows by a key. Careful: groupby needs sorted input. Show BOTH the
    groupby version and the defaultdict version, and say which you would ship
    and why."""
    raise NotImplementedError


def p09_round_robin(*its: Iterable[T]) -> Iterator[T]:
    """'abc', 'de' -> a, d, b, e, c"""
    raise NotImplementedError


def p10_all_pairs(items: Iterable[T]) -> list[tuple[T, T]]:
    """Every unordered pair, no repeats. [1,2,3] -> (1,2),(1,3),(2,3)"""
    raise NotImplementedError


def p11_cartesian(a: Iterable[T], b: Iterable[T]) -> list[tuple[T, T]]:
    """Every combination from two iterables."""
    raise NotImplementedError


def p12_cycle_n(items: Iterable[T], total: int) -> list[T]:
    """Repeat the sequence until `total` items have been produced."""
    raise NotImplementedError


def p13_zip_padded(a: Iterable[T], b: Iterable[T], fill: Any) -> list[tuple]:
    """Zip without truncating the longer one."""
    raise NotImplementedError


def p14_dedupe_consecutive(it: Iterable[T]) -> Iterator[T]:
    """[1,1,2,2,2,1] -> 1,2,1  (Unix uniq, NOT set())"""
    raise NotImplementedError


def p15_select(items: Iterable[T], flags: Iterable[bool]) -> list[T]:
    """Keep items whose corresponding flag is True."""
    raise NotImplementedError


def p16_split_at(it: Iterable[T], n: int) -> tuple[list[T], Iterator[T]]:
    """First n as a list, the REST as a lazy iterator. Careful: consuming the
    first part must not consume the rest."""
    raise NotImplementedError


def p17_nth(it: Iterable[T], n: int, default: Any = None) -> Any:
    """The nth item of an iterator, without materialising it."""
    raise NotImplementedError


def p18_last(it: Iterable[T]) -> T:
    """The final item of an iterator, in constant memory."""
    raise NotImplementedError


def p19_count_items(it: Iterable[Any]) -> int:
    """len() for an iterator. Note what this costs."""
    raise NotImplementedError


def p20_interleave_longest(*its: Iterable[T]) -> list[T]:
    """Round-robin, but continue with the longer iterables after the short ones
    are exhausted."""
    raise NotImplementedError


# --- Part B -------------------------------------------------------------------
# Implement these SIX yourself, lazily, with no itertools import:
#   my_chain, my_islice, my_takewhile, my_pairwise, my_accumulate, my_groupby
#
# Constraints: each must be a generator, must not materialise its input, and
# must work on an infinite iterable where that makes sense.
#
# my_groupby is much harder than the others. Work out why before starting:
# what must happen to the previous group when the caller advances to the next
# one WITHOUT having consumed it?


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

    assert list(p09_round_robin("abc", "de")) == ["a", "d", "b", "e", "c"]
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

    print("all 20 checks passed")


if __name__ == "__main__":
    verify()
