"""CSV and JSON import/export.

Uses the csv module, not str.split. Product names contain commas, quotes and
occasionally newlines, and every hand-rolled CSV writer is correct only until
it meets one.
"""

from __future__ import annotations

import csv
import io
import json
from dataclasses import dataclass
from datetime import datetime

from inventory.errors import DataFileError
from inventory.models import Item, Money
from inventory.store import Store

CSV_FIELDS = ["sku", "name", "quantity", "unit_price", "location", "tags"]


def to_csv(items: list[Item]) -> str:
    buf = io.StringIO(newline="")
    writer = csv.DictWriter(buf, fieldnames=CSV_FIELDS, lineterminator="\n")
    writer.writeheader()
    for i in items:
        writer.writerow({
            "sku": i.sku, "name": i.name, "quantity": i.quantity,
            "unit_price": f"{i.unit_price.minor_units / 100:.2f}",
            "location": i.location, "tags": ";".join(i.tags),
        })
    return buf.getvalue()
    # Tags are joined with ';' not ',' so a tag list never needs CSV quoting
    # inside a field. A small format decision that removes a whole class of
    # round-trip bug.


def to_json(items: list[Item]) -> str:
    return json.dumps(
        [{"sku": i.sku, "name": i.name, "quantity": i.quantity,
          "unit_price": f"{i.unit_price.minor_units / 100:.2f}",
          "location": i.location, "tags": list(i.tags),
          "updated": i.updated.isoformat()} for i in items],
        indent=2, ensure_ascii=False,
    )


@dataclass(frozen=True)
class ImportPlan:
    """What an import WOULD do. Produced without touching the store, so
    --dry-run and the real import run identical code."""

    to_add: list[Item]
    to_update: list[tuple[Item, Item]]      # (existing, incoming)
    unchanged: list[Item]
    errors: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors

    def summary(self) -> str:
        return (f"{len(self.to_add)} to add, {len(self.to_update)} to update, "
                f"{len(self.unchanged)} unchanged, {len(self.errors)} errors")


def plan_import(store: Store, text: str, *, at: datetime | None = None) -> ImportPlan:
    """Parse and diff. Pure: no mutation, so --dry-run is free."""
    to_add: list[Item] = []
    to_update: list[tuple[Item, Item]] = []
    unchanged: list[Item] = []
    errors: list[str] = []

    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames is None or "sku" not in reader.fieldnames:
        raise DataFileError("CSV has no header row, or no 'sku' column")

    for line_no, row in enumerate(reader, start=2):    # 2: header is line 1
        try:
            incoming = Item(
                sku=(row.get("sku") or "").strip(),
                name=(row.get("name") or "").strip(),
                quantity=int(row.get("quantity") or 0),
                unit_price=Money.parse(row.get("unit_price") or "0"),
                location=(row.get("location") or "").strip(),
                tags=tuple(t for t in (row.get("tags") or "").split(";") if t),
                updated=at or datetime.now().astimezone(),
            )
        except Exception as exc:                        # noqa: BLE001
            errors.append(f"line {line_no}: {exc}")
            continue

        existing = store.items.get(incoming.sku)
        if existing is None:
            to_add.append(incoming)
        elif (existing.name, existing.quantity, existing.unit_price,
              existing.location, existing.tags) == (
              incoming.name, incoming.quantity, incoming.unit_price,
              incoming.location, incoming.tags):
            unchanged.append(existing)
        else:
            to_update.append((existing, incoming))

    return ImportPlan(to_add, to_update, unchanged, errors)


def apply_import(store: Store, plan: ImportPlan) -> int:
    if not plan.ok:
        raise DataFileError(
            f"refusing to import with {len(plan.errors)} errors:\n  "
            + "\n  ".join(plan.errors[:10])
        )
    for item in plan.to_add:
        store.put(item)
    for _existing, incoming in plan.to_update:
        store.put(incoming)
    return len(plan.to_add) + len(plan.to_update)
