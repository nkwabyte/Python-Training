"""Solution 08.2 — Delete the getters."""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal


class ProductV2:
    """Eight getter/setter pairs became three properties and three plain
    attributes. The call sites did not change.

    THE RULE THIS DEMONSTRATES: write a plain attribute. Promote it to a
    property the day it needs to do something. Because attribute and property
    access are the same syntax, that promotion breaks nothing -- so writing
    getters "in case you need them later" solves a problem Python does not
    have.

    WHY days_until_restock IS A METHOD, NOT A PROPERTY, AND TAKES `today`:

    Not a property, because a property looks like an attribute and readers
    assume attributes are (a) cheap and (b) STABLE. This value changes without
    anyone touching the object -- read it twice across midnight and it differs.
    An attribute that changes on its own violates the expectation the syntax
    creates. Parentheses signal "this is a computation with a result that
    depends on when you asked".

    Taking `today` as a parameter, rather than calling date.today() inside, is
    what makes it testable. With the internal call, testing "what happens the
    day before restock" requires freezing the system clock. With the parameter
    it is one line, and the test cannot become flaky at midnight or across a
    daylight-saving boundary. Every function whose behaviour depends on the
    clock should take the clock as an argument.
    """

    def __init__(self, sku: str, name: str, price: str, cost: str,
                 stock: int, restock_date: date) -> None:
        self._sku = sku                    # read-only: set once, never rebound
        self.name = name                   # plain: no invariant
        self.cost = Decimal(cost)          # plain: no invariant
        self.restock_date = restock_date   # plain: no invariant
        self.price = Decimal(price)        # property setter validates
        self.stock = stock                 # property setter validates
        self.discount_pct = 0              # property setter validates

    # -- identity: read-only ---------------------------------------------------
    @property
    def sku(self) -> str:
        """No setter. A SKU identifies the object; changing it would make every
        index, cache and foreign key holding the old value wrong. Read-only is
        not a restriction here, it is the correct model of the domain."""
        return self._sku

    # -- validated attributes --------------------------------------------------
    @property
    def price(self) -> Decimal:
        return self._price

    @price.setter
    def price(self, value: Decimal) -> None:
        if value < 0:
            raise ValueError(f"price cannot be negative, got {value}")
        self._price = value            # _price, NOT self.price -- the latter
                                       # would call this setter again forever

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, value: int) -> None:
        if value < 0:
            raise ValueError(f"stock cannot be negative, got {value}")
        self._stock = value

    @property
    def discount_pct(self) -> int:
        return self._discount_pct

    @discount_pct.setter
    def discount_pct(self, value: int) -> None:
        if not 0 <= value <= 100:
            raise ValueError(f"discount must be 0-100, got {value}")
        self._discount_pct = value

    # -- computed, cheap, stable -> properties ---------------------------------
    @property
    def margin(self) -> Decimal:
        return self.price - self.cost

    @property
    def sale_price(self) -> Decimal:
        return self.price * (100 - self.discount_pct) / 100

    @property
    def in_stock(self) -> bool:
        return self.stock > 0

    # -- depends on when you ask -> a method with the clock injected -----------
    def days_until_restock(self, today: date) -> int:
        return (self.restock_date - today).days

    def __repr__(self) -> str:
        return (f"ProductV2(sku={self.sku!r}, name={self.name!r}, "
                f"price={self.price}, stock={self.stock})")


def existing_callers(p) -> dict[str, object]:  # type: ignore[no-untyped-def]
    p.name = "Renamed"
    p.price = Decimal("19.99")
    p.stock = 5
    p.discount_pct = 10
    return {
        "sku": p.sku, "name": p.name, "price": p.price,
        "margin": p.margin, "sale_price": p.sale_price, "in_stock": p.in_stock,
    }


def verify() -> None:
    p = ProductV2("SKU-1", "Widget", "10.00", "4.00", 3,
                  date.today() + timedelta(days=7))

    result = existing_callers(p)
    assert result["sku"] == "SKU-1"
    assert result["name"] == "Renamed"
    assert result["margin"] == Decimal("15.99")
    assert result["sale_price"] == Decimal("17.991")
    assert result["in_stock"] is True

    for attr, bad in [("price", Decimal("-1")), ("stock", -1),
                      ("discount_pct", 101)]:
        try:
            setattr(p, attr, bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{attr} accepted {bad!r}")

    try:
        p.sku = "SKU-2"       # type: ignore[misc]
    except AttributeError:
        pass
    else:
        raise AssertionError("sku must be read-only")

    assert p.days_until_restock(date.today()) == 7
    assert p.days_until_restock(date.today() + timedelta(days=3)) == 4

    import inspect
    src = inspect.getsource(ProductV2)
    assert "def get_" not in src
    assert src.count("@property") <= 8

    print("all checks passed")
    print(repr(p))


if __name__ == "__main__":
    verify()
