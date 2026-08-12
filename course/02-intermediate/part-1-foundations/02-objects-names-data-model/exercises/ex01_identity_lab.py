"""Exercise 02.1 — The identity lab.

Twelve predictions. For EACH one, write your predicted output in the PREDICTION
comment BEFORE running anything. Then run and compare.

Scoring: count how many you got right out of 12. This is the single best
diagnostic in Part 1. Anything below 9 means re-read sections 2 through 6 of the
README before moving on -- not as punishment, but because every later module
assumes this is automatic for you.

Run:  python ex01_identity_lab.py
"""

from __future__ import annotations

import copy


def q01() -> None:
    # PREDICTION:
    a = [1, 2, 3]
    b = a
    b.append(4)
    print("q01", a)


def q02() -> None:
    # PREDICTION:
    a = [1, 2, 3]
    b = a
    b = [9, 9, 9]
    print("q02", a)


def q03() -> None:
    # PREDICTION:
    a = [1, 2]
    b = a
    b += [3]
    print("q03", a, a is b)


def q04() -> None:
    # PREDICTION:
    a = [1, 2]
    b = a
    b = b + [3]
    print("q04", a, a is b)


def q05() -> None:
    # PREDICTION:
    t = (1, 2)
    u = t
    u += (3,)
    print("q05", t, u, t is u)


def q06() -> None:
    # PREDICTION:
    grid = [[0] * 3] * 3
    grid[0][0] = 1
    print("q06", grid)


def q07() -> None:
    # PREDICTION:
    def add(item: str, bag: list[str] = []) -> list[str]:
        bag.append(item)
        return bag

    print("q07", add("a"), add("b"), add("c"))


def q08() -> None:
    # PREDICTION:
    outer = [[1, 2], [3, 4]]
    shallow = copy.copy(outer)
    deep = copy.deepcopy(outer)
    outer[0].append(99)
    print("q08", shallow, deep)


def q09() -> None:
    # PREDICTION: (and explain WHY, not just what)
    a, b = 256, 256
    c, d = 1000, 1000
    print("q09", a is b, c is d)


def q10() -> None:
    # PREDICTION:
    t = ([1, 2], "x")
    t[0].append(3)
    print("q10", t)
    try:
        t[0] = [9]
    except Exception as exc:
        print("q10 error:", type(exc).__name__)


def q11() -> None:
    # PREDICTION:
    nums = [1, 2, 3, 4, 5, 6]
    for n in nums:
        if n % 2 == 0:
            nums.remove(n)
    print("q11", nums)


def q12() -> None:
    # PREDICTION:
    a = [3, 1, 2]
    b = a.sort()
    c = sorted([3, 1, 2])
    print("q12", a, b, c)


if __name__ == "__main__":
    for fn in [q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11, q12]:
        fn()

    print(
        "\nNow write, for each question you got wrong, ONE sentence naming the\n"
        "mechanism you misjudged. Not 'I forgot' -- the actual mechanism.\n"
        "Put those sentences in PROGRESS.md's mistakes log."
    )
