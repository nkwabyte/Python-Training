from __future__ import annotations

from inventory import Store
from datetime import datetime

from inventory.reporting import dead_stock, low_stock, tag_counts, top_by_value, value_by


def test_low_stock_sorted_by_quantity(store: Store) -> None:
    rows = low_stock(store, threshold=10)
    assert [r.sku for r in rows] == ["SKU-003", "SKU-002"]


def test_low_stock_threshold(store: Store) -> None:
    assert len(low_stock(store, threshold=0)) == 1


def test_value_by_location(store: Store) -> None:
    rows = value_by(store, "location")
    by_group = {r.group: r for r in rows}
    assert str(by_group["A1"].value) == "$399.60"      # 40 * 9.99
    assert str(by_group["B3"].value) == "$247.50"      # 250 * 0.99


def test_value_by_tag_counts_items_once_per_tag(store: Store) -> None:
    rows = {r.group: r for r in value_by(store, "tag")}
    assert rows["fast"].items == 2
    assert "(untagged)" in rows


def test_dead_stock_uses_injected_now(store: Store, fixed_now: datetime) -> None:
    """`now` is a parameter, so this test needs no monkeypatching of the clock
    and cannot become flaky at midnight or across a DST boundary."""
    stale = dead_stock(store, days=90, now=fixed_now)
    assert [i.sku for i in stale] == ["SKU-002"]       # SKU-003 has zero stock


def test_dead_stock_with_a_short_window(store: Store, fixed_now: datetime) -> None:
    # SKU-001 is 1 day old (fresh); SKU-003 is old but has zero stock, and
    # dead stock means stock, so it is excluded. That leaves SKU-002 and SKU-004.
    assert [i.sku for i in dead_stock(store, days=2, now=fixed_now)] == [
        "SKU-002", "SKU-004"]


def test_top_by_value(store: Store) -> None:
    assert [i.sku for i in top_by_value(store, 2)] == ["SKU-001", "SKU-004"]


def test_tag_counts(store: Store) -> None:
    assert dict(tag_counts(store))["fast"] == 2
