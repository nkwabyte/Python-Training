"""Exercise 11.3 — Replace stringly-typed state with enums.

The order-processing code below uses strings for status, permissions and
priority. Every bug in it is a bug that an enum makes impossible.

Run:  python ex03_enums.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Order:
    id: int
    status: str = "pending"
    priority: str = "normal"
    permissions: list[str] = field(default_factory=list)
    history: list[tuple[datetime, str]] = field(default_factory=list)


VALID_TRANSITIONS = {
    "pending": ["paid", "cancelled"],
    "paid": ["shipped", "refunded"],
    "shipped": ["delivered", "returned"],
    "delivered": [],
    "cancelled": [],
    "refunded": [],
    "returned": ["refunded"],
}


def transition(order: Order, new_status: str) -> None:
    """BUG 1: a typo in new_status raises KeyError far from its cause -- or
    worse, silently passes if the typo is in VALID_TRANSITIONS itself."""
    if new_status not in VALID_TRANSITIONS[order.status]:
        raise ValueError(f"cannot go from {order.status} to {new_status}")
    order.status = new_status
    order.history.append((datetime.now(), new_status))


def can_edit(order: Order, user_permissions: list[str]) -> bool:
    """BUG 2: permission strings are compared by value, so 'Admin' and 'admin'
    are different permissions, and nothing enumerates the valid set."""
    return "admin" in user_permissions or (
        "editor" in user_permissions and order.status == "pending"
    )


def priority_score(order: Order) -> int:
    """BUG 3: an unknown priority silently scores 0, so a typo'd 'urgnet' order
    sorts LAST rather than first. Nothing fails; the wrong thing just happens."""
    return {"low": 1, "normal": 2, "high": 3, "urgent": 4}.get(order.priority, 0)


def describe(order: Order) -> str:
    """BUG 4: adding a new status requires finding and updating every one of
    these chains, and nothing tells you when you have missed one."""
    if order.status == "pending":
        return "awaiting payment"
    elif order.status == "paid":
        return "preparing"
    elif order.status == "shipped":
        return "in transit"
    else:
        return "finished"


# TODO 1 -----------------------------------------------------------------------
# Status as an Enum, with the transition table as a class-level mapping and
# can_transition_to() as a method. Adding a status must be ONE edit.

# TODO 2 -----------------------------------------------------------------------
# Permission as a Flag, so a permission SET is a single value:
#     perms = Permission.READ | Permission.WRITE
#     Permission.WRITE in perms
# Add ADMIN as a combination that implies the others. Show that this makes
# can_edit shorter AND makes an invalid permission impossible to construct.

# TODO 3 -----------------------------------------------------------------------
# Priority as an IntEnum so ordering is free and sorting needs no key function.
# Then say why IntEnum is justified here and would not be for Status.

# TODO 4 -----------------------------------------------------------------------
# Rewrite describe() with match. Add a new Status member and observe what mypy
# says about the match. Then remove the wildcard case and observe what changes.
# Write down what exhaustiveness checking gives you that the if/elif chain
# cannot, and what it costs.

# TODO 5 -----------------------------------------------------------------------
# The boundary. Orders arrive as JSON with status as a string. Write:
#     Status.parse(raw: str) -> Status
# raising a useful error listing the valid values, and a to_json() that emits
# the string form. Then answer: WHERE in a program should string-to-enum
# conversion happen, and how many places should there be?


def verify() -> None:
    o = Order(1)
    assert o.status is Status.PENDING              # type: ignore[name-defined]

    transition(o, Status.PAID)                     # type: ignore[name-defined]
    assert o.status is Status.PAID                 # type: ignore[name-defined]

    try:
        transition(o, Status.DELIVERED)            # type: ignore[name-defined]
    except ValueError:
        pass
    else:
        raise AssertionError("invalid transition must raise")

    perms = Permission.READ | Permission.WRITE     # type: ignore[name-defined]
    assert Permission.WRITE in perms               # type: ignore[name-defined]
    assert Permission.ADMIN not in perms           # type: ignore[name-defined]

    assert Priority.URGENT > Priority.LOW          # type: ignore[name-defined]
    orders = [Order(1, priority=Priority.LOW),     # type: ignore[name-defined]
              Order(2, priority=Priority.URGENT)]  # type: ignore[name-defined]
    assert sorted(orders, key=lambda x: x.priority, reverse=True)[0].id == 2

    assert Status.parse("paid") is Status.PAID     # type: ignore[name-defined]
    try:
        Status.parse("payed")                      # type: ignore[name-defined]
    except ValueError as exc:
        assert "paid" in str(exc), "the error must list the valid values"
    else:
        raise AssertionError("a typo must be rejected at the boundary")

    print("all enum checks passed")


if __name__ == "__main__":
    verify()
