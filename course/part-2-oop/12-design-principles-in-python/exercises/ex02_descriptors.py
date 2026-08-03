"""Exercise 12.2 — Four descriptors.

Run:  python ex02_descriptors.py
"""

from __future__ import annotations

from typing import Any


# TODO 1 -----------------------------------------------------------------------
class Positive:
    """A validated numeric attribute that must be > 0.

    Implement __set_name__, __get__, __set__.
    __get__ must return the descriptor itself when accessed on the CLASS
    (obj is None) -- otherwise Product.price would raise, and help(), Sphinx,
    and every introspection tool would break.
    """


# TODO 2 -----------------------------------------------------------------------
class Typed:
    """Runtime type enforcement: Typed(str), Typed(int), Typed(list, str).

    Then answer: this is what type hints DO NOT do (Module 04). When is runtime
    enforcement worth it, and when is a static checker enough?
    """


# TODO 3 -----------------------------------------------------------------------
class Lazy:
    """Compute once, on first access, then cache -- functools.cached_property,
    written by hand.

    The whole trick is ONE line: define __get__ but NOT __set__, so this is a
    NON-DATA descriptor and the instance __dict__ beats it. On first access,
    write the computed value into obj.__dict__[name]. Every later access finds
    it at rung 2 of the lookup ladder and never reaches this class again.

    Prove it: put a print in the computation and access the attribute three
    times. Then check that the value really is in obj.__dict__.

    Then answer: what breaks if you add a __set__ method that just raises?
    (Try it. The result is instructive and is exactly why cached_property has
    the shape it does.)
    """


# TODO 4 -----------------------------------------------------------------------
class Unit:
    """A quantity with a unit, converting on assignment.

        class Recipe:
            flour = Unit("g", {"kg": 1000, "g": 1, "oz": 28.35})

        r.flour = "2 kg"     ->  stored as 2000 (grams)
        r.flour              ->  2000
        r.flour_display      ->  "2000 g"

    Accept a number (assumed to be in the canonical unit) or a string with a
    unit suffix. Reject unknown units with a message listing the valid ones.
    """


# --- the class that motivated all this ---------------------------------------
class ProductBefore:
    """Six properties, thirty lines, four of them identical apart from a name.
    This is the duplication descriptors remove."""

    def __init__(self, name: str, price: float, weight: float) -> None:
        self.name = name
        self.price = price
        self.weight = weight

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value <= 0:
            raise ValueError("price must be positive")
        self._price = value

    @property
    def weight(self) -> float:
        return self._weight

    @weight.setter
    def weight(self, value: float) -> None:
        if value <= 0:
            raise ValueError("weight must be positive")
        self._weight = value


def verify() -> None:
    class Product:
        name = Typed(str)                        # type: ignore[name-defined]
        price = Positive()                       # type: ignore[name-defined]
        weight = Positive()                      # type: ignore[name-defined]
        tags = Typed(list)                       # type: ignore[name-defined]

        def __init__(self, name: str, price: float, weight: float) -> None:
            self.name, self.price, self.weight = name, price, weight
            self.tags = []

        @Lazy                                     # type: ignore[name-defined]
        def expensive_score(self) -> float:
            print("      (computing score)")
            return self.price * self.weight

    p = Product("widget", 10.0, 2.0)
    assert p.price == 10.0

    for attr, bad in [("price", 0), ("weight", -1)]:
        try:
            setattr(p, attr, bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{attr} accepted {bad}")

    try:
        p.name = 123          # type: ignore[assignment]
    except TypeError:
        pass
    else:
        raise AssertionError("Typed must reject the wrong type")

    assert isinstance(Product.price, Positive), (   # type: ignore[name-defined]
        "__get__ must return self when accessed on the class"
    )

    print("    accessing expensive_score three times:")
    assert p.expensive_score == 20.0
    assert p.expensive_score == 20.0
    assert p.expensive_score == 20.0
    assert "expensive_score" in p.__dict__, "Lazy must cache into the instance dict"

    class Recipe:
        flour = Unit("g", {"kg": 1000, "g": 1, "oz": 28.35})   # type: ignore[name-defined]

    r = Recipe()
    r.flour = "2 kg"          # type: ignore[assignment]
    assert r.flour == 2000
    r.flour = 500             # type: ignore[assignment]
    assert r.flour == 500
    try:
        r.flour = "2 furlongs"   # type: ignore[assignment]
    except ValueError as exc:
        assert "kg" in str(exc), "the error must list the valid units"
    else:
        raise AssertionError("unknown unit must be rejected")

    print("all descriptor checks passed")


if __name__ == "__main__":
    verify()
