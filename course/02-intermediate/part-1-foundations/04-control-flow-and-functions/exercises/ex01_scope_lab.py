"""Exercise 04.1 — Scope and closure predictions.

Twelve questions. Write your prediction in the PREDICTION comment BEFORE
running. Several of these raise; predicting the EXCEPTION TYPE counts as a
correct answer.

Run:  python ex01_scope_lab.py
"""

from __future__ import annotations

counter = 0
items: list[int] = []
config = {"debug": False}


def q01() -> None:
    # PREDICTION:
    print("q01", counter)


def q02() -> None:
    # PREDICTION:
    try:
        counter += 1  # type: ignore[misc]  # noqa: F821
        print("q02", counter)
    except Exception as exc:
        print("q02", type(exc).__name__)


def q03() -> None:
    # PREDICTION:
    items.append(1)
    config["debug"] = True
    print("q03", items, config)


def q04() -> None:
    # PREDICTION:
    x = "outer"

    def inner() -> None:
        print("q04", x)

    inner()


def q05() -> None:
    # PREDICTION:
    x = "outer"

    def inner() -> None:
        x = "inner"          # noqa: F841
    inner()
    print("q05", x)


def q06() -> None:
    # PREDICTION:
    x = "outer"

    def inner() -> None:
        nonlocal x
        x = "inner"
    inner()
    print("q06", x)


def q07() -> None:
    # PREDICTION:
    funcs = [lambda: i for i in range(3)]
    print("q07", [f() for f in funcs])


def q08() -> None:
    # PREDICTION:
    funcs = [lambda i=i: i for i in range(3)]
    print("q08", [f() for f in funcs])


def q09() -> None:
    # PREDICTION:
    i = "untouched"
    squares = [i * i for i in range(3)]
    print("q09", i, squares)


def q10() -> None:
    # PREDICTION:
    for j in range(3):
        pass
    print("q10", j)


def q11() -> None:
    # PREDICTION: (what does each loop print?)
    for n in [1, 3, 5]:
        if n % 2 == 0:
            break
    else:
        print("q11a else ran")

    for n in [1, 2, 5]:
        if n % 2 == 0:
            break
    else:
        print("q11b else ran")

    for n in []:
        pass
    else:
        print("q11c else ran")


def q12() -> None:
    # PREDICTION:
    def make_adders() -> list:  # type: ignore[type-arg]
        adders = []
        for n in range(3):
            def adder(x: int, n: int = n) -> int:
                return x + n
            adders.append(adder)
        return adders

    print("q12", [a(10) for a in make_adders()])


if __name__ == "__main__":
    for fn in [q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11, q12]:
        fn()
    print(
        "\nFor every one you got wrong, write ONE sentence naming the mechanism\n"
        "(compile-time local decision / cell sharing / comprehension scope /\n"
        "nobreak semantics). Put it in PROGRESS.md."
    )
