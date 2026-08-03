"""An order. Needs pricing to compute its total."""

from shop.pricing import total_for


class Order:
    def __init__(self, customer, lines: list[tuple[str, int, float]]) -> None:  # type: ignore[no-untyped-def]
        self.customer = customer
        self.lines = lines

    def total(self) -> float:
        return total_for(self.customer, self.lines)
