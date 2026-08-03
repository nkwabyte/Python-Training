"""Shared fixtures.

The most important thing here is that NO test can reach the real data file.
Every test gets a tmp_path and an explicit env dict.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from inventory import Store
from inventory.models import Item, Money

FIXED_NOW = datetime(2026, 8, 1, 12, 0, tzinfo=timezone.utc)


@pytest.fixture
def fixed_now() -> datetime:
    """A frozen clock, injected as a fixture.

    Note that FIXED_NOW is exposed as a FIXTURE rather than imported from
    conftest by other test modules. `from .conftest import FIXED_NOW` fails
    with "attempted relative import with no known parent package" when tests/
    is not a package -- exactly the Module 06 error. Fixtures are conftest's
    supported export mechanism; module-level constants are not.
    """
    return FIXED_NOW


@pytest.fixture
def empty_store() -> Store:
    return Store()


@pytest.fixture
def store() -> Store:
    s = Store()
    for sku, name, qty, price, loc, tags, age_days in [
        ("SKU-001", "Widget, blue", 40, "9.99", "A1", ("fast", "small"), 1),
        ("SKU-002", "Gizmo", 5, "24.50", "A2", ("slow",), 120),
        ("SKU-003", "Doohickey", 0, "1.00", "B1", (), 200),
        ("SKU-004", "Thingamajig", 250, "0.99", "B3", ("fast",), 3),
    ]:
        s.put(Item(sku, name, qty, Money.parse(price), loc, tags,
                   updated=FIXED_NOW - timedelta(days=age_days)))
    return s


@pytest.fixture
def data_file(tmp_path: Path) -> Path:
    return tmp_path / "inventory.json"


@pytest.fixture
def env(data_file: Path) -> dict[str, str]:
    """An env dict pointing at the temp file. Passed explicitly to main(), so
    os.environ is never touched and tests cannot interfere with each other."""
    return {"INVENTORY_FILE": str(data_file)}
