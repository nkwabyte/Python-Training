"""Exercise 09.5 — A hashable, immutable mapping.

Build FrozenDict: everything a dict can do for READING, nothing it can do for
writing, and usable as a dict key or set member.

This exists in real code more often than you would think -- as a cache key made
of keyword arguments, as a configuration snapshot, as a graph node label.

Run:  python ex05_frozen_dict.py
"""

from __future__ import annotations

from collections.abc import Hashable, Iterator, Mapping
from typing import Any


class FrozenDict(Mapping[str, Any]):
    """An immutable, hashable mapping.

    Inheriting from collections.abc.Mapping gives you get, keys, values, items,
    __contains__, __eq__ and __ne__ for free, provided you implement the three
    abstract methods. Look up which three before starting -- finding that out is
    part of the exercise.

    TODO 1  __init__ accepting the same argument forms dict does:
              FrozenDict()
              FrozenDict({"a": 1})
              FrozenDict([("a", 1)])
              FrozenDict(a=1, b=2)
            Store a private copy. A caller who passes a dict and then mutates it
            must not change your FrozenDict (Module 08).

    TODO 2  The three abstract methods Mapping requires.

    TODO 3  __hash__. This is the hard part and the point of the exercise.
            - dicts have no defined order for hashing purposes, so
              {"a": 1, "b": 2} and {"b": 2, "a": 1} MUST hash equally
            - the hash must be consistent with the __eq__ that Mapping gave you
            - it must raise TypeError if any VALUE is unhashable, because
              FrozenDict({"a": [1,2]}) cannot honestly claim to be hashable
            - cache it: hashing is O(n) and a hashable object gets hashed a lot
            Hint: frozenset(self.items()) solves the ordering problem in one
            step. Work out why before using it.

    TODO 4  __repr__ that round-trips.

    TODO 5  Explicitly BLOCK mutation with clear errors:
            __setitem__, __delitem__, and any attribute assignment after
            construction. A silent "it just does not have that method"
            AttributeError is much less helpful than a message saying the type
            is immutable.

    TODO 6  Two derivation methods that return NEW FrozenDicts:
              with_(key, value)      -> a copy plus one entry
              without(key)           -> a copy minus one entry
            Immutable types need these, or they are unusable.

    TODO 7  Then answer:
            - MappingProxyType also gives a read-only mapping. Name two things
              FrozenDict does that MappingProxyType does not.
            - what should FrozenDict({"a": 1}) == {"a": 1} return? Justify.
    """


def verify() -> None:
    fd = FrozenDict(a=1, b=2)

    assert fd["a"] == 1
    assert fd.get("z", "default") == "default"
    assert len(fd) == 2
    assert set(fd) == {"a", "b"}
    assert set(fd.keys()) == {"a", "b"}
    assert sorted(fd.values()) == [1, 2]
    assert ("a", 1) in set(fd.items())
    assert "a" in fd and "z" not in fd

    assert FrozenDict({"a": 1}) == FrozenDict(a=1)
    assert FrozenDict(a=1, b=2) == FrozenDict(b=2, a=1)
    assert hash(FrozenDict(a=1, b=2)) == hash(FrozenDict(b=2, a=1)), (
        "insertion order must not affect the hash"
    )

    d = {FrozenDict(a=1): "value"}
    assert d[FrozenDict(a=1)] == "value"
    assert len({FrozenDict(a=1), FrozenDict(a=1)}) == 1

    for op, args in [("__setitem__", ("a", 9)), ("__delitem__", ("a",))]:
        try:
            getattr(fd, op)(*args)
        except TypeError as exc:
            assert "immutable" in str(exc).lower(), str(exc)
        else:
            raise AssertionError(f"{op} should have raised")

    try:
        fd.new_attribute = 1        # type: ignore[attr-defined]
    except (AttributeError, TypeError):
        pass
    else:
        raise AssertionError("attribute assignment should be blocked")

    source = {"a": 1}
    fd2 = FrozenDict(source)
    source["b"] = 2
    assert "b" not in fd2, "constructor must copy its input"

    assert fd.with_("c", 3) == FrozenDict(a=1, b=2, c=3)
    assert fd.without("a") == FrozenDict(b=2)
    assert fd == FrozenDict(a=1, b=2), "derivation must not mutate the original"

    try:
        hash(FrozenDict(bad=[1, 2]))
    except TypeError:
        pass
    else:
        raise AssertionError("a FrozenDict with unhashable values must not hash")

    assert eval(repr(fd)) == fd    # noqa: S307

    print("all FrozenDict checks passed")


if __name__ == "__main__":
    verify()
