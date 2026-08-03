"""The exception hierarchy.

ONE base class, so that cli.py can write a single `except InventoryError` and
map everything to an exit code. Every error carries the data a caller needs to
build a message, rather than baking a formatted string into the raise site --
that separation is what lets --json emit structured errors.
"""

from __future__ import annotations


class InventoryError(Exception):
    """Base for everything this package raises deliberately.

    exit_code is an attribute on the exception rather than a lookup table in
    cli.py, so that adding an error type cannot forget to add its code.
    """

    exit_code = 1

    def as_dict(self) -> dict[str, object]:
        return {"error": type(self).__name__, "message": str(self)}


class ValidationError(InventoryError):
    """Input violated a rule of the domain."""

    exit_code = 2

    def __init__(self, field: str, value: object, reason: str) -> None:
        super().__init__(f"invalid {field}: {value!r} -- {reason}")
        self.field = field
        self.value = value
        self.reason = reason

    def as_dict(self) -> dict[str, object]:
        return {**super().as_dict(), "field": self.field,
                "value": repr(self.value), "reason": self.reason}


class NotFoundError(InventoryError):
    def __init__(self, sku: str) -> None:
        super().__init__(f"no item with SKU {sku!r}")
        self.sku = sku


class DuplicateSKUError(InventoryError):
    def __init__(self, sku: str) -> None:
        super().__init__(f"SKU {sku!r} already exists")
        self.sku = sku


class InsufficientStockError(InventoryError):
    def __init__(self, sku: str, requested: int, available: int) -> None:
        super().__init__(
            f"cannot take {requested} of {sku!r}: only {available} available"
        )
        self.sku = sku
        self.requested = requested
        self.available = available


class DataFileError(InventoryError):
    """The data file is missing, unreadable, corrupt, or from a future version.

    Its own exit code, because a script's response to "bad data file" is
    different from its response to "that SKU does not exist".
    """

    exit_code = 3
