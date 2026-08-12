"""Solution 11.4 — Four value objects."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from typing import Any, Iterator

DISPOSABLE_DOMAINS = frozenset({"mailinator.com", "guerrillamail.com", "10minutemail.com"})


@dataclass(frozen=True)
class Email:
    """A syntactically plausible email address.

    HOW MUCH VALIDATION IS CORRECT? Very little, and this is the important
    lesson. The RFC 5322 grammar permits quoted local parts, comments,
    IP-literal domains and folding whitespace; the well-known "correct" regex is
    ~6000 characters and still rejects valid addresses. Meanwhile a syntactically
    perfect address may not exist, and a syntactically odd one may work fine.

    So: check the handful of things that are certainly wrong (no @, empty parts,
    whitespace, no dot in the domain), and then PROVE the address by sending a
    confirmation email. Delivery is the only real validation. Every minute spent
    on the regex is a minute not spent on the confirmation flow.

    CASE: RFC 5321 says the local part is case-sensitive; essentially every
    provider treats it as insensitive. We lowercase only the domain, which is
    unambiguously case-insensitive, and preserve the local part. That means
    Ada@x.com and ada@x.com are two distinct Email values -- correct by the
    standard, occasionally surprising in practice. A system doing deduplication
    should normalise further, deliberately, at that point rather than here.
    """

    address: str

    def __post_init__(self) -> None:
        raw = self.address.strip()
        if not raw:
            raise ValueError("email must not be empty")
        if any(c.isspace() for c in raw):
            raise ValueError(f"email must not contain whitespace: {raw!r}")
        if raw.count("@") != 1:
            raise ValueError(f"email must contain exactly one @: {raw!r}")
        local, _, domain = raw.partition("@")
        if not local:
            raise ValueError(f"email has an empty local part: {raw!r}")
        if not domain:
            raise ValueError(f"email has an empty domain: {raw!r}")
        if "." not in domain or domain.startswith(".") or domain.endswith("."):
            raise ValueError(f"email domain looks invalid: {domain!r}")
        object.__setattr__(self, "address", f"{local}@{domain.lower()}")

    @property
    def local(self) -> str:
        return self.address.partition("@")[0]

    @property
    def domain(self) -> str:
        return self.address.partition("@")[2]

    @property
    def is_disposable(self) -> bool:
        return self.domain in DISPOSABLE_DOMAINS

    def __str__(self) -> str:
        return self.address


@dataclass(frozen=True, order=True)
class Percentage:
    """A value in [0, 100].

    THE 75-VERSUS-0.75 CONFUSION is a real and expensive bug class: someone
    passes 0.15 meaning 15% and gets 0.15%, or passes 15 meaning 0.15 and gets
    1500%. Both are silent.

    The fix is that the CONSTRUCTOR takes exactly one interpretation (a
    percentage), and the other is available only through a named classmethod.
    You cannot write from_fraction(75) by accident, because 75 is out of range
    for a fraction and raises.
    """

    value: Decimal

    def __init__(self, value: Any) -> None:
        if isinstance(value, float):
            value = Decimal(str(value))
        elif not isinstance(value, Decimal):
            value = Decimal(str(value))
        if not value.is_finite():
            raise ValueError(f"percentage must be finite, got {value}")
        if not Decimal(0) <= value <= Decimal(100):
            raise ValueError(f"percentage must be 0-100, got {value}")
        object.__setattr__(self, "value", value)

    @classmethod
    def from_fraction(cls, fraction: Any) -> Percentage:
        f = Decimal(str(fraction))
        if not Decimal(0) <= f <= Decimal(1):
            raise ValueError(
                f"a fraction must be 0-1, got {f}. Did you mean "
                f"Percentage({f}) rather than Percentage.from_fraction({f})?"
            )
        return cls(f * 100)

    @property
    def fraction(self) -> Decimal:
        return self.value / 100

    def of(self, amount: Decimal) -> Decimal:
        return (amount * self.fraction).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP)

    def __add__(self, other: Percentage) -> Percentage:
        """REFUSED for two Percentages, allowed for percentage POINTS.

        "50% + 30%" is ambiguous: it may mean 80% (adding shares of the same
        base) or a 95% compounded increase (applying one after the other). Since
        the two readings give different answers and the syntax cannot express
        which was meant, the operation is refused and named methods are provided
        instead. An operator whose meaning a reader must guess is worse than no
        operator.
        """
        return NotImplemented

    def plus_points(self, points: Any) -> Percentage:
        return Percentage(min(Decimal(100), self.value + Decimal(str(points))))

    def compounded_with(self, other: Percentage) -> Percentage:
        combined = (1 + self.fraction) * (1 + other.fraction) - 1
        return Percentage(min(Decimal(100), combined * 100))

    def __str__(self) -> str:
        normalised = self.value.normalize()
        text = format(normalised, "f")
        return f"{text}%"


@dataclass(frozen=True)
class DateRange:
    """A half-open interval [start, end).

    WHY HALF-OPEN, and it is the same reason as Python's slicing (Module 03):

      - adjacent ranges tile perfectly with no overlap and no gap:
        [Jan 1, Feb 1) + [Feb 1, Mar 1) == [Jan 1, Mar 1). With inclusive ends
        you must write Jan 31 and remember which months have 30 days, and every
        such boundary is a bug waiting for February.
      - length is end - start, with no +1 anywhere.
      - splitting at a point produces two ranges with no argument about which
        side owns the point.

    EMPTY RANGES: rejected here. An empty range is representable ([x, x)) and
    arguably useful as an identity element, but in a scheduling or billing
    domain it almost always signals a caller bug -- someone computed a duration
    of zero and did not notice. Rejecting it makes that bug loud. A library type
    would accept it; a domain type should not.
    """

    start: date
    end: date

    def __post_init__(self) -> None:
        if self.end <= self.start:
            raise ValueError(
                f"end must be after start: [{self.start}, {self.end})"
            )

    @property
    def days(self) -> int:
        return (self.end - self.start).days

    def __len__(self) -> int:
        return self.days

    def __contains__(self, day: object) -> bool:
        return isinstance(day, date) and self.start <= day < self.end

    def __iter__(self) -> Iterator[date]:
        current = self.start
        while current < self.end:
            yield current
            current += timedelta(days=1)

    def overlaps(self, other: DateRange) -> bool:
        return self.start < other.end and other.start < self.end

    def intersection(self, other: DateRange) -> DateRange | None:
        if not self.overlaps(other):
            return None
        return DateRange(max(self.start, other.start), min(self.end, other.end))

    def union(self, other: DateRange) -> DateRange:
        """Raises for disjoint ranges, because the union of two disjoint ranges
        is not a range -- it is a set of two. Returning the enclosing span would
        silently include dates in neither input, which is exactly the kind of
        quiet wrongness that surfaces three layers later in a billing total."""
        if not self.overlaps(other) and self.end != other.start and other.end != self.start:
            raise ValueError(
                f"[{self.start}, {self.end}) and [{other.start}, {other.end}) "
                "are disjoint; their union is not a single range"
            )
        return DateRange(min(self.start, other.start), max(self.end, other.end))

    def split_by_month(self) -> list[DateRange]:
        out: list[DateRange] = []
        cursor = self.start
        while cursor < self.end:
            if cursor.month == 12:
                next_month = date(cursor.year + 1, 1, 1)
            else:
                next_month = date(cursor.year, cursor.month + 1, 1)
            out.append(DateRange(cursor, min(next_month, self.end)))
            cursor = next_month
        return out

    def __str__(self) -> str:
        return f"[{self.start}, {self.end})"


@dataclass(frozen=True, order=True)
class Money:
    minor_units: int
    currency: str = "USD"

    @classmethod
    def parse(cls, raw: Any, currency: str = "USD") -> Money:
        if isinstance(raw, float):
            raise TypeError(
                f"Money cannot be built from a float: {raw!r} is not exactly "
                'representable. Pass a string like "19.99".'
            )
        try:
            value = Decimal(str(raw))
        except InvalidOperation as exc:
            raise ValueError(f"not a valid amount: {raw!r}") from exc
        cents = (value * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP)
        return cls(int(cents), currency)

    def _same(self, other: Money) -> None:
        if self.currency != other.currency:
            raise ValueError(
                f"cannot combine {self.currency} and {other.currency} without "
                "an explicit exchange rate"
            )

    def __add__(self, other: Money) -> Money:
        if not isinstance(other, Money):
            return NotImplemented
        self._same(other)
        return Money(self.minor_units + other.minor_units, self.currency)

    def __sub__(self, other: Money) -> Money:
        if not isinstance(other, Money):
            return NotImplemented
        self._same(other)
        return Money(self.minor_units - other.minor_units, self.currency)

    def __mul__(self, qty: int) -> Money:
        if not isinstance(qty, int):
            return NotImplemented          # Money * Money is meaningless
        return Money(self.minor_units * qty, self.currency)

    __rmul__ = __mul__

    def allocate(self, n: int) -> list[Money]:
        if n <= 0:
            raise ValueError("n must be positive")
        base, remainder = divmod(self.minor_units, n)
        return [Money(base + (1 if i < remainder else 0), self.currency)
                for i in range(n)]

    def __str__(self) -> str:
        sign = "-" if self.minor_units < 0 else ""
        whole, cents = divmod(abs(self.minor_units), 100)
        return f"{sign}${whole:,}.{cents:02d}"

    # ORDERING ACROSS CURRENCIES: order=True on the dataclass compares
    # (minor_units, currency) as a tuple, so USD and EUR sort by amount then by
    # code without raising. That is deliberate here: raising from __lt__ makes
    # sorted() on a mixed list explode halfway through, leaving the caller with
    # a partially consumed iterator and a confusing traceback. Sorting by
    # (amount, currency) is meaningless but harmless; ADDING across currencies
    # is meaningful-looking and wrong, so THAT is what raises. Put the loud
    # failure where the silent bug would be.


def verify() -> None:
    e = Email("  Ada@Example.COM ")
    assert str(e) == "Ada@example.com", str(e)
    assert e.domain == "example.com" and e.local == "Ada"
    assert e == Email("Ada@example.com")
    assert {e: 1}[Email("Ada@example.com")] == 1
    assert Email("x@mailinator.com").is_disposable
    for bad in ["", "no-at-sign", "a@@b.com", "@b.com", "a@", "a@b", "a b@c.com"]:
        try:
            Email(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Email({bad!r}) should have been rejected")

    p = Percentage(75)
    assert p.fraction == Decimal("0.75")
    assert str(p) == "75%"
    assert str(Percentage.from_fraction(0.125)) == "12.5%"
    assert p.of(Decimal("200.00")) == Decimal("150.00")
    assert Percentage(10) < Percentage(20)
    assert str(Percentage(50).compounded_with(Percentage(30))) == "95%"
    for bad in [-1, 101]:
        try:
            Percentage(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Percentage({bad}) should have been rejected")
    try:
        Percentage.from_fraction(75)
    except ValueError as exc:
        assert "Did you mean" in str(exc)

    r = DateRange(date(2026, 1, 1), date(2026, 2, 1))
    assert len(r) == 31
    assert date(2026, 1, 15) in r
    assert date(2026, 2, 1) not in r
    assert len(list(r)) == 31
    r2 = DateRange(date(2026, 1, 20), date(2026, 3, 1))
    assert r.overlaps(r2)
    assert r.intersection(r2) == DateRange(date(2026, 1, 20), date(2026, 2, 1))
    assert len(DateRange(date(2026, 1, 1), date(2026, 4, 1)).split_by_month()) == 3
    parts = DateRange(date(2026, 1, 1), date(2026, 4, 1)).split_by_month()
    assert sum(len(p) for p in parts) == 90
    for bad_start, bad_end in [(date(2026, 2, 1), date(2026, 1, 1)),
                               (date(2026, 1, 1), date(2026, 1, 1))]:
        try:
            DateRange(bad_start, bad_end)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid range should be rejected")

    m = Money.parse("19.99")
    assert str(m) == "$19.99"
    assert m + Money.parse("0.01") == Money.parse("20.00")
    assert m * 3 == Money.parse("59.97")
    parts_m = Money.parse("10.00").allocate(3)
    assert [str(x) for x in parts_m] == ["$3.34", "$3.33", "$3.33"]
    assert sum(parts_m[1:], parts_m[0]) == Money.parse("10.00")
    for bad_call, exc_type in [(lambda: Money.parse(19.99), TypeError),
                               (lambda: Money.parse("1") + Money.parse("1", "EUR"),
                                ValueError)]:
        try:
            bad_call()      # type: ignore[operator]
        except exc_type:
            pass
        else:
            raise AssertionError(f"expected {exc_type.__name__}")

    print("all value object checks passed")


if __name__ == "__main__":
    verify()
