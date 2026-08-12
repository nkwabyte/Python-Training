"""Exercise 09.3 — Five broken equality/hash implementations.

Each class below has a bug that makes it misbehave in a dict or a set. Find it,
explain it in terms of BUCKETS, fix it, and make the tests pass.

Run:  python ex03_eq_hash.py
"""

from __future__ import annotations

from typing import Any


# --- broken 1 -----------------------------------------------------------------
class UserA:
    def __init__(self, user_id: int, name: str) -> None:
        self.id = user_id
        self.name = name

    def __eq__(self, other: object) -> bool:
        return isinstance(other, UserA) and self.id == other.id


# --- broken 2 -----------------------------------------------------------------
class UserB:
    def __init__(self, user_id: int, name: str) -> None:
        self.id = user_id
        self.name = name

    def __eq__(self, other: object) -> bool:
        return isinstance(other, UserB) and self.id == other.id

    def __hash__(self) -> int:
        return hash((self.id, self.name))


# --- broken 3 -----------------------------------------------------------------
class Tag:
    def __init__(self, label: str) -> None:
        self.label = label

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Tag) and self.label == other.label

    def __hash__(self) -> int:
        return hash(self.label)

    def rename(self, new_label: str) -> None:
        self.label = new_label


# --- broken 4 -----------------------------------------------------------------
class Money:
    def __init__(self, cents: int, currency: str = "USD") -> None:
        self.cents = cents
        self.currency = currency

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return False                  # instead of NotImplemented
        return self.cents == other.cents and self.currency == other.currency

    def __hash__(self) -> int:
        return hash((self.cents, self.currency))


class Cents(int):
    """A type that WANTS to compare equal to a Money of the same value."""

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Money):
            return int(self) == other.cents
        return int(self) == other

    def __hash__(self) -> int:
        return hash(int(self))


# --- broken 5 -----------------------------------------------------------------
class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x, self.y = x, y

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Point) and (self.x, self.y) == (other.x, other.y)

    def __hash__(self) -> int:
        return 0            # "correct" but pathological. Why?


# --- tests --------------------------------------------------------------------
def test_a_is_hashable() -> None:
    a = UserA(1, "Ada")
    assert {a: "x"}[UserA(1, "Ada")] == "x"


def test_b_equal_objects_are_the_same_key() -> None:
    d = {UserB(1, "Ada"): "first"}
    d[UserB(1, "Ada Lovelace")] = "second"
    assert len(d) == 1, "two EQUAL objects created two dict entries"


def test_tag_stays_findable_after_rename() -> None:
    t = Tag("python")
    s = {t}
    t.rename("py")
    assert t in s, "the object is in the set but cannot be found"


def test_money_interoperates_with_cents() -> None:
    assert Money(500) == Cents(500)
    assert Cents(500) == Money(500)


def test_point_hash_is_distributed() -> None:
    points = {Point(x, y) for x in range(100) for y in range(100)}
    assert len(points) == 10_000
    hashes = {hash(p) for p in points}
    assert len(hashes) > 1_000, (
        f"only {len(hashes)} distinct hashes for 10,000 objects: every lookup "
        "is a linear scan"
    )


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
        except Exception as exc:
            print(f"  FAIL  {t.__name__}: {type(exc).__name__}: {exc}")
