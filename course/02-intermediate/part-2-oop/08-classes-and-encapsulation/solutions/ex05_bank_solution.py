"""Solution 08.5 — Design a class properly."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any

ZERO = Decimal("0.00")


class InsufficientFunds(Exception):
    """Carries the numbers, not a formatted string.

    An exception that only has a message forces every handler to parse English
    to react. Carrying `requested` and `available` lets a caller decide (retry
    with a smaller amount? offer an overdraft?) and lets the CLI or API render
    the message however it likes -- including as JSON. Module 16 makes this a
    rule.
    """

    def __init__(self, requested: Decimal, available: Decimal) -> None:
        super().__init__(
            f"cannot withdraw {requested}: only {available} available"
        )
        self.requested = requested
        self.available = available


def _money(value: Any, field: str) -> Decimal:
    """One conversion point, so no other method has to think about types."""
    if isinstance(value, float):
        raise TypeError(
            f"{field} must not be a float: {value!r} is not exactly "
            f'representable. Pass a string like "10.00".'
        )
    try:
        return Decimal(str(value)).quantize(Decimal("0.01"))
    except InvalidOperation as exc:
        raise ValueError(f"{field}: {value!r} is not a valid amount") from exc


class Account:
    """A bank account.

    __SLOTS__ DECISION (TODO 9): NO.

    A real banking system holds thousands of Account objects in memory at once,
    not millions -- accounts live in a database, and only the working set is
    materialised. At 10^3-10^4 instances, __slots__ saves under a megabyte,
    which is not a reason to do anything. Against that: an ORM will want to set
    attributes it manages, a serializer may want __dict__, and a subclass
    (SavingsAccount, EscrowAccount) would inherit a layout restriction for no
    benefit. Save __slots__ for the Points and the parse Nodes.
    """

    def __init__(self, owner: str, opening_balance: Any = "0.00",
                 overdraft_limit: Any = "0.00") -> None:
        if not owner or not owner.strip():
            raise ValueError("owner must not be empty")

        self.owner = owner.strip()
        self._balance = _money(opening_balance, "opening_balance")
        limit = _money(overdraft_limit, "overdraft_limit")
        if limit < ZERO:
            raise ValueError(f"overdraft_limit must not be negative, got {limit}")
        self._overdraft_limit = limit
        self._history: list[str] = []
        self._record("opened", self._balance)

    # -- read-only state -------------------------------------------------------
    @property
    def balance(self) -> Decimal:
        """No setter, deliberately.

        This is the entire reason the class exists. If a caller can write
        self.balance, the invariant "the balance only changes through recorded
        transactions" is unenforceable, the history is untrustworthy, and the
        class is a namespace with extra ceremony.

        Making it read-only costs nothing -- callers who want to change it were
        always going to have to call deposit or withdraw anyway.
        """
        return self._balance

    @property
    def overdraft_limit(self) -> Decimal:
        return self._overdraft_limit

    @property
    def available(self) -> Decimal:
        return self._balance + self._overdraft_limit

    # -- operations ------------------------------------------------------------
    def deposit(self, amount: Any) -> Decimal:
        value = self._positive(amount, "deposit")
        self._balance += value
        self._record("deposit", value)
        return self._balance

    def withdraw(self, amount: Any) -> Decimal:
        value = self._positive(amount, "withdraw")
        if value > self.available:
            raise InsufficientFunds(value, self.available)
        self._balance -= value
        self._record("withdraw", -value)
        return self._balance

    def transfer(self, other: Account, amount: Any) -> None:
        """FAILURE DECISION (TODO 5): withdraw first, and roll back by hand if
        the deposit raises.

        The reasoning: the two operations are not atomic and cannot be made so
        without a transaction manager. Given that, the question is which
        failure is worse. Depositing first and failing on the withdrawal
        CREATES MONEY -- the worst possible outcome in a ledger. Withdrawing
        first and failing on the deposit destroys money, which is bad but
        recoverable, and the rollback below makes even that unlikely.

        The compensating action is written explicitly and recorded in the
        history, so an auditor can see that it happened. A silent rollback is
        almost as bad as none.

        What this is NOT: correct under concurrency, or across a process crash
        between the two lines. A real system uses a database transaction and
        makes the whole transfer a single atomic unit. This is Module 27's
        subject, and the honest answer to "is this good enough" is "only for a
        single-threaded toy".
        """
        if other is self:
            raise ValueError("cannot transfer to the same account")
        value = self._positive(amount, "transfer")

        self.withdraw(value)
        try:
            other.deposit(value)
        except Exception:
            self._balance += value                    # compensate
            self._record("transfer-rollback", value)
            raise

    # -- alternative constructor ----------------------------------------------
    @classmethod
    def open_joint(cls, owner_a: str, owner_b: str, **kwargs: Any) -> Account:
        """cls, not Account.

        A subclass -- SavingsAccount, BusinessAccount -- calling
        SavingsAccount.open_joint() gets a SavingsAccount back. Hardcoding
        Account would silently downgrade the type and break every subsequent
        subclass-specific call. Named constructors are the main reason
        classmethod exists, because __init__ can only have one signature.
        """
        return cls(f"{owner_a} and {owner_b}", **kwargs)

    # -- history ---------------------------------------------------------------
    def statement(self) -> tuple[str, ...]:
        """A tuple (TODO 7).

        Chosen over the alternatives because:
          - list(self._history) hands out a mutable copy; harmless, but the
            type says "you may change this", which is a false invitation.
          - iter(self._history) is O(1) but single-use, and callers reasonably
            expect a statement to be re-readable.
          - returning self._history is the leak this whole module is about.
        A tuple is O(n), obviously immutable, indexable, and re-iterable. For a
        history of thousands of entries the copy cost is irrelevant; if it were
        not, the answer would be a generator plus a documented single-use
        contract.
        """
        return tuple(self._history)

    # -- helpers ---------------------------------------------------------------
    def _positive(self, amount: Any, operation: str) -> Decimal:
        value = _money(amount, operation)
        if value <= ZERO:
            raise ValueError(
                f"{operation} amount must be positive, got {value}. "
                f"A negative deposit is a withdrawal that skips the overdraft "
                f"check -- rejecting it here is not pedantry."
            )
        return value

    def _record(self, action: str, delta: Decimal) -> None:
        stamp = datetime.now().isoformat(timespec="seconds")
        self._history.append(
            f"{stamp}  {action:<18} {delta:>+12}  balance {self._balance:>12}"
        )

    def __repr__(self) -> str:
        """Useful in a debugger, safe in a log.

        Includes owner and balance because both are needed to identify the
        object during debugging. If this class had an account NUMBER, it would
        appear masked (****1234) or not at all -- __repr__ is called by
        logging, tracebacks, and error-reporting services that ship data to
        third parties, so anything sensitive in a repr is effectively public.
        Even the owner name is arguably too much under GDPR; in a real system
        this would be an opaque account ID.
        """
        return (f"Account(owner={self.owner!r}, balance={self._balance}, "
                f"available={self.available})")


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
        assert exc.requested == Decimal("999.00")
        assert exc.available == Decimal("120.00")
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

    # the rollback path
    class Rejecting(Account):
        def deposit(self, amount: Any) -> Decimal:
            raise RuntimeError("account frozen")

    frozen = Rejecting("Dee")
    before = a.balance
    try:
        a.transfer(frozen, "10.00")
    except RuntimeError:
        pass
    assert a.balance == before, "rollback failed: money was destroyed"
    assert any("rollback" in line for line in a.statement())

    joint = Account.open_joint("Ada", "Bo", opening_balance="500.00")
    assert isinstance(joint, Account)
    assert "Ada" in joint.owner and "Bo" in joint.owner

    # cls, not Account: a subclass gets its own type back
    class Savings(Account):
        pass

    assert type(Savings.open_joint("X", "Y")) is Savings

    stmt = a.statement()
    assert isinstance(stmt, tuple)
    try:
        stmt.append("forged")              # type: ignore[attr-defined]
    except AttributeError:
        pass
    else:
        raise AssertionError("statement must not be mutable")

    try:
        Account("Eve", 100.0)              # a float
    except TypeError:
        pass
    else:
        raise AssertionError("float construction must be rejected")

    assert "Ada" in repr(a)
    print("all account checks passed\n")
    print(repr(a))
    for line in a.statement():
        print(" ", line)


if __name__ == "__main__":
    verify()
