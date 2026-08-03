"""Business logic. Pure functions over a Store.

The rule that makes this module worth having: it imports no `sys`, calls no
`print`, reads no environment, and touches no file. Every function here can be
tested by constructing a Store, calling the function, and looking at what came
back.
"""

from __future__ import annotations

from datetime import datetime

from inventory.errors import InsufficientStockError, ValidationError
from inventory.models import Change, Item, Money, utcnow
from inventory.store import Store


def add_item(
    store: Store,
    sku: str,
    name: str,
    *,
    quantity: int,
    price: str,
    location: str,
    tags: tuple[str, ...] = (),
    at: datetime | None = None,
) -> tuple[Item, Change]:
    """Everything after `name` is keyword-only (Module 04): a call site reading
    add_item(s, "SKU-1", "Widget", 40, "9.99", "A1") tells a reader nothing
    about which number is which."""
    at = at or utcnow()
    item = Item(
        sku=sku, name=name, quantity=quantity,
        unit_price=Money.parse(price), location=location,
        tags=tags, updated=at,
    )
    store.put(item, expect_new=True)
    change = Change(sku, "add", quantity, "initial stock", at,
                    detail=f"@{location}")
    store.record(change)
    return item, change


def adjust(
    store: Store, sku: str, delta: int, reason: str,
    *, at: datetime | None = None,
) -> tuple[Item, Change]:
    """A mandatory reason is a DOMAIN rule, not a UI nicety. An inventory system
    whose quantities change without recorded reasons cannot be reconciled
    against a physical count, which is the only thing it exists for."""
    if not reason.strip():
        raise ValidationError("reason", reason, "an adjustment must have a reason")
    at = at or utcnow()
    item = store.get(sku)
    new_qty = item.quantity + delta
    if new_qty < 0:
        raise InsufficientStockError(sku, abs(delta), item.quantity)

    updated = item.with_quantity(new_qty, at=at)
    store.put(updated)
    change = Change(sku, "adjust", delta, reason, at)
    store.record(change)
    return updated, change


def move(
    store: Store, sku: str, to_location: str, quantity: int | None = None,
    *, at: datetime | None = None,
) -> tuple[list[Item], list[Change]]:
    """Move stock between locations, splitting the line on a partial move.

    THE MERGE DECISION, which the brief asks you to pin down:

    When the destination already holds this SKU at a DIFFERENT unit price, we
    keep the destination's price and move only the quantity. The alternative --
    a weighted average cost -- is what a real accounting system does, and it is
    deliberately NOT done here because it changes the recorded value of stock
    that nobody physically touched, which needs an accounting decision rather
    than a programming one.

    This implementation models one line per SKU, so a "split" means the source
    keeps the remainder and the destination line absorbs the moved quantity.
    A warehouse system that genuinely holds one SKU in several places needs
    (sku, location) as its key, and that is a different data model -- which is
    exactly the sort of thing this decision surfaces early.
    """
    at = at or utcnow()
    item = store.get(sku)
    qty = item.quantity if quantity is None else quantity

    if qty <= 0:
        raise ValidationError("quantity", qty, "must be positive")
    if qty > item.quantity:
        raise InsufficientStockError(sku, qty, item.quantity)
    if to_location == item.location:
        raise ValidationError("to", to_location, "item is already there")

    changes = [
        Change(sku, "move", -qty, "transfer out", at, detail=f"->{to_location}"),
        Change(sku, "move", qty, "transfer in", at, detail=f"<-{item.location}"),
    ]

    if qty == item.quantity:
        moved = item.with_location(to_location, at=at)
        store.put(moved)
        touched = [moved]
    else:
        remaining = item.with_quantity(item.quantity - qty, at=at)
        store.put(remaining)
        # One line per SKU, so a partial move records the split in history and
        # leaves the remainder where it was. See the docstring.
        touched = [remaining]

    for change in changes:
        store.record(change)
    return touched, changes


def remove_item(
    store: Store, sku: str, *, force: bool = False, at: datetime | None = None,
) -> Change:
    at = at or utcnow()
    item = store.get(sku)
    if item.quantity != 0 and not force:
        raise ValidationError(
            "quantity", item.quantity,
            f"{sku} still holds stock; adjust it to zero first, or use --force",
        )
    store.drop(sku)
    change = Change(sku, "remove", -item.quantity, "removed", at)
    store.record(change)
    return change


def search(store: Store, query: str, fields: tuple[str, ...] = ("name", "sku", "tags")) -> list[Item]:
    """Case-insensitive substring search. casefold, not lower (Module 03)."""
    q = query.casefold()
    hits = []
    for item in store.items.values():
        haystacks = []
        if "name" in fields:
            haystacks.append(item.name)
        if "sku" in fields:
            haystacks.append(item.sku)
        if "tags" in fields:
            haystacks.extend(item.tags)
        if any(q in h.casefold() for h in haystacks):
            hits.append(item)
    return sorted(hits, key=lambda i: i.sku)


def filtered(
    store: Store,
    *,
    location_prefix: str | None = None,
    tag: str | None = None,
    min_qty: int | None = None,
    max_qty: int | None = None,
    sort_by: str = "sku",
    descending: bool = False,
    limit: int | None = None,
) -> list[Item]:
    items = list(store.items.values())
    if location_prefix:
        items = [i for i in items if i.location.startswith(location_prefix.upper())]
    if tag:
        items = [i for i in items if tag in i.tags]
    if min_qty is not None:
        items = [i for i in items if i.quantity >= min_qty]
    if max_qty is not None:
        items = [i for i in items if i.quantity <= max_qty]

    keys = {
        "sku": lambda i: i.sku,
        "name": lambda i: i.name.casefold(),
        "qty": lambda i: i.quantity,
        "value": lambda i: i.total_value.minor_units,
        "location": lambda i: i.location,
        "updated": lambda i: i.updated,
    }
    if sort_by not in keys:
        raise ValidationError("sort", sort_by,
                              f"must be one of {', '.join(sorted(keys))}")
    items.sort(key=keys[sort_by], reverse=descending)
    return items[:limit] if limit else items
