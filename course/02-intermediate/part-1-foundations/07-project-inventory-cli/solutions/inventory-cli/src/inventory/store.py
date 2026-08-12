"""Persistence and indexing. Knows about files; knows nothing about the CLI."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from inventory.errors import DataFileError, DuplicateSKUError, NotFoundError
from inventory.models import Change, Item, Money

SCHEMA_VERSION = 1


@dataclass
class Store:
    """In-memory inventory with a by-SKU index and an append-only history.

    A schema version is written from day one. It costs one integer and it is
    the difference between "we can migrate this" and "we cannot tell what this
    file is". Every persistent format should have one.
    """

    items: dict[str, Item] = field(default_factory=dict)
    history: list[Change] = field(default_factory=list)

    # -- queries ---------------------------------------------------------------
    def get(self, sku: str) -> Item:
        try:
            return self.items[sku]
        except KeyError:
            raise NotFoundError(sku) from None

    def by_location(self) -> dict[str, list[Item]]:
        groups: dict[str, list[Item]] = {}
        for item in self.items.values():
            groups.setdefault(item.location, []).append(item)
        return groups

    def history_for(self, sku: str) -> list[Change]:
        return [c for c in self.history if c.sku == sku]

    # -- mutation (the only mutable thing in the package) ----------------------
    def put(self, item: Item, *, expect_new: bool = False) -> None:
        if expect_new and item.sku in self.items:
            raise DuplicateSKUError(item.sku)
        self.items[item.sku] = item

    def drop(self, sku: str) -> Item:
        try:
            return self.items.pop(sku)
        except KeyError:
            raise NotFoundError(sku) from None

    def record(self, change: Change) -> None:
        self.history.append(change)

    # -- serialization ---------------------------------------------------------
    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "items": [
                {
                    "sku": i.sku, "name": i.name, "quantity": i.quantity,
                    "unit_price_minor": i.unit_price.minor_units,
                    "currency": i.unit_price.currency,
                    "location": i.location, "tags": list(i.tags),
                    "updated": i.updated.isoformat(),
                }
                for i in sorted(self.items.values(), key=lambda i: i.sku)
            ],
            "history": [
                {"sku": c.sku, "action": c.action, "delta": c.delta,
                 "reason": c.reason, "at": c.at.isoformat(), "detail": c.detail}
                for c in self.history
            ],
        }

    @classmethod
    def from_dict(cls, data: Any) -> Store:
        if not isinstance(data, dict):
            raise DataFileError("data file must contain a JSON object")

        version = data.get("schema_version")
        if version is None:
            raise DataFileError("data file has no schema_version field")
        if version > SCHEMA_VERSION:
            raise DataFileError(
                f"data file is schema version {version}, but this build "
                f"understands up to {SCHEMA_VERSION}. Upgrade the tool."
            )

        store = cls()
        for raw in data.get("items", []):
            try:
                store.items[raw["sku"]] = Item(
                    sku=raw["sku"],
                    name=raw["name"],
                    quantity=int(raw["quantity"]),
                    unit_price=Money(int(raw["unit_price_minor"]),
                                     raw.get("currency", "USD")),
                    location=raw["location"],
                    tags=tuple(raw.get("tags", ())),
                    updated=datetime.fromisoformat(raw["updated"]),
                )
            except (KeyError, TypeError, ValueError) as exc:
                raise DataFileError(f"malformed item record: {exc}") from exc

        for raw in data.get("history", []):
            try:
                store.history.append(Change(
                    sku=raw["sku"], action=raw["action"], delta=int(raw["delta"]),
                    reason=raw["reason"], at=datetime.fromisoformat(raw["at"]),
                    detail=raw.get("detail", ""),
                ))
            except (KeyError, TypeError, ValueError) as exc:
                raise DataFileError(f"malformed history record: {exc}") from exc

        return store

    # -- file I/O --------------------------------------------------------------
    @classmethod
    def load(cls, path: Path) -> Store:
        if not path.exists():
            return cls()                      # an absent file means empty, not
                                              # an error -- first run must work
        try:
            raw = path.read_text(encoding="utf-8")
        except IsADirectoryError as exc:
            raise DataFileError(f"{path} is a directory, not a file") from exc
        except PermissionError as exc:
            raise DataFileError(f"{path} is not readable") from exc
        except OSError as exc:
            raise DataFileError(f"cannot read {path}: {exc}") from exc

        if not raw.strip():
            return cls()                      # empty file means empty store

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise DataFileError(
                f"{path} is not valid JSON (line {exc.lineno}, column "
                f"{exc.colno}): {exc.msg}"
            ) from exc

        return cls.from_dict(data)

    def save(self, path: Path) -> None:
        """Atomic write.

        Write to a temp file in the SAME DIRECTORY, then rename over the target.
        os.replace is atomic within a filesystem, so at every instant the target
        path names either the complete old file or the complete new one -- never
        a truncated one. A kill -9 at any point loses the new data, never the
        old.

        The temp file must be in the same directory. Writing it to /tmp and
        renaming across a mount point is a copy, not a rename, and is not
        atomic.

        This protects against a CRASH. It does NOT protect against two
        concurrent writers: the second save still overwrites the first
        entirely. Concurrency needs locking, which is a different problem
        (see the extensions).
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_name(path.name + ".tmp")
        try:
            tmp.write_text(
                json.dumps(self.to_dict(), indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            tmp.replace(path)
        except OSError as exc:
            tmp.unlink(missing_ok=True)
            raise DataFileError(f"cannot write {path}: {exc}") from exc
