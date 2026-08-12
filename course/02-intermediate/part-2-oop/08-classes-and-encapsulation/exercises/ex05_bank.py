"""Exercise 08.5 — Design a class properly.

An Account class. Small enough to finish, large enough that every decision in
Module 08 shows up.

Everything here is a DESIGN exercise: the tests define the required behaviour,
but several choices are yours. Write down each choice and the reason.

Run:  python ex05_bank.py
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any


class InsufficientFunds(Exception):
    """Raised when a withdrawal would exceed the available balance."""


class Account:
    """A bank account.

    TODO 1  __init__(owner, opening_balance="0.00", overdraft_limit="0.00")
            Validate: owner non-empty; balances parse as Decimal; overdraft
            limit not negative. Store money as Decimal, never float (Module 03).

    TODO 2  `balance` must be a READ-ONLY property. There must be no way to
            write a balance directly -- it changes only through deposit,
            withdraw and transfer. That is the entire point of the class; if a
            caller can write self.balance, the class is a namespace, not an
            invariant.

    TODO 3  `available` -- a computed property: balance + overdraft_limit.

    TODO 4  deposit(amount) and withdraw(amount).
            Both reject zero and negative amounts (a negative deposit is a
            withdrawal that skips the overdraft check -- a real class of bug).
            withdraw raises InsufficientFunds when it would exceed `available`,
            and the exception must carry the requested and available amounts.

    TODO 5  transfer(other, amount).
            Think about failure: if the deposit into `other` raised, must the
            withdrawal be undone? Write down your answer and implement it.
            (There is no single right answer without a transaction manager --
            but there IS a wrong answer, which is not thinking about it.)

    TODO 6  A classmethod `open_joint(owner_a, owner_b, **kwargs)` returning a
            new account with a combined owner name. Use cls, not Account, and
            say why.

    TODO 7  `statement()` returning the transaction history WITHOUT letting the
            caller modify it. Pick one of the strategies from the README's table
            and justify it.

    TODO 8  __repr__ that is useful in a debugger and does NOT expose anything
            that should not appear in a log. Think about what an account
            number would mean here.

    TODO 9  Decide: __slots__ or not? Justify with reference to how many
            Account objects a real system holds at once.
    """


def verify() -> None:
    a = Account("Ada", "100.00")
    assert a.balance == Decimal("100.00")
    assert a.available == Decimal("100.00")

    a.deposit("50.00")
    assert a.balance == Decimal("150.00")

    a.withdraw("30.00")
    assert a.balance == Decimal("120.00")

    try:
        a.balance = Decimal("1000000")     # type: ignore[misc]
    except AttributeError:
        pass
    else:
        raise AssertionError("balance must be read-only")

    for bad in ["0.00", "-5.00"]:
        for method in (a.deposit, a.withdraw):
            try:
                method(bad)
            except ValueError:
                pass
            else:
                raise AssertionError(f"{method.__name__}({bad}) should raise")

    try:
        a.withdraw("999.00")
    except InsufficientFunds as exc:
        assert exc.requested == Decimal("999.00")     # type: ignore[attr-defined]
        assert exc.available == Decimal("120.00")     # type: ignore[attr-defined]
    else:
        raise AssertionError("overdraw must raise InsufficientFunds")

    o = Account("Bo", "10.00", overdraft_limit="100.00")
    assert o.available == Decimal("110.00")
    o.withdraw("60.00")
    assert o.balance == Decimal("-50.00")

    b = Account("Cy")
    a.transfer(b, "20.00")
    assert a.balance == Decimal("100.00")
    assert b.balance == Decimal("20.00")

    joint = Account.open_joint("Ada", "Bo", opening_balance="500.00")
    assert isinstance(joint, Account)
    assert "Ada" in joint.owner and "Bo" in joint.owner

    stmt = a.statement()
    before = len(list(stmt))
    try:
        stmt.append("forged entry")       # type: ignore[attr-defined]
    except AttributeError:
        pass
    assert len(list(a.statement())) == before, "statement must not be mutable"

    assert "Ada" in repr(a)
    print("all account checks passed")
    print(repr(a))
    for line in a.statement():
        print(" ", line)


if __name__ == "__main__":
    verify()
