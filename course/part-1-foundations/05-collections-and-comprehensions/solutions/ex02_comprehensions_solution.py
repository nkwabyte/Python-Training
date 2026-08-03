"""Solution 05.2 — Comprehensions in both directions."""

from __future__ import annotations

import itertools
from collections import defaultdict
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


# --- Part A -------------------------------------------------------------------
def a01_uppercase(words: list[str]) -> list[str]:
    return [w.upper() for w in words]


def a02_positives(nums: list[int]) -> list[int]:
    return [n for n in nums if n > 0]                    # FILTER: if after for


def a03_clamp(nums: list[int]) -> list[int]:
    return [n if n > 0 else 0 for n in nums]             # TRANSFORM: before for


def a04_lengths(words: list[str]) -> dict[str, int]:
    return {w: len(w) for w in words}


def a05_initials(words: list[str]) -> set[str]:
    return {w[0].lower() for w in words}


def a06_flatten(matrix: list[list[int]]) -> list[int]:
    return [cell for row in matrix for cell in row]
    # The for clauses appear in the SAME ORDER as the nested loops they replace:
    #   for row in matrix:      ->  for row in matrix
    #       for cell in row:    ->  for cell in row
    # Everyone reverses this once. Read left to right, outermost first.


def a07_transpose(matrix: list[list[int]]) -> list[list[int]]:
    return [list(col) for col in zip(*matrix, strict=True)]
    # The one-word answer is zip(*matrix). SHIP THIS ONE. The comprehension
    # version below is correct but reimplements a builtin:
    #   [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]
    # zip(*m) is faster, shorter, and cannot have an index bug. The lesson:
    # before writing a comprehension over range(len(...)), check for a builtin.


def a08_names_of_active(people: list[dict[str, Any]]) -> list[str]:
    return [p["name"] for p in people if p["active"]]


def a09_by_name(people: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {p["name"]: p for p in people}
    # This is "build an index", the fix for Module 03's exercise 5. Note it
    # silently drops duplicates -- last wins. If names are not unique this is a
    # bug, and a defaultdict(list) is what you actually wanted.


def a10_high_scorers_by_dept(people: list[dict[str, Any]]) -> dict[str, list[str]]:
    """NOT a single comprehension. This is a GROUPING, and grouping needs
    accumulation into an existing bucket, which a comprehension cannot express
    without either a nested comprehension that re-scans the input per key
    (O(n*k)) or a walrus-operator trick that is unreadable.

    defaultdict(list) is the right tool and the loop is three lines."""
    out: dict[str, list[str]] = defaultdict(list)
    for p in people:
        if p["score"] >= 88:
            out[p["dept"]].append(p["name"])
    return dict(out)     # convert back, so callers do not inherit the
                         # read-inserts-a-key behaviour


def a11_pairs(xs: list[int]) -> list[tuple[int, int]]:
    return list(itertools.combinations(xs, 2))
    # The comprehension version is:
    #   [(x, y) for i, x in enumerate(xs) for y in xs[i+1:]]
    # combinations is clearer, and it is lazy, so it works on large inputs.


def a12_word_positions(words: list[str]) -> dict[str, int]:
    return {w.lower(): i for i, w in enumerate(words)}


def a13_filter_and_transform(nums: list[int]) -> list[int]:
    return [n * n for n in nums if n > 0 if n % 2 == 0]
    # Two ifs are ANDed. `if n > 0 and n % 2 == 0` is equally correct; use
    # whichever reads better. Separate ifs tend to read better when the
    # conditions are conceptually independent.


def a14_invert(mapping: dict[str, int]) -> dict[int, str]:
    return {v: k for k, v in mapping.items()}
    # IF TWO KEYS SHARE A VALUE, the later one wins and the earlier is silently
    # lost. Acceptable ONLY when values are known unique. If they are not, you
    # want dict[int, list[str]] built with a defaultdict -- and the fact that
    # the one-liner hides this decision is exactly why it deserves a comment.


def a15_running_total(nums: list[int]) -> list[int]:
    return list(itertools.accumulate(nums))
    # CANNOT be a plain comprehension: each element depends on the previous, and
    # comprehensions have no state between iterations.
    #
    # The walrus "solution" exists:
    #     total = 0
    #     [total := total + n for n in nums]
    # and it is a bad idea. It mutates an enclosing variable as a side effect of
    # building a list, so the comprehension is no longer a description of a
    # result -- it is a loop wearing a disguise, and it leaves `total` modified
    # afterwards. accumulate() says what is happening.


# --- Part B: back to loops ----------------------------------------------------
def b01_side_effects(words: list[str]) -> None:
    """WHY WRONG: it builds a list of len(words) Nones and immediately discards
    it, allocating memory to accomplish nothing. More importantly it lies about
    intent: a comprehension says "I am producing a value", and this produces
    nothing. A reader has to look twice to see that the result is unused."""
    for w in words:
        print(w)


def b02_too_much(people: list[dict[str, Any]]) -> list[str]:
    """WHY WRONG: four clauses plus a conditional expression inside a range().
    Nobody can read it, and nobody can debug it -- you cannot set a breakpoint
    inside a comprehension or print an intermediate value.

    The rule of thumb: two `for`s or two `if`s is the ceiling. Beyond that, the
    comprehension has stopped describing a result and started encoding a
    procedure."""
    out: list[str] = []
    for p in people:
        if not p["active"] or p["score"] <= 80:
            continue
        if p["name"][0] in "XYZ":
            continue
        copies = 1 if p["dept"] == "eng" else 2
        label = f"{p['name']} ({p['dept']})"
        out.extend([label] * copies)
    return out


def b03_hidden_work(paths: list[str]) -> list[str]:
    """WHY WRONG: expensive() is called THREE TIMES PER ELEMENT -- once in each
    condition and once in the output expression. On a disk or network call that
    is a 3x cost increase hidden in code that looks efficient.

    Two fixes. The loop below is the clearest. The walrus version is defensible
    here because it removes redundant work rather than adding side effects:

        [r.upper() for p in paths if (r := expensive(p)) is not None and len(r) > 3]

    That is the legitimate use case the walrus was designed for."""
    out: list[str] = []
    for p in paths:
        result = expensive(p)
        if result is not None and len(result) > 3:
            out.append(result.upper())
    return out


def expensive(path: str) -> str | None:
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
    print("  PASS  part A")


def test_part_b() -> None:
    assert b02_too_much(PEOPLE) == ["Ada (eng)", "Cy (eng)", "Di (ops)", "Di (ops)"]
    assert b03_hidden_work(["abcd", "ab", ""]) == ["ABCD"]
    print("  PASS  part B")


if __name__ == "__main__":
    test_part_a()
    test_part_b()
