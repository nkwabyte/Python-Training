"""Exercise 04.5 — Six loops to rewrite.

Each one works. Each one is written the way someone writes Python when they are
still writing C or Java in it. Rewrite each idiomatically, keeping the
behaviour identical, and note in a comment what the rewrite eliminated.

Run:  python ex05_control_flow.py
"""

from __future__ import annotations

from collections.abc import Iterable


# --- 1: index arithmetic ------------------------------------------------------
def with_positions(names: list[str]) -> list[str]:
    """ELIMINATE: manual index tracking."""
    result = []
    i = 0
    while i < len(names):
        result.append(f"{i + 1}. {names[i]}")
        i += 1
    return result


# --- 2: parallel indexing -----------------------------------------------------
def pair_up(names: list[str], scores: list[int]) -> list[str]:
    """ELIMINATE: indexing two lists in lockstep.
    BONUS: make mismatched lengths an ERROR rather than silent truncation."""
    result = []
    for i in range(len(names)):
        result.append(f"{names[i]}={scores[i]}")
    return result


# --- 3: the flag --------------------------------------------------------------
def has_admin(users: list[dict[str, object]]) -> bool:
    """ELIMINATE: the found flag. Two idiomatic rewrites exist -- one uses
    for/else, the other uses a builtin. Write both, and say which you prefer."""
    found = False
    for user in users:
        if user.get("role") == "admin":
            found = True
            break
    return found


# --- 4: accumulate and branch -------------------------------------------------
def split_valid(records: list[dict[str, object]]) -> tuple[list, list]:  # type: ignore[type-arg]
    """ELIMINATE: two appends in a manual loop.
    Careful: a single comprehension iterates twice. Is that acceptable here?
    When is it not?"""
    valid = []
    invalid = []
    for record in records:
        if record.get("email"):
            valid.append(record)
        else:
            invalid.append(record)
    return valid, invalid


# --- 5: nested loop with a sentinel -------------------------------------------
def find_pair(numbers: list[int], target: int) -> tuple[int, int] | None:
    """ELIMINATE: the nested break dance.
    Two rewrites: one using itertools, one using a dict for an O(n) algorithm.
    The second is a genuinely better algorithm, not just tidier code -- say what
    changed in the complexity."""
    result = None
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] + numbers[j] == target:
                result = (numbers[i], numbers[j])
                break
        if result is not None:
            break
    return result


# --- 6: building a string -----------------------------------------------------
def render_csv(rows: list[list[str]]) -> str:
    """ELIMINATE: string concatenation in a loop, and the trailing-separator
    dance."""
    out = ""
    for row in rows:
        line = ""
        for i, cell in enumerate(row):
            line += cell
            if i < len(row) - 1:
                line += ","
        out += line + "\n"
    return out


# --- tests --------------------------------------------------------------------
def test_all() -> None:
    assert with_positions(["a", "b"]) == ["1. a", "2. b"]
    assert pair_up(["a", "b"], [1, 2]) == ["a=1", "b=2"]
    assert has_admin([{"role": "user"}, {"role": "admin"}]) is True
    assert has_admin([{"role": "user"}]) is False
    valid, invalid = split_valid([{"email": "a@b"}, {}, {"email": ""}])
    assert len(valid) == 1 and len(invalid) == 2
    assert find_pair([1, 2, 3, 4], 7) == (3, 4)
    assert find_pair([1, 2], 99) is None
    assert render_csv([["a", "b"], ["c", "d"]]) == "a,b\nc,d\n"
    print("  PASS  behaviour preserved")


def test_pair_up_is_strict() -> None:
    try:
        pair_up(["a", "b", "c"], [1, 2])
    except ValueError:
        print("  PASS  pair_up rejects mismatched lengths")
        return
    print("  TODO  pair_up still truncates silently")


if __name__ == "__main__":
    test_all()
    test_pair_up_is_strict()
