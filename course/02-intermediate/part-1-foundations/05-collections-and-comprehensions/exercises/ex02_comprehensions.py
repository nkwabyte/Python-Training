"""Exercise 05.2 — Comprehensions in both directions.

Part A: fifteen loops that should be comprehensions.
Part B: three comprehensions that should NOT be comprehensions. Convert them
back and say why.

Knowing when NOT to use one is the part that separates readable code from
clever code.

Run:  python ex02_comprehensions.py
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Any

WORDS = ["apple", "Banana", "cherry", "date", "Elderberry", "fig"]
NUMS = [3, -1, 4, -1, 5, 9, -2, 6]
MATRIX = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
PEOPLE = [
    {"name": "Ada", "dept": "eng", "score": 95, "active": True},
    {"name": "Bo", "dept": "ops", "score": 82, "active": False},
    {"name": "Cy", "dept": "eng", "score": 88, "active": True},
    {"name": "Di", "dept": "ops", "score": 91, "active": True},
]


# --- Part A: convert each of these to a comprehension -------------------------
def a01_uppercase(words: list[str]) -> list[str]:
    out = []
    for w in words:
        out.append(w.upper())
    return out


def a02_positives(nums: list[int]) -> list[int]:
    out = []
    for n in nums:
        if n > 0:
            out.append(n)
    return out


def a03_clamp(nums: list[int]) -> list[int]:
    out = []
    for n in nums:
        out.append(n if n > 0 else 0)
    return out


def a04_lengths(words: list[str]) -> dict[str, int]:
    out = {}
    for w in words:
        out[w] = len(w)
    return out


def a05_initials(words: list[str]) -> set[str]:
    out = set()
    for w in words:
        out.add(w[0].lower())
    return out


def a06_flatten(matrix: list[list[int]]) -> list[int]:
    out = []
    for row in matrix:
        for cell in row:
            out.append(cell)
    return out


def a07_transpose(matrix: list[list[int]]) -> list[list[int]]:
    out = []
    for j in range(len(matrix[0])):
        row = []
        for i in range(len(matrix)):
            row.append(matrix[i][j])
        out.append(row)
    return out
    # Note: there is a one-word answer using a builtin. Find it, then also
    # write the comprehension version, and say which you would ship.


def a08_names_of_active(people: list[dict[str, Any]]) -> list[str]:
    out = []
    for p in people:
        if p["active"]:
            out.append(p["name"])
    return out


def a09_by_name(people: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out = {}
    for p in people:
        out[p["name"]] = p
    return out


def a10_high_scorers_by_dept(people: list[dict[str, Any]]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for p in people:
        if p["score"] >= 88:
            if p["dept"] not in out:
                out[p["dept"]] = []
            out[p["dept"]].append(p["name"])
    return out
    # This one should NOT become a single comprehension. Which tool fits?


def a11_pairs(xs: list[int]) -> list[tuple[int, int]]:
    out = []
    for i, x in enumerate(xs):
        for y in xs[i + 1:]:
            out.append((x, y))
    return out


def a12_word_positions(words: list[str]) -> dict[str, int]:
    out = {}
    for i, w in enumerate(words):
        out[w.lower()] = i
    return out


def a13_filter_and_transform(nums: list[int]) -> list[int]:
    out = []
    for n in nums:
        if n > 0:
            if n % 2 == 0:
                out.append(n * n)
    return out


def a14_invert(mapping: dict[str, int]) -> dict[int, str]:
    out = {}
    for k, v in mapping.items():
        out[v] = k
    return out
    # What happens if two keys share a value? Is that acceptable? Say so.


def a15_running_total(nums: list[int]) -> list[int]:
    out = []
    total = 0
    for n in nums:
        total += n
        out.append(total)
    return out
    # TRAP: this one CANNOT be a plain comprehension, because each result
    # depends on the previous. Name the itertools function that does it, and
    # say why the walrus-operator "solution" is a bad idea.


# --- Part B: convert these BACK to loops, and say why -------------------------
def b01_side_effects(words: list[str]) -> None:
    """WHY IS THIS WRONG?"""
    [print(w) for w in words]  # noqa: C416


def b02_too_much(people: list[dict[str, Any]]) -> list[str]:
    """WHY IS THIS WRONG?"""
    return [
        f"{p['name']} ({p['dept']})"
        for p in people
        if p["active"]
        if p["score"] > 80
        for _ in range(1 if p["dept"] == "eng" else 2)
        if p["name"][0] not in "XYZ"
    ]


def b03_hidden_work(paths: list[str]) -> list[str]:
    """WHY IS THIS WRONG?  (hint: how many times is the expensive call made?)"""
    return [
        expensive(p).upper()
        for p in paths
        if expensive(p) is not None
        if len(expensive(p)) > 3
    ]


def expensive(path: str) -> str | None:
    """Pretend this hits the disk."""
    return path if path else None


# --- tests --------------------------------------------------------------------
def test_part_a() -> None:
    assert a01_uppercase(["a"]) == ["A"]
    assert a02_positives(NUMS) == [3, 4, 5, 9, 6]
    assert a03_clamp([-1, 2]) == [0, 2]
    assert a04_lengths(["ab"]) == {"ab": 2}
    assert a05_initials(["Apple", "avocado"]) == {"a"}
    assert a06_flatten(MATRIX) == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert a07_transpose(MATRIX) == [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    assert a08_names_of_active(PEOPLE) == ["Ada", "Cy", "Di"]
    assert set(a09_by_name(PEOPLE)) == {"Ada", "Bo", "Cy", "Di"}
    assert a10_high_scorers_by_dept(PEOPLE) == {"eng": ["Ada", "Cy"], "ops": ["Di"]}
    assert a11_pairs([1, 2, 3]) == [(1, 2), (1, 3), (2, 3)]
    assert a12_word_positions(["A", "b"]) == {"a": 0, "b": 1}
    assert a13_filter_and_transform(NUMS) == [16, 36]
    assert a14_invert({"a": 1, "b": 2}) == {1: "a", 2: "b"}
    assert a15_running_total([1, 2, 3]) == [1, 3, 6]
    print("  PASS  part A behaviour preserved")


if __name__ == "__main__":
    test_part_a()
    print("\nNow answer the WHY questions in Part B, in comments.")
