"""Solution 08.3 — Six leaks, fixed, with the tests that catch them.

The question that finds every one of these: "after this returns, who else can
reach this object, and what can they do to it?"
"""

from __future__ import annotations

from datetime import datetime
from types import MappingProxyType
from typing import Any


# --- leak 1: a getter returning the internal list -----------------------------
class ShoppingCart:
    """CAUSE: get_items() returned self._items, so a caller could append a
    negative-priced item and change the total without going through add().
    An accessor that returns a mutable internal is not encapsulation; it is a
    public attribute with extra steps."""

    def __init__(self) -> None:
        self._items: list[dict[str, Any]] = []

    def add(self, name: str, price: float, qty: int = 1) -> None:
        if price < 0 or qty < 1:
            raise ValueError("price must be >= 0 and qty >= 1")
        self._items.append({"name": name, "price": price, "qty": qty})

    @property
    def items(self) -> tuple[Any, ...]:
        # A tuple of MappingProxy views: the sequence cannot be changed, and
        # neither can the dicts inside it. Returning tuple(self._items) alone
        # would still hand out mutable dicts -- the shallow-copy trap from
        # Module 02, one level down.
        return tuple(MappingProxyType(i) for i in self._items)

    @property
    def total(self) -> float:
        return sum(i["price"] * i["qty"] for i in self._items)


# --- leak 2: storing the caller's list ----------------------------------------
class Report:
    """CAUSE: the constructor stored the caller's list. The caller kept a live
    handle and could change the report afterwards. Copy on the way IN is as
    important as copying on the way out, and is missed far more often."""

    def __init__(self, rows: list[list[str]]) -> None:
        self._rows = [list(r) for r in rows]     # deep enough for list-of-lists

    def row_count(self) -> int:
        return len(self._rows)

    def __iter__(self):  # type: ignore[no-untyped-def]
        return iter(tuple(r) for r in self._rows)


# --- leak 3: a mutable CLASS attribute ----------------------------------------
class Registry:
    """CAUSE: _handlers was a class attribute, so every instance shared one
    dict. `self._handlers[name] = handler` MUTATES the shared object rather
    than rebinding, so it never creates an instance attribute (Module 02).

    Two independent bugs here: the sharing, and the leaking getter."""

    def __init__(self) -> None:
        self._handlers: dict[str, Any] = {}      # per instance

    def register(self, name: str, handler: Any) -> None:
        self._handlers[name] = handler

    @property
    def handlers(self) -> MappingProxyType[str, Any]:
        # A read-only VIEW: O(1), and it stays live as new handlers register.
        # Note it is a view, not a snapshot -- the underlying dict is still
        # writable by us, and those writes are visible through the proxy. That
        # is the intended behaviour here; if you need a snapshot, copy.
        return MappingProxyType(self._handlers)


# --- leak 4: __dict__ and __repr__ exposing a secret ---------------------------
class Session:
    """CAUSE: to_dict() returned self.__dict__ -- both the internal dict itself
    (mutable, live) and the token inside it. __repr__ put the token in every
    log line and traceback that ever prints this object.

    Credentials in logs are one of the most common real leaks, precisely
    because __repr__ is called by places you did not write: logging,
    exceptions, debuggers, and error-reporting services that ship your
    tracebacks to a third party."""

    __slots__ = ("user", "created", "_token")

    def __init__(self, user: str) -> None:
        self.user = user
        self.created = datetime.now()
        self._token = "tok_" + user

    def __repr__(self) -> str:
        return f"Session(user={self.user!r}, created={self.created.isoformat()})"

    def to_dict(self) -> dict[str, Any]:
        return {"user": self.user, "created": self.created.isoformat()}

    def authenticate(self, candidate: str) -> bool:
        """The token is USED here and never handed out. If a caller never needs
        the value, do not give them a way to read it."""
        import hmac
        return hmac.compare_digest(self._token, candidate)


# --- leak 5: [[0]*cols]*rows --------------------------------------------------
class Matrix:
    """CAUSE: [[0.0] * cols] * rows repeats the REFERENCE to one inner list, so
    every row is the same object. Module 02's grid trap, in production form."""

    def __init__(self, rows: int, cols: int) -> None:
        if rows < 1 or cols < 1:
            raise ValueError("dimensions must be positive")
        self._rows, self._cols = rows, cols
        self._data = [[0.0] * cols for _ in range(rows)]
        # The inner [0.0] * cols is FINE: float is immutable, so sharing a
        # reference to 0.0 is harmless. Only the OUTER multiplication breaks.

    def get(self, r: int, c: int) -> float:
        return self._data[r][c]

    def set(self, r: int, c: int, value: float) -> None:
        self._data[r][c] = value

    def row(self, r: int) -> tuple[float, ...]:
        return tuple(self._data[r])


# --- leak 6: append-only in name only -----------------------------------------
class EventLog:
    """CAUSE: two leaks with different shapes.

    since() returned a NEW list, which is fine -- mutating it is harmless.
    That one is not actually a bug, and noticing that is part of the exercise:
    not every returned collection needs defending.

    clear_after_export() is the real bug. It hands out the internal list AND
    rebinds self._events to a new one, so the caller now owns the only
    reference to the entire history. An "append-only" log that can be emptied
    by a caller is not append-only, and the docstring is a lie the type system
    cannot catch."""

    def __init__(self) -> None:
        self._events: list[tuple[datetime, str]] = []

    def append(self, message: str) -> None:
        self._events.append((datetime.now(), message))

    def __iter__(self):  # type: ignore[no-untyped-def]
        return iter(tuple(self._events))     # snapshot, so mutation during
                                             # iteration cannot corrupt it

    def __len__(self) -> int:
        return len(self._events)

    def since(self, when: datetime) -> tuple[tuple[datetime, str], ...]:
        return tuple(e for e in self._events if e[0] >= when)

    def export(self) -> tuple[tuple[datetime, str], ...]:
        """Exports WITHOUT clearing. If truncation is genuinely required, it
        belongs in a separately named method whose name says so -- and probably
        should not exist on a type documented as append-only."""
        return tuple(self._events)


# --- tests --------------------------------------------------------------------
def test_cart_does_not_leak() -> None:
    c = ShoppingCart()
    c.add("widget", 10.0)
    before = c.total
    items = c.items
    try:
        items[0]["price"] = -100.0     # type: ignore[index]
    except TypeError:
        pass
    else:
        raise AssertionError("cart items are still mutable")
    assert c.total == before


def test_report_copies_its_input() -> None:
    rows = [["a"]]
    r = Report(rows)
    rows.append(["b"])
    rows[0].append("mutated")
    assert r.row_count() == 1
    assert list(r) == [("a",)]


def test_registry_is_not_shared_across_instances() -> None:
    r1, r2 = Registry(), Registry()
    r1.register("x", print)
    assert list(r2.handlers) == []
    try:
        r1.handlers["y"] = print      # type: ignore[index]
    except TypeError:
        pass
    else:
        raise AssertionError("handlers view is writable")


def test_session_repr_and_dict_hide_the_token() -> None:
    s = Session("ada")
    assert "tok_" not in repr(s)
    assert "tok_" not in str(s.to_dict())
    assert s.authenticate("tok_ada") is True
    assert s.authenticate("wrong") is False


def test_matrix_rows_are_independent() -> None:
    m = Matrix(3, 3)
    m.set(0, 0, 9.0)
    assert m.get(1, 0) == 0.0
    assert m.row(0) == (9.0, 0.0, 0.0)


def test_event_log_is_really_append_only() -> None:
    log = EventLog()
    log.append("started")
    log.append("continued")

    exported = log.export()
    assert len(log) == 2, "export must not clear"
    try:
        exported.append(("x", "y"))    # type: ignore[attr-defined]
    except AttributeError:
        pass
    else:
        raise AssertionError("export returned something mutable")

    snapshot = list(log)
    log.append("during iteration")
    assert len(snapshot) == 2


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"  PASS  {t.__name__}")
    print(f"\n{len(tests)} tests passed")
