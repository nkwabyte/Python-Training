"""Exercise 11.4 — Four value objects that cannot hold an invalid value.

The theme: validation happens ONCE, at construction. After that, every function
receiving one of these types can trust it completely -- no re-checking, no
defensive code, no "what if the email is empty" branch anywhere.

Run:  python ex04_value_objects.py
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal


# TODO 1 -----------------------------------------------------------------------
@dataclass(frozen=True)
class Email:
    """A syntactically valid email address.

    - normalise: strip whitespace, lowercase the DOMAIN only (the local part is
      case-sensitive per RFC 5321, even though almost every provider ignores
      that -- note the discrepancy in a comment and pick a side)
    - reject: empty, no @, more than one @, empty local or domain part, a
      domain with no dot, whitespace anywhere inside
    - expose: .local, .domain, .is_disposable (against a small blocklist)
    - __str__ returns the address

    Then answer: full RFC 5322 validation by regex is famously about 6000
    characters long and still not exactly right. What is the correct amount of
    validation for an email address in a real system, and what actually proves
    an address is valid?
    """


# TODO 2 -----------------------------------------------------------------------
@dataclass(frozen=True, order=True)
class Percentage:
    """A value between 0 and 100 inclusive.

    - construct from a percentage (75) or from a fraction (0.75) via a
      classmethod. Make it impossible to confuse the two -- that confusion is a
      real and expensive bug class.
    - reject out-of-range and non-finite values
    - .fraction property
    - of(amount) applying the percentage to a Decimal
    - __str__ as "75%" or "12.5%" (no trailing zeros)
    - arithmetic: adding two Percentages -- does that make sense? Decide, and
      either implement it with a clamping rule or refuse it. Write down why.
    """


# TODO 3 -----------------------------------------------------------------------
@dataclass(frozen=True)
class DateRange:
    """A half-open interval [start, end).

    - reject end <= start (empty and inverted ranges are both errors here --
      decide whether an empty range should be legal and justify it)
    - .days, __len__, __contains__(date), __iter__ over the dates
    - overlaps(other), intersection(other) -> DateRange | None,
      union(other) -> DateRange (raise if they do not touch -- why?)
    - split_by_month() -> list[DateRange]

    Half-open is not arbitrary. Explain in a comment what
    [Jan 1, Feb 1) + [Feb 1, Mar 1) gives you that inclusive ranges do not, and
    connect it to Module 03's slicing convention.
    """


# TODO 4 -----------------------------------------------------------------------
@dataclass(frozen=True, order=True)
class Money:
    """Exact currency, from Module 03 -- now as a proper value object.

    - integer minor units + currency code
    - reject float construction
    - arithmetic only within one currency
    - multiplication by a quantity, never by another Money
    - allocate(n) splitting exactly, with no lost minor units
    - ordering only within one currency (what should comparing USD to EUR do --
      raise, or return NotImplemented? These give different behaviour in
      sorted(). Try both and pick.)
    """


def verify() -> None:
    e = Email("  Ada@Example.COM ")
    assert str(e) == "Ada@example.com", str(e)
    assert e.domain == "example.com"
    assert e.local == "Ada"
    assert e == Email("Ada@example.com")
    assert {e: 1}[Email("Ada@example.com")] == 1
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
    assert Percentage.from_fraction(0.125).__str__() == "12.5%"
    assert p.of(Decimal("200.00")) == Decimal("150.00")
    assert Percentage(10) < Percentage(20)
    for bad in [-1, 101]:
        try:
            Percentage(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Percentage({bad}) should have been rejected")

    r = DateRange(date(2026, 1, 1), date(2026, 2, 1))
    assert len(r) == 31
    assert date(2026, 1, 15) in r
    assert date(2026, 2, 1) not in r, "half-open: the end is excluded"
    assert len(list(r)) == 31
    r2 = DateRange(date(2026, 1, 20), date(2026, 3, 1))
    assert r.overlaps(r2)
    assert r.intersection(r2) == DateRange(date(2026, 1, 20), date(2026, 2, 1))
    assert len(DateRange(date(2026, 1, 1), date(2026, 4, 1)).split_by_month()) == 3
    try:
        DateRange(date(2026, 2, 1), date(2026, 1, 1))
    except ValueError:
        pass
    else:
        raise AssertionError("inverted range should be rejected")

    m = Money.parse("19.99")
    assert str(m) == "$19.99"
    assert m + Money.parse("0.01") == Money.parse("20.00")
    assert m * 3 == Money.parse("59.97")
    parts = Money.parse("10.00").allocate(3)
    assert [str(p) for p in parts] == ["$3.34", "$3.33", "$3.33"]
    assert sum(parts[1:], parts[0]) == Money.parse("10.00")
    try:
        Money.parse(19.99)      # type: ignore[arg-type]
    except TypeError:
        pass
    else:
        raise AssertionError("float construction must be rejected")

    print("all value object checks passed")


if __name__ == "__main__":
    verify()
