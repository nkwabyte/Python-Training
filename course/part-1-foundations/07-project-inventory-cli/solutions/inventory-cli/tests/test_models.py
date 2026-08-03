from __future__ import annotations

from decimal import Decimal

import pytest

from inventory import ValidationError
from inventory.models import Item, Money


class TestMoney:
    def test_parses_string_exactly(self) -> None:
        assert Money.parse("19.99").minor_units == 1999

    def test_rejects_float(self) -> None:
        with pytest.raises(ValidationError, match="floats cannot represent"):
            Money.parse(19.99)  # type: ignore[arg-type]

    def test_no_drift_over_many_additions(self) -> None:
        total = Money(0)
        for _ in range(1000):
            total = total + Money.parse("0.01")
        assert total == Money.parse("10.00")

    def test_multiplication_by_quantity(self) -> None:
        assert Money.parse("9.99") * 3 == Money.parse("29.97")

    def test_str_formats_with_separators(self) -> None:
        assert str(Money.parse("1234567.05")) == "$1,234,567.05"

    def test_rejects_negative(self) -> None:
        with pytest.raises(ValidationError):
            Money.parse("-1.00")

    def test_decimal_input(self) -> None:
        assert Money.parse(Decimal("5.005")).minor_units == 501   # ROUND_HALF_UP


class TestItem:
    def test_valid(self) -> None:
        i = Item("SKU-1", "Widget", 5, Money.parse("2.00"), "A1")
        assert i.total_value == Money.parse("10.00")

    @pytest.mark.parametrize(
        ("kwargs", "field"),
        [
            ({"sku": "bad sku"}, "sku"),
            ({"sku": "-LEADING"}, "sku"),
            ({"name": "  "}, "name"),
            ({"name": "line\nbreak"}, "name"),
            ({"quantity": -1}, "quantity"),
            ({"location": "zz9"}, "location"),
            ({"tags": ("a", "a")}, "tags"),
        ],
    )
    def test_rejects_invalid(self, kwargs: dict, field: str) -> None:
        base = dict(sku="SKU-1", name="Widget", quantity=1,
                    unit_price=Money.parse("1.00"), location="A1", tags=())
        with pytest.raises(ValidationError) as exc:
            Item(**{**base, **kwargs})       # type: ignore[arg-type]
        assert exc.value.field == field

    def test_is_immutable(self) -> None:
        i = Item("SKU-1", "Widget", 5, Money.parse("2.00"), "A1")
        with pytest.raises(AttributeError):
            i.quantity = 10                   # type: ignore[misc]

    def test_with_quantity_returns_new_object(self) -> None:
        a = Item("SKU-1", "Widget", 5, Money.parse("2.00"), "A1")
        b = a.with_quantity(10)
        assert a.quantity == 5 and b.quantity == 10
        assert a is not b

    def test_unicode_name_is_fine(self) -> None:
        assert Item("SKU-1", "Café ☕", 1, Money.parse("1.00"), "A1").name == "Café ☕"
