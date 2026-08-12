"""Exercise 09.1 — Which dunder gets called?

Twelve cases. For each, predict (a) which dunder Python calls, (b) what happens
if it is missing, and (c) the output. Then run.

Run:  python ex01_protocols.py
"""

from __future__ import annotations


class OnlyGetItem:
    """No __iter__, no __contains__, no __len__."""

    def __init__(self, data: list[int]) -> None:
        self._data = data

    def __getitem__(self, i: int) -> int:
        print(f"    __getitem__({i!r})")
        return self._data[i]


class OnlyStr:
    def __str__(self) -> str:
        return "I am a nice string"


class OnlyLen:
    def __init__(self, n: int) -> None:
        self.n = n

    def __len__(self) -> int:
        print("    __len__ called")
        return self.n


class SelfIterator:
    def __init__(self, items: list[int]) -> None:
        self._items = items
        self._pos = 0

    def __iter__(self) -> SelfIterator:
        return self                       # the trap

    def __next__(self) -> int:
        if self._pos >= len(self._items):
            raise StopIteration
        self._pos += 1
        return self._items[self._pos - 1]


class Vec:
    def __init__(self, x: int) -> None:
        self.x = x

    def __mul__(self, other: object) -> object:
        print(f"    Vec.__mul__({other!r})")
        if isinstance(other, int):
            return Vec(self.x * other)
        return NotImplemented

    def __repr__(self) -> str:
        return f"Vec({self.x})"


class Sloppy:
    def __eq__(self, other: object) -> bool:
        return False                      # instead of NotImplemented


class Suppressor:
    def __enter__(self) -> Suppressor:
        return self

    def __exit__(self, *exc: object) -> bool:
        print(f"    __exit__ got {exc[0]}")
        return True                       # what does this do?


def q01() -> None:
    # PREDICTION: dunder?  missing?  output?
    print("q01"); og = OnlyGetItem([10, 20, 30])
    print("   ", list(og))


def q02() -> None:
    # PREDICTION:
    print("q02"); og = OnlyGetItem([10, 20, 30])
    print("   ", 20 in og)


def q03() -> None:
    # PREDICTION:
    print("q03"); og = OnlyGetItem([10, 20, 30])
    try:
        print("   ", len(og))
    except TypeError as exc:
        print("    TypeError:", exc)


def q04() -> None:
    # PREDICTION: what does each of the three lines print?
    print("q04"); o = OnlyStr()
    print("   ", str(o))
    print("   ", repr(o)[:20] + "...")
    print("   ", [o])


def q05() -> None:
    # PREDICTION: how many times is __len__ called?
    print("q05"); ol = OnlyLen(0)
    if ol:
        print("    truthy")
    else:
        print("    falsy")


def q06() -> None:
    # PREDICTION:
    print("q06"); si = SelfIterator([1, 2, 3])
    print("    first  loop:", [x for x in si])
    print("    second loop:", [x for x in si])


def q07() -> None:
    # PREDICTION: does this work? which dunder?
    print("q07"); v = Vec(5)
    print("   ", v * 3)


def q08() -> None:
    # PREDICTION: does this work? which dunder is tried, and what then?
    print("q08"); v = Vec(5)
    try:
        print("   ", 3 * v)
    except TypeError as exc:
        print("    TypeError:", exc)


def q09() -> None:
    # PREDICTION:
    print("q09"); s = Sloppy()
    print("   ", s == s)
    print("   ", s != s)


def q10() -> None:
    # PREDICTION: is the exception raised, suppressed, or something else?
    print("q10")
    with Suppressor():
        raise ValueError("boom")
    print("    we got here")


def q11() -> None:
    # PREDICTION: special methods are looked up on the TYPE. What happens here?
    print("q11")

    class Plain:
        pass

    p = Plain()
    p.__len__ = lambda: 42      # type: ignore[method-assign]
    try:
        print("   ", len(p))
    except TypeError as exc:
        print("    TypeError:", exc)


def q12() -> None:
    # PREDICTION: which of the two objects' __eq__ runs, and in what order?
    print("q12")

    class A:
        def __eq__(self, other: object) -> bool:
            print("    A.__eq__")
            return NotImplemented

    class B(A):
        def __eq__(self, other: object) -> bool:
            print("    B.__eq__")
            return True

    print("   ", A() == B())


if __name__ == "__main__":
    for fn in [q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11, q12]:
        fn()
