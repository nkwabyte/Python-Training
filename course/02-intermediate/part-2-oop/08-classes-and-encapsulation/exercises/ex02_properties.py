"""Exercise 08.2 — Delete the getters.

`Product` below was written by someone whose habits come from Java. It has
eight getter/setter pairs and one real invariant buried among them.

Your job: reduce it to plain attributes plus AT MOST three properties, WITHOUT
breaking the existing call sites in `existing_callers()`.

That constraint is the whole point. In Java, removing a getter breaks every
caller. In Python it does not, because a plain attribute and a property are
accessed with identical syntax. Prove it to yourself.

Run:  python ex02_properties.py
"""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal


class Product:
    def __init__(self, sku: str, name: str, price: str, cost: str,
                 stock: int, restock_date: date) -> None:
        self._sku = sku
        self._name = name
        self._price = Decimal(price)
        self._cost = Decimal(cost)
        self._stock = stock
        self._restock_date = restock_date
        self._discount_pct = 0

    # -- eight getter/setter pairs, seven of which do nothing --------------
    def get_sku(self) -> str:
        return self._sku

    def get_name(self) -> str:
        return self._name

    def set_name(self, value: str) -> None:
        self._name = value

    def get_price(self) -> Decimal:
        return self._price

    def set_price(self, value: Decimal) -> None:
        if value < 0:
            raise ValueError("price cannot be negative")     # a REAL invariant
        self._price = value

    def get_cost(self) -> Decimal:
        return self._cost

    def set_cost(self, value: Decimal) -> None:
        self._cost = value

    def get_stock(self) -> int:
        return self._stock

    def set_stock(self, value: int) -> None:
        if value < 0:
            raise ValueError("stock cannot be negative")     # a REAL invariant
        self._stock = value

    def get_restock_date(self) -> date:
        return self._restock_date

    def set_restock_date(self, value: date) -> None:
        self._restock_date = value

    def get_discount_pct(self) -> int:
        return self._discount_pct

    def set_discount_pct(self, value: int) -> None:
        if not 0 <= value <= 100:
            raise ValueError("discount must be 0-100")       # a REAL invariant
        self._discount_pct = value

    # -- computed values, currently methods --------------------------------
    def get_margin(self) -> Decimal:
        return self._price - self._cost

    def get_sale_price(self) -> Decimal:
        return self._price * (100 - self._discount_pct) / 100

    def is_in_stock(self) -> bool:
        return self._stock > 0

    def days_until_restock(self) -> int:
        return (self._restock_date - date.today()).days


# TODO -------------------------------------------------------------------------
# Rewrite Product below as ProductV2 with:
#   - sku as a READ-ONLY property (it identifies the object; it must not change)
#   - name, cost, restock_date as PLAIN attributes (no validation needed)
#   - price, stock, discount_pct as properties WITH their validation
#   - margin, sale_price, in_stock as computed properties (no parentheses)
#   - days_until_restock as a METHOD taking `today` as a parameter
#
# The last one is a design question, not a style one. Answer it in a comment:
# why should days_until_restock NOT be a property, and why should it take
# `today` as an argument rather than calling date.today() itself?
class ProductV2:
    ...


def existing_callers(p) -> dict[str, object]:  # type: ignore[no-untyped-def]
    """Simulates code elsewhere in the codebase that must keep working.

    Note these use ATTRIBUTE syntax. If your rewrite is correct, the same
    function works against ProductV2 unchanged -- which is the demonstration.
    """
    p.name = "Renamed"
    p.price = Decimal("19.99")
    p.stock = 5
    p.discount_pct = 10
    return {
        "sku": p.sku,
        "name": p.name,
        "price": p.price,
        "margin": p.margin,
        "sale_price": p.sale_price,
        "in_stock": p.in_stock,
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
        p.sku = "SKU-2"
    except AttributeError:
        pass
    else:
        raise AssertionError("sku must be read-only")

    assert p.days_until_restock(date.today()) == 7
    assert p.days_until_restock(date.today() + timedelta(days=3)) == 4

    import inspect
    src = inspect.getsource(ProductV2)
    assert "def get_" not in src, "no getters"
    assert src.count("@property") <= 6, "too many properties; some should be plain"

    print("all checks passed")


if __name__ == "__main__":
    verify()
