"""Reports return DATA. Rendering is cli.py's job.

That separation is what makes --json a two-line addition instead of a rewrite:
the same function feeds both the human table and the machine-readable output.
"""

from __future__ import annotations

import heapq
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta

from inventory.models import Item, Money, utcnow
from inventory.store import Store


@dataclass(frozen=True)
class LowStockRow:
    sku: str
    name: str
    quantity: int
    location: str


@dataclass(frozen=True)
class ValueRow:
    group: str
    items: int
    units: int
    value: Money


def low_stock(store: Store, threshold: int = 10) -> list[LowStockRow]:
    rows = [
        LowStockRow(i.sku, i.name, i.quantity, i.location)
        for i in store.items.values()
        if i.quantity <= threshold
    ]
    rows.sort(key=lambda r: (r.quantity, r.sku))
    return rows


def value_by(store: Store, group_by: str = "location") -> list[ValueRow]:
    getter = {
        "location": lambda i: i.location,
        "tag": None,                       # handled separately: one item, many tags
        "none": lambda i: "total",
    }
    if group_by == "tag":
        groups: dict[str, list[Item]] = defaultdict(list)
        for item in store.items.values():
            for tag in item.tags or ("(untagged)",):
                groups[tag].append(item)
    else:
        key = getter.get(group_by) or getter["none"]
        groups = defaultdict(list)
        for item in store.items.values():
            groups[key(item)].append(item)

    rows = []
    for group, items in groups.items():
        total = Money(0)
        for item in items:
            total = total + item.total_value
        rows.append(ValueRow(group, len(items),
                             sum(i.quantity for i in items), total))
    rows.sort(key=lambda r: -r.value.minor_units)
    return rows


def dead_stock(store: Store, days: int = 90, *, now: datetime | None = None) -> list[Item]:
    """`now` is a parameter with a default, not a call to utcnow() inside.

    That one choice is the difference between a test that constructs items with
    known timestamps and asserts, and a test that monkeypatches the datetime
    module. Any function whose behaviour depends on the clock should take the
    clock as an argument.
    """
    now = now or utcnow()
    cutoff = now - timedelta(days=days)
    stale = [i for i in store.items.values() if i.updated < cutoff and i.quantity > 0]
    return sorted(stale, key=lambda i: i.updated)


def top_by_value(store: Store, k: int = 10) -> list[Item]:
    """heapq.nlargest: O(n log k), and it streams (Module 05)."""
    return heapq.nlargest(k, store.items.values(),
                          key=lambda i: i.total_value.minor_units)


def tag_counts(store: Store) -> list[tuple[str, int]]:
    return Counter(t for i in store.items.values() for t in i.tags).most_common()
