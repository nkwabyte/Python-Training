"""Exercise 08.3 — Six leaks.

Each class below hands out something it should not, or accepts something it
should have copied. Find the leak, fix it, and write the test that proves it.

The question to ask of every method: "after this returns, who else can reach
this object, and what can they do to it?"

Run:  python ex03_encapsulation.py
"""

from __future__ import annotations

from datetime import datetime
from typing import Any


# --- leak 1 -------------------------------------------------------------------
class ShoppingCart:
    def __init__(self) -> None:
        self._items: list[dict[str, Any]] = []

    def add(self, name: str, price: float, qty: int = 1) -> None:
        self._items.append({"name": name, "price": price, "qty": qty})

    def get_items(self) -> list[dict[str, Any]]:
        return self._items

    @property
    def total(self) -> float:
        return sum(i["price"] * i["qty"] for i in self._items)


# --- leak 2 -------------------------------------------------------------------
class Report:
    def __init__(self, rows: list[list[str]]) -> None:
        self._rows = rows

    def row_count(self) -> int:
        return len(self._rows)


# --- leak 3 -------------------------------------------------------------------
class Registry:
    _handlers: dict[str, Any] = {}          # note: a CLASS attribute

    def register(self, name: str, handler: Any) -> None:
        self._handlers[name] = handler

    def handlers(self) -> dict[str, Any]:
        return self._handlers


# --- leak 4 -------------------------------------------------------------------
class Session:
    def __init__(self, user: str) -> None:
        self.user = user
        self.created = datetime.now()
        self._token = "tok_" + user

    def __repr__(self) -> str:
        return f"Session(user={self.user!r}, token={self._token!r})"

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


# --- leak 5 -------------------------------------------------------------------
class Matrix:
    def __init__(self, rows: int, cols: int) -> None:
        self._data = [[0.0] * cols] * rows     # two bugs in one line

    def get(self, r: int, c: int) -> float:
        return self._data[r][c]

    def set(self, r: int, c: int, value: float) -> None:
        self._data[r][c] = value


# --- leak 6 -------------------------------------------------------------------
class EventLog:
    """Append-only. Or so the docstring claims."""

    def __init__(self) -> None:
        self._events: list[tuple[datetime, str]] = []

    def append(self, message: str) -> None:
        self._events.append((datetime.now(), message))

    def __iter__(self):  # type: ignore[no-untyped-def]
        return iter(self._events)

    def since(self, when: datetime) -> list[tuple[datetime, str]]:
        return [e for e in self._events if e[0] >= when]

    def clear_after_export(self) -> list[tuple[datetime, str]]:
        exported = self._events
        self._events = []
        return exported


# --- write these -------------------------------------------------------------
def test_cart_does_not_leak() -> None:
    """Prove a caller cannot change the total without going through add()."""
    ...


def test_report_copies_its_input() -> None: ...
def test_registry_is_not_shared_across_instances() -> None: ...
def test_session_repr_and_dict_hide_the_token() -> None: ...
def test_matrix_rows_are_independent() -> None: ...
def test_event_log_is_really_append_only() -> None: ...


if __name__ == "__main__":
    # Demonstrate each leak before fixing it.
    c = ShoppingCart()
    c.add("widget", 10.0)
    c.get_items().append({"name": "free stuff", "price": -100.0, "qty": 1})
    print("leak 1: total is now", c.total)

    rows = [["a"]]
    r = Report(rows)
    rows.append(["b"])
    print("leak 2: row_count is now", r.row_count())

    r1, r2 = Registry(), Registry()
    r1.register("x", print)
    print("leak 3: second registry sees", list(r2.handlers()))

    s = Session("ada")
    print("leak 4:", s)
    print("leak 4:", s.to_dict())

    m = Matrix(3, 3)
    m.set(0, 0, 9.0)
    print("leak 5: row 1 is", [m.get(1, c) for c in range(3)])

    log = EventLog()
    log.append("started")
    for entry in log:
        pass
    stolen = log.since(datetime.min)
    stolen.clear()
    print("leak 6: log still has", len(list(log)), "-- but check clear_after_export")
