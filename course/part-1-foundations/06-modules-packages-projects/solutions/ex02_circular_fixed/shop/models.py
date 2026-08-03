"""FIX A: the extracted shared module.

The cycle was order -> pricing -> customer -> order. The reason all three
needed each other is that the TYPES were tangled with the BEHAVIOUR. Pulling
the data definitions into a module that imports nothing from the package breaks
every edge at once.

Note that this module has no imports from `shop` at all. That is the test of a
successful extraction: the new module must sit at the BOTTOM of the dependency
graph, not in the middle of it.
"""

from __future__ import annotations

from dataclasses import dataclass, field

DISCOUNT_TIERS: dict[str, float] = {
    "standard": 0.0,
    "gold": 0.05,
    "platinum": 0.10,
}
LOYALTY_BONUS = 0.02
LOYALTY_THRESHOLD = 10


@dataclass
class Customer:
    name: str
    tier: str = "standard"
    orders: list[Order] = field(default_factory=list)

    def discount_rate(self) -> float:
        base = DISCOUNT_TIERS[self.tier]
        if len(self.orders) > LOYALTY_THRESHOLD:
            base += LOYALTY_BONUS
        return base

    def place(self, order: Order) -> None:
        self.orders.append(order)


@dataclass
class Order:
    customer: Customer
    lines: list[tuple[str, int, float]]

    def total(self) -> float:
        # Import inside the method: pricing imports models, so a module-level
        # import here would recreate a cycle. This is fix B applied at exactly
        # one place, deliberately, with a comment -- which is the acceptable
        # way to use it.
        from shop.pricing import total_for

        return total_for(self.customer, self.lines)
