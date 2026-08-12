"""Prices an order. Needs to know about discounts, which live on Customer."""

from shop.customer import Customer

TAX_RATE = 0.20


def subtotal(lines: list[tuple[str, int, float]]) -> float:
    return sum(qty * unit for _name, qty, unit in lines)


def total_for(customer: Customer, lines: list[tuple[str, int, float]]) -> float:
    base = subtotal(lines)
    discounted = base * (1 - customer.discount_rate())
    return round(discounted * (1 + TAX_RATE), 2)
