"""Pricing depends on models. Models does not depend on pricing at import time."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:                       # FIX D, where it genuinely applies
    from shop.models import Customer    # type-only: no runtime import at all

TAX_RATE = 0.20


def subtotal(lines: list[tuple[str, int, float]]) -> float:
    return sum(qty * unit for _name, qty, unit in lines)


def total_for(customer: Customer, lines: list[tuple[str, int, float]]) -> float:
    base = subtotal(lines)
    discounted = base * (1 - customer.discount_rate())
    return round(discounted * (1 + TAX_RATE), 2)
