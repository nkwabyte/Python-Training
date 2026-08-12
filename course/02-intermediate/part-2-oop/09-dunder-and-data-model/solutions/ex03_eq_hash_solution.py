"""Solution 09.3 — Five broken equality/hash implementations, fixed.

Every bug here is one of three rules being broken. All three are consequences
of how a hash table works, not arbitrary conventions:

  R1  equal objects MUST have equal hashes
  R2  a hashed value must not change while the object is in a hash container
  R3  __eq__ must return NotImplemented, not False, for types it does not know
"""

from __future__ import annotations

from typing import Any


# --- fixed 1: __eq__ without __hash__ -----------------------------------------
class UserA:
    """CAUSE: defining __eq__ sets __hash__ to None automatically.

    That is not Python being awkward. The default __hash__ is based on
    IDENTITY, so two objects that your __eq__ says are equal would get
    different hashes -- breaking R1 and creating unreachable dict entries.
    Rather than let you build that silently, Python removes __hash__ and makes
    the failure immediate and loud.

    FIX: define __hash__ over the same fields __eq__ compares.
    """

    def __init__(self, user_id: int, name: str) -> None:
        self.id = user_id
        self.name = name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UserA):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)          # exactly what __eq__ compares


# --- fixed 2: hash and eq disagree --------------------------------------------
class UserB:
    """CAUSE: __eq__ compares only id; __hash__ hashes (id, name). So two
    users with the same id and different names are EQUAL but hash DIFFERENTLY
    -- R1 broken.

    In the bucket picture: they are equal, so the dict should treat them as one
    key. But they hash to different buckets, so the dict never even compares
    them and stores two entries. The dict now contains two keys that are equal
    to each other, which is supposed to be impossible, and every downstream
    assumption about key uniqueness is now false.

    FIX: hash exactly the fields __eq__ compares. Whenever you change one, look
    at the other -- they are one decision written in two places.
    """

    def __init__(self, user_id: int, name: str) -> None:
        self.id = user_id
        self.name = name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UserB):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


# --- fixed 3: mutable hashed state --------------------------------------------
class Tag:
    """CAUSE: label is hashed AND mutable. Insert into a set, rename, and the
    object's hash changes while it sits in a bucket chosen by the OLD hash.
    Lookup computes the NEW hash, goes to a different bucket, finds nothing --
    R2 broken. The object is in the set (len() proves it) and unfindable.

    THREE FIXES, in order of preference:

    1. Make it immutable. Remove rename(); derive a new Tag instead. Best,
       because the bug becomes unrepresentable. This is what frozen dataclasses
       are for (Module 11).
    2. Hash something immutable instead -- an id assigned at construction.
       Correct if identity, not label, is what makes two tags "the same".
    3. Remove-mutate-reinsert at every call site. Correct and fragile: one
       forgotten call site restores the bug.

    Implemented as (1).
    """

    __slots__ = ("_label",)

    def __init__(self, label: str) -> None:
        object.__setattr__(self, "_label", label)

    @property
    def label(self) -> str:
        return self._label

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError("Tag is immutable; use renamed() for a new one")

    def renamed(self, new_label: str) -> Tag:
        return Tag(new_label)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tag):
            return NotImplemented
        return self._label == other._label

    def __hash__(self) -> int:
        return hash(self._label)

    def __repr__(self) -> str:
        return f"Tag({self._label!r})"


# --- fixed 4: False instead of NotImplemented ---------------------------------
class Money:
    """CAUSE: returning False for an unknown type claims authority.

    `Money(500) == Cents(500)` calls Money.__eq__ first, which returns False.
    Python takes that as a definitive answer and never asks Cents. So the
    comparison is asymmetric: Cents(500) == Money(500) is True (Cents was
    asked), and Money(500) == Cents(500) is False. Equality that is not
    symmetric breaks sorting, set membership, and every caller's assumptions.

    NotImplemented means "I do not know" -- Python then tries the reflected
    operation and only raises/falls back to identity if BOTH decline.
    """

    __slots__ = ("cents", "currency")

    def __init__(self, cents: int, currency: str = "USD") -> None:
        object.__setattr__(self, "cents", cents)
        object.__setattr__(self, "currency", currency)

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError("Money is immutable")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented          # the fix
        return (self.cents, self.currency) == (other.cents, other.currency)

    def __hash__(self) -> int:
        return hash((self.cents, self.currency))

    def __repr__(self) -> str:
        return f"Money({self.cents}, {self.currency!r})"


class Cents(int):
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Money):
            return int(self) == other.cents
        return int(self) == other

    def __hash__(self) -> int:
        return hash(int(self))


# --- fixed 5: constant hash ---------------------------------------------------
class Point:
    """CAUSE: __hash__ returning 0 is CORRECT but pathological.

    It satisfies R1 -- equal objects trivially have equal hashes -- so nothing
    is unreachable. But every object lands in the same bucket, so the hash table
    degenerates into a linked list and every lookup becomes a linear scan with
    an __eq__ call per element. A dict of 10,000 such points does 10,000
    comparisons per lookup: O(1) has silently become O(n), with no error and no
    warning, only a program that gets slower as it grows.

    This is worth knowing because the same thing happens accidentally: hashing
    a field with very few distinct values (a status enum, a boolean, a
    truncated timestamp) gives a handful of buckets and the same collapse.

    FIX: hash the tuple of the fields __eq__ compares. Python's tuple hash is
    well distributed.
    """

    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        self.x, self.y = x, y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))


# --- tests --------------------------------------------------------------------
def test_a_is_hashable() -> None:
    assert {UserA(1, "Ada"): "x"}[UserA(1, "Ada")] == "x"


def test_b_equal_objects_are_the_same_key() -> None:
    d = {UserB(1, "Ada"): "first"}
    d[UserB(1, "Ada Lovelace")] = "second"
    assert len(d) == 1
    assert d[UserB(1, "anything")] == "second"


def test_tag_stays_findable_after_rename() -> None:
    t = Tag("python")
    s = {t}
    assert t in s
    new = t.renamed("py")
    assert new not in s and t in s, "renaming derives a NEW tag"
    try:
        t.label = "py"        # type: ignore[misc]
    except AttributeError:
        pass
    else:
        raise AssertionError("Tag must be immutable")


def test_money_interoperates_with_cents() -> None:
    assert Money(500) == Cents(500)
    assert Cents(500) == Money(500)
    assert (Money(500) == "not money") is False     # falls back to identity


def test_point_hash_is_distributed() -> None:
    points = {Point(x, y) for x in range(100) for y in range(100)}
    assert len(points) == 10_000
    hashes = {hash(p) for p in points}
    assert len(hashes) > 9_000, f"only {len(hashes)} distinct hashes"


def test_the_lesson_measured() -> None:
    """Show what a constant hash actually costs."""
    import time

    class BadPoint(Point):
        __slots__ = ()

        def __hash__(self) -> int:
            return 0

    for cls, label in [(Point, "good hash"), (BadPoint, "constant hash")]:
        objs = {cls(x, y) for x in range(60) for y in range(60)}
        probe = cls(59, 59)
        start = time.perf_counter()
        for _ in range(2000):
            probe in objs      # noqa: B015
        elapsed = (time.perf_counter() - start) * 1000
        print(f"        {label:<16} {len(objs):>5} items, 2000 lookups: "
              f"{elapsed:7.2f} ms")


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"  PASS  {t.__name__}")
    print(f"\n{len(tests)} tests passed")
