"""A customer. Needs order history to compute loyalty discounts."""

from shop.order import Order


class Customer:
    def __init__(self, name: str, tier: str = "standard") -> None:
        self.name = name
        self.tier = tier
        self.orders: list[Order] = []

    def discount_rate(self) -> float:
        base = {"standard": 0.0, "gold": 0.05, "platinum": 0.10}[self.tier]
        if len(self.orders) > 10:
            base += 0.02
        return base

    def place(self, order: Order) -> None:
        self.orders.append(order)
