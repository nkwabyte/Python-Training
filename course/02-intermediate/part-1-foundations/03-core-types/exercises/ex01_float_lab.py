"""Exercise 03.1 — Numbers that do not lie.

Part A: twelve predictions. Write your answer in the PREDICTION comment BEFORE
running. Part B: build a Money type that does not drift.

Run:  python ex01_float_lab.py
"""

from __future__ import annotations

import math
from decimal import Decimal


def part_a() -> None:
    """Predict each, then run."""
    checks = [
        # PREDICTION:
        ("0.1 + 0.2 == 0.3", lambda: 0.1 + 0.2 == 0.3),
        # PREDICTION:
        ("0.1 + 0.2", lambda: 0.1 + 0.2),
        # PREDICTION:
        ("round(2.5), round(3.5)", lambda: (round(2.5), round(3.5))),
        # PREDICTION:
        ("Decimal(0.1)", lambda: Decimal(0.1)),
        # PREDICTION:
        ('Decimal("0.1") + Decimal("0.2") == Decimal("0.3")',
         lambda: Decimal("0.1") + Decimal("0.2") == Decimal("0.3")),
        # PREDICTION:
        ("-7 // 2", lambda: -7 // 2),
        # PREDICTION:
        ("-7 % 3", lambda: -7 % 3),
        # PREDICTION:
        ("7 / 1", lambda: 7 / 1),
        # PREDICTION:
        ("float('nan') == float('nan')", lambda: float("nan") == float("nan")),
        # PREDICTION:
        ("1e16 + 1 == 1e16", lambda: 1e16 + 1 == 1e16),
        # PREDICTION:
        ("sum([0.1] * 10) == 1.0", lambda: sum([0.1] * 10) == 1.0),
        # PREDICTION:
        ("True + True, sum([True, False, True])",
         lambda: (True + True, sum([True, False, True]))),
    ]
    for label, fn in checks:
        print(f"  {label:<52} -> {fn()!r}")


# --- Part B: a Money type -----------------------------------------------------
class Money:
    """Currency amounts that never drift.

    TODO 1  Decide the internal representation. Two defensible choices:
              (a) Decimal, quantized to the currency's minor unit
              (b) an int number of minor units (cents) plus a currency code
            Pick one, and write a comment justifying it. Most payment systems
            choose (b). Say why.

    TODO 2  Constructor. Accept str ("19.99"), int, or Decimal. REJECT float
            with a TypeError and a message explaining why -- this is the single
            most valuable line in the class.

    TODO 3  __add__, __sub__ between Money of the SAME currency. Adding USD to
            EUR must raise, not silently coerce.

    TODO 4  Multiplication by an int or Decimal (a quantity), NOT by another
            Money -- money times money is meaningless.

    TODO 5  __eq__ and __hash__ so Money can be a dict key. (Module 09 covers
            the pair properly; do your best now and revisit.)

    TODO 6  __str__ ("$19.99") and __repr__ (Money('19.99', 'USD')).

    TODO 7  allocate(n): split an amount into n parts that SUM EXACTLY to the
            original, distributing the remainder one minor unit at a time.
            Splitting $10.00 three ways must give [3.34, 3.33, 3.33], not three
            times 3.33 with a lost cent. This is a real accounting requirement
            and the reason naive division is unacceptable for money.
    """

    def __init__(self, amount: str | int | Decimal, currency: str = "USD") -> None:
        raise NotImplementedError


def verify() -> None:
    a = Money("19.99")
    b = Money("0.01")
    assert str(a + b) == "$20.00"
    assert (a + b) == Money("20.00")

    total = Money("0.00")
    for _ in range(10):
        total = total + Money("0.10")
    assert total == Money("1.00"), f"drift! got {total}"

    parts = Money("10.00").allocate(3)  # type: ignore[attr-defined]
    assert len(parts) == 3
    assert sum(parts[1:], parts[0]) == Money("10.00"), "allocation lost money"
    assert [str(p) for p in parts] == ["$3.34", "$3.33", "$3.33"], parts

    try:
        Money(19.99)  # type: ignore[arg-type]
    except TypeError:
        pass
    else:
        raise AssertionError("float construction must be rejected")

    try:
        Money("1.00", "USD") + Money("1.00", "EUR")
    except ValueError:
        pass
    else:
        raise AssertionError("cross-currency addition must raise")

    print("all Money checks passed")


if __name__ == "__main__":
    print("=== Part A ===")
    part_a()
    print("\n=== Part B ===")
    verify()
