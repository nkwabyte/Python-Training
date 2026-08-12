"""Solution 04.5 — Six loops, rewritten."""

from __future__ import annotations

from itertools import combinations


# --- 1: enumerate replaces index arithmetic -----------------------------------
def with_positions(names: list[str]) -> list[str]:
    # ELIMINATED: a counter variable, a manual bounds check, and an off-by-one
    # opportunity. enumerate's `start` argument removes the +1 as well.
    return [f"{i}. {name}" for i, name in enumerate(names, start=1)]


# --- 2: zip replaces parallel indexing ----------------------------------------
def pair_up(names: list[str], scores: list[int]) -> list[str]:
    # ELIMINATED: range(len(...)), double subscripting, and -- with strict=True
    # -- the silent truncation that hides data bugs. Without strict, a names
    # list one element longer than scores produces a shorter result and no
    # complaint, which is how partial data reaches a report.
    return [f"{name}={score}" for name, score in zip(names, scores, strict=True)]


# --- 3: any() replaces the flag -----------------------------------------------
def has_admin(users: list[dict[str, object]]) -> bool:
    # ELIMINATED: the flag variable and the break.
    # any() short-circuits on the first True, so this is not less efficient
    # than the manual loop -- it stops at the same element.
    return any(user.get("role") == "admin" for user in users)


def has_admin_for_else(users: list[dict[str, object]]) -> bool:
    """The for/else version, for comparison."""
    for user in users:
        if user.get("role") == "admin":
            return True
    return False
    # PREFERENCE: any(). It states the intent ("is there one?") rather than
    # describing a search. for/else earns its place when you need to DO
    # something with the found item AND have a distinct not-found branch --
    # then the early return version above is usually still clearer.


# --- 4: partition ---------------------------------------------------------------
def split_valid(records: list[dict[str, object]]) -> tuple[list, list]:  # type: ignore[type-arg]
    """Two comprehensions iterate twice. Acceptable here?

    Yes, when the input is a materialised list, the predicate is cheap, and
    clarity matters more than one extra pass. Two comprehensions are the
    clearest possible statement of "these, and those".

    NOT acceptable when:
      - the input is a GENERATOR or a file handle. The second pass gets nothing,
        because the iterator is exhausted. This is a silent, nasty bug.
      - the predicate is expensive (a network call, a regex over long text) --
        you would pay for it twice.
      - the input is large enough that two passes hurt cache behaviour.
    In those cases, the single explicit loop below is correct.
    """
    valid = [r for r in records if r.get("email")]
    invalid = [r for r in records if not r.get("email")]
    return valid, invalid


def split_valid_single_pass(records: list[dict[str, object]]) -> tuple[list, list]:  # type: ignore[type-arg]
    """One pass. Use this shape when the input is an iterator."""
    valid: list[dict[str, object]] = []
    invalid: list[dict[str, object]] = []
    for record in records:
        (valid if record.get("email") else invalid).append(record)
    return valid, invalid


# --- 5: nested break -> itertools, then a better algorithm --------------------
def find_pair_itertools(numbers: list[int], target: int) -> tuple[int, int] | None:
    """ELIMINATED: the nested loop, the result sentinel, and the double break.
    Still O(n^2) -- this is a readability fix, not an algorithmic one."""
    return next(
        ((a, b) for a, b in combinations(numbers, 2) if a + b == target),
        None,
    )


def find_pair(numbers: list[int], target: int) -> tuple[int, int] | None:
    """The real fix: O(n^2) -> O(n).

    For each element, the partner we need is fully determined (target - x), so
    instead of searching for it we ask a set whether we have already seen it.
    One pass, O(1) membership, O(n) extra space.

    This is the classic time-space trade and the single most useful pattern in
    interview-style problems: replace a search with a lookup. Module 32 in the
    C++ course calls it the same thing.

    Note it returns the pair in first-seen order, which differs from the nested
    loop's (i, j) order for some inputs. Check whether callers care before
    swapping the implementation -- an "equivalent" rewrite that changes result
    ordering is a classic silent regression.
    """
    seen: set[int] = set()
    for x in numbers:
        if (partner := target - x) in seen:
            return (partner, x)
        seen.add(x)
    return None


# --- 6: join replaces concatenation -------------------------------------------
def render_csv(rows: list[list[str]]) -> str:
    # ELIMINATED: quadratic string building, the enumerate/length dance for the
    # trailing comma, and the trailing-newline special case. Two joins express
    # "cells joined by commas, rows joined by newlines" directly.
    return "".join(",".join(row) + "\n" for row in rows)
    # Note: for real CSV, use the csv module (Module 19). It handles quoting,
    # embedded commas, embedded newlines, and dialects. Hand-rolled CSV writing
    # is correct for exactly as long as no field contains a comma.


# --- tests --------------------------------------------------------------------
def test_all() -> None:
    assert with_positions(["a", "b"]) == ["1. a", "2. b"]
    assert pair_up(["a", "b"], [1, 2]) == ["a=1", "b=2"]
    assert has_admin([{"role": "user"}, {"role": "admin"}]) is True
    assert has_admin([{"role": "user"}]) is False
    assert has_admin_for_else([{"role": "admin"}]) is True

    valid, invalid = split_valid([{"email": "a@b"}, {}, {"email": ""}])
    assert len(valid) == 1 and len(invalid) == 2
    v2, i2 = split_valid_single_pass([{"email": "a@b"}, {}, {"email": ""}])
    assert (v2, i2) == (valid, invalid)

    assert find_pair([1, 2, 3, 4], 7) == (3, 4)
    assert find_pair([1, 2], 99) is None
    assert find_pair_itertools([1, 2, 3, 4], 7) == (3, 4)

    assert render_csv([["a", "b"], ["c", "d"]]) == "a,b\nc,d\n"
    print("  PASS  behaviour preserved")


def test_pair_up_is_strict() -> None:
    try:
        pair_up(["a", "b", "c"], [1, 2])
    except ValueError:
        print("  PASS  pair_up rejects mismatched lengths")
        return
    raise AssertionError("pair_up still truncates silently")


def test_split_valid_generator_trap() -> None:
    """Demonstrates why two comprehensions are not always safe."""
    records = iter([{"email": "a@b"}, {}])
    valid = [r for r in records if r.get("email")]
    invalid = [r for r in records if not r.get("email")]   # iterator exhausted
    assert len(valid) == 1
    assert len(invalid) == 0, "second pass over an iterator sees nothing"
    print("  PASS  two-pass trap demonstrated (invalid is empty, not 1)")


if __name__ == "__main__":
    test_all()
    test_pair_up_is_strict()
    test_split_valid_generator_trap()
