"""Warehouse inventory manager.

The public API. Everything a caller needs is re-exported here, so that
internals can be reorganised without breaking anyone (Module 06).

Note what is NOT here: no I/O, no configuration reads, no logging setup. This
module must be importable in under 100ms with no side effects, because every
consumer pays for whatever it does.
"""

from inventory.errors import (
    DataFileError,
    DuplicateSKUError,
    InsufficientStockError,
    InventoryError,
    NotFoundError,
    ValidationError,
)
from inventory.models import Change, Item, Money
from inventory.store import Store

__all__ = [
    "Change",
    "DataFileError",
    "DuplicateSKUError",
    "InsufficientStockError",
    "InventoryError",
    "Item",
    "Money",
    "NotFoundError",
    "Store",
    "ValidationError",
    "__version__",
]

__version__ = "1.0.0"
