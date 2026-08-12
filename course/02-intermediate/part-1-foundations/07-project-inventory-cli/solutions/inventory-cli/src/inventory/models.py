"""The domain types. Immutable, validated at construction, no I/O.

WHY IMMUTABLE ITEMS (the decision Stage 2 asks you to make and write down):

  1. Operations return a NEW item, so the change history falls out for free --
     you have the before and the after, both intact, with no bookkeeping.
  2. Every operation is testable with one equality assertion and no setup.
  3. Aliasing bugs (Module 02) become unrepresentable. An item handed to two
     parts of the program cannot be changed underneath either of them.
  4. Items become hashable and usable in sets and as dict keys.

The cost is allocation per change. For a warehouse with 10^4-10^6 items that is
irrelevant; at 10^8 it would not be. Know which regime you are in.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

from inventory.errors import ValidationError

SKU_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9-]{1,31}$")
LOCATION_PATTERN = re.compile(r"^[A-Z]\d{1,3}$")


def utcnow() -> datetime:
    """One place that reads the clock.

    Every other function takes a timestamp as a parameter with this as its
    default. That is what makes time-dependent logic testable without
    monkeypatching the datetime module (Module 18).
    """
    return datetime.now(timezone.utc)


@dataclass(frozen=True, order=True)
class Money:
    """Exact currency. Integer minor units, never float (Module 03)."""

    minor_units: int
    currency: str = "USD"

    @classmethod
    def parse(cls, raw: str | int | Decimal, currency: str = "USD") -> Money:
        if isinstance(raw, float):
            raise ValidationError(
                "price", raw,
                "floats cannot represent money exactly; pass a string like '9.99'",
            )
        try:
            value = Decimal(str(raw))
        except InvalidOperation as exc:
            raise ValidationError("price", raw, "not a number") from exc
        if value < 0:
            raise ValidationError("price", raw, "must not be negative")
        cents = (value * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP)
        return cls(int(cents), currency)

    def __mul__(self, qty: int) -> Money:
        if not isinstance(qty, int):
            return NotImplemented
        return Money(self.minor_units * qty, self.currency)

    __rmul__ = __mul__

    def __add__(self, other: Money) -> Money:
        if not isinstance(other, Money):
            return NotImplemented
        if other.currency != self.currency:
            raise ValidationError("currency", other.currency,
                                  f"cannot add to {self.currency}")
        return Money(self.minor_units + other.minor_units, self.currency)

    def __str__(self) -> str:
        sign = "-" if self.minor_units < 0 else ""
        whole, cents = divmod(abs(self.minor_units), 100)
        return f"{sign}${whole:,}.{cents:02d}"

    def __repr__(self) -> str:
        return f"Money.parse({str(self)[1:]!r})"


@dataclass(frozen=True)
class Item:
    sku: str
    name: str
    quantity: int
    unit_price: Money
    location: str
    tags: tuple[str, ...] = ()          # tuple: frozen must mean frozen
    updated: datetime = field(default_factory=utcnow, compare=False)

    def __post_init__(self) -> None:
        """Validate at CONSTRUCTION, so an invalid Item cannot exist.

        This is the single highest-value habit in domain modelling: if the type
        cannot hold a bad value, no downstream code needs to check for one.
        """
        if not SKU_PATTERN.match(self.sku):
            raise ValidationError(
                "sku", self.sku,
                "must be 2-32 chars of A-Z, 0-9 and hyphen, starting alphanumeric",
            )
        if not self.name.strip():
            raise ValidationError("name", self.name, "must not be empty")
        if "\n" in self.name:
            raise ValidationError("name", self.name, "must not contain newlines")
        if self.quantity < 0:
            raise ValidationError("quantity", self.quantity,
                                  "must not be negative")
        if not LOCATION_PATTERN.match(self.location):
            raise ValidationError("location", self.location,
                                  "must look like A1, B12 or C304")
        if len(set(self.tags)) != len(self.tags):
            raise ValidationError("tags", self.tags, "must not contain duplicates")

    @property
    def total_value(self) -> Money:
        return self.unit_price * self.quantity

    def with_quantity(self, quantity: int, *, at: datetime | None = None) -> Item:
        return replace(self, quantity=quantity, updated=at or utcnow())

    def with_location(self, location: str, *, at: datetime | None = None) -> Item:
        return replace(self, location=location, updated=at or utcnow())


@dataclass(frozen=True)
class Change:
    """One entry in the append-only history.

    Records the DELTA and the reason, not the resulting state. That makes the
    log replayable (the `undo` extension) and makes it obvious when two changes
    conflict.
    """

    sku: str
    action: str
    delta: int
    reason: str
    at: datetime = field(default_factory=utcnow)
    detail: str = ""

    def __str__(self) -> str:
        sign = f"{self.delta:+d}" if self.delta else "0"
        extra = f" ({self.detail})" if self.detail else ""
        return (f"{self.at:%Y-%m-%d %H:%M}  {self.action:<8} {sign:>5}  "
                f"{self.reason}{extra}")
