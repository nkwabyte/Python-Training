"""Solution 03.1 — Money that does not drift."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from typing import Final

MINOR_UNITS: Final[dict[str, int]] = {"USD": 2, "EUR": 2, "GBP": 2, "JPY": 0}
SYMBOLS: Final[dict[str, str]] = {"USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥"}


class Money:
    """An exact currency amount.

    REPRESENTATION (TODO 1): an integer number of MINOR UNITS (cents), plus a
    currency code.

    Why integers rather than Decimal:
      - Exactness is structural, not a matter of remembering to quantize. There
        is no rounding mode to get wrong because there are no fractions.
      - Addition and subtraction are ordinary integer ops: fast, and impossible
        to make imprecise.
      - It matches how payment processors, ledgers, and databases actually
        store money (Stripe, banking cores, and most double-entry systems all
        use integer minor units).
      - Serialisation is trivial and unambiguous. "1999" cannot be
        misinterpreted; "19.99" can be parsed into a float by a careless
        consumer.
    The cost: percentages and currency conversion need explicit rounding
    decisions -- which is arguably a feature, since those decisions have real
    accounting consequences and should be visible.
    """

    __slots__ = ("_units", "currency")

    def __init__(self, amount: str | int | Decimal, currency: str = "USD") -> None:
        if isinstance(amount, float):
            # TODO 2: the most valuable four lines in the class.
            raise TypeError(
                "Money cannot be constructed from a float: 19.99 is not exactly "
                "representable in binary, so the error would be baked in at "
                'construction. Pass a string instead: Money("19.99").'
            )
        if currency not in MINOR_UNITS:
            raise ValueError(f"unknown currency {currency!r}")

        exponent = MINOR_UNITS[currency]
        if isinstance(amount, int):
            value = Decimal(amount)
        elif isinstance(amount, str):
            value = Decimal(amount)
        elif isinstance(amount, Decimal):
            value = amount
        else:
            raise TypeError(f"unsupported type {type(amount).__name__}")

        scaled = (value * (10**exponent)).quantize(Decimal(1), rounding=ROUND_HALF_UP)
        self._units = int(scaled)
        self.currency = currency

    # -- construction helpers --------------------------------------------------
    @classmethod
    def from_minor_units(cls, units: int, currency: str = "USD") -> Money:
        obj = cls.__new__(cls)
        object.__setattr__(obj, "_units", units)
        object.__setattr__(obj, "currency", currency)
        return obj

    @property
    def amount(self) -> Decimal:
        return Decimal(self._units).scaleb(-MINOR_UNITS[self.currency])

    # -- arithmetic (TODO 3, 4) -----------------------------------------------
    def _check(self, other: Money) -> None:
        if self.currency != other.currency:
            raise ValueError(
                f"cannot combine {self.currency} and {other.currency}: "
                "currency conversion needs an explicit rate and rounding rule"
            )

    def __add__(self, other: Money) -> Money:
        if not isinstance(other, Money):
            return NotImplemented
        self._check(other)
        return Money.from_minor_units(self._units + other._units, self.currency)

    def __sub__(self, other: Money) -> Money:
        if not isinstance(other, Money):
            return NotImplemented
        self._check(other)
        return Money.from_minor_units(self._units - other._units, self.currency)

    def __mul__(self, factor: int | Decimal) -> Money:
        # Money * Money is meaningless (dollars squared), so it is not defined.
        if isinstance(factor, float):
            raise TypeError("multiply Money by int or Decimal, never float")
        if not isinstance(factor, (int, Decimal)):
            return NotImplemented
        scaled = (Decimal(self._units) * Decimal(factor)).quantize(
            Decimal(1), rounding=ROUND_HALF_UP
        )
        return Money.from_minor_units(int(scaled), self.currency)

    __rmul__ = __mul__

    def __neg__(self) -> Money:
        return Money.from_minor_units(-self._units, self.currency)

    # -- comparison (TODO 5) ---------------------------------------------------
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self._units == other._units and self.currency == other.currency

    def __lt__(self, other: Money) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        self._check(other)
        return self._units < other._units

    def __hash__(self) -> int:
        # __eq__ and __hash__ must agree: equal objects must hash equally.
        # Hashing the same tuple that __eq__ compares guarantees it. (Module 09)
        return hash((self._units, self.currency))

    # -- display (TODO 6) ------------------------------------------------------
    def __str__(self) -> str:
        sign = "-" if self._units < 0 else ""
        digits = MINOR_UNITS[self.currency]
        whole, frac = divmod(abs(self._units), 10**digits or 1)
        symbol = SYMBOLS.get(self.currency, self.currency + " ")
        if digits == 0:
            return f"{sign}{symbol}{whole:,}"
        return f"{sign}{symbol}{whole:,}.{frac:0{digits}d}"

    def __repr__(self) -> str:
        return f"Money({str(self.amount)!r}, {self.currency!r})"

    # -- allocation (TODO 7) ---------------------------------------------------
    def allocate(self, n: int) -> list[Money]:
        """Split into n parts that sum EXACTLY to self.

        $10.00 / 3 is not $3.33 three times -- that loses a cent. The remainder
        must go somewhere, and accounting requires it to go somewhere explicit
        and deterministic. We distribute one minor unit at a time to the
        earliest parts, which is the standard "largest remainder" convention.
        """
        if n <= 0:
            raise ValueError("n must be positive")
        base, remainder = divmod(self._units, n)
        parts = [base + (1 if i < remainder else 0) for i in range(n)]
        return [Money.from_minor_units(p, self.currency) for p in parts]

    def allocate_by(self, ratios: list[int]) -> list[Money]:
        """Split proportionally, still summing exactly. Used for tax splits,
        revenue shares, and discount distribution."""
        total = sum(ratios)
        if total <= 0:
            raise ValueError("ratios must sum to a positive number")
        parts = [self._units * r // total for r in ratios]
        remainder = self._units - sum(parts)
        for i in range(remainder):
            parts[i % len(parts)] += 1
        return [Money.from_minor_units(p, self.currency) for p in parts]


def verify() -> None:
    a, b = Money("19.99"), Money("0.01")
    assert str(a + b) == "$20.00"
    assert (a + b) == Money("20.00")

    total = Money("0.00")
    for _ in range(10):
        total = total + Money("0.10")
    assert total == Money("1.00"), f"drift! got {total}"

    # the float version, for contrast
    ftotal = 0.0
    for _ in range(10):
        ftotal += 0.10
    assert ftotal != 1.0, "floats used to drift; if this fails, note the platform"

    parts = Money("10.00").allocate(3)
    assert [str(p) for p in parts] == ["$3.34", "$3.33", "$3.33"], parts
    assert sum(parts[1:], parts[0]) == Money("10.00")

    shares = Money("100.00").allocate_by([1, 1, 2])
    assert [str(s) for s in shares] == ["$25.00", "$25.00", "$50.00"], shares
    assert sum(shares[1:], shares[0]) == Money("100.00")

    assert str(Money("1234", "JPY")) == "¥1,234"
    assert Money("5.00") * 3 == Money("15.00")
    assert {Money("1.00"): "a"}[Money("1.00")] == "a"

    for bad, exc in [(lambda: Money(19.99), TypeError),
                     (lambda: Money("1.00") + Money("1.00", "EUR"), ValueError),
                     (lambda: Money("1.00") * 1.5, TypeError)]:
        try:
            bad()  # type: ignore[operator,arg-type]
        except exc:
            pass
        else:
            raise AssertionError(f"expected {exc.__name__}")

    print("all Money checks passed")


if __name__ == "__main__":
    verify()
