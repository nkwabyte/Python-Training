from __future__ import annotations

import pytest

from inventory import (
    DuplicateSKUError,
    InsufficientStockError,
    NotFoundError,
    Store,
    ValidationError,
)
from inventory.operations import add_item, adjust, filtered, move, remove_item, search


class TestAdd:
    def test_adds_and_records_history(self, empty_store: Store) -> None:
        item, change = add_item(empty_store, "SKU-9", "New", quantity=3,
                                price="1.50", location="C1")
        assert empty_store.get("SKU-9") is item
        assert change.delta == 3
        assert empty_store.history[-1] is change

    def test_duplicate_sku(self, store: Store) -> None:
        with pytest.raises(DuplicateSKUError):
            add_item(store, "SKU-001", "Dup", quantity=1, price="1.00",
                     location="A1")


class TestAdjust:
    def test_increases(self, store: Store) -> None:
        item, _ = adjust(store, "SKU-001", +10, "restock")
        assert item.quantity == 50

    def test_decreases(self, store: Store) -> None:
        item, _ = adjust(store, "SKU-001", -5, "damaged")
        assert item.quantity == 35

    def test_cannot_go_negative(self, store: Store) -> None:
        with pytest.raises(InsufficientStockError) as exc:
            adjust(store, "SKU-002", -10, "oops")
        assert exc.value.available == 5

    def test_reason_is_mandatory(self, store: Store) -> None:
        with pytest.raises(ValidationError, match="reason"):
            adjust(store, "SKU-001", -1, "   ")

    def test_original_item_is_untouched(self, store: Store) -> None:
        """Immutability means the pre-change object is still valid and intact,
        which is what makes the history log trustworthy."""
        before = store.get("SKU-001")
        adjust(store, "SKU-001", -5, "damaged")
        assert before.quantity == 40


class TestMove:
    def test_full_move_changes_location(self, store: Store) -> None:
        items, changes = move(store, "SKU-001", "C9")
        assert items[0].location == "C9"
        assert items[0].quantity == 40
        assert [c.delta for c in changes] == [-40, 40]

    def test_partial_move_leaves_remainder(self, store: Store) -> None:
        items, _ = move(store, "SKU-001", "C9", 10)
        assert items[0].quantity == 30
        assert items[0].location == "A1"

    def test_cannot_move_more_than_held(self, store: Store) -> None:
        with pytest.raises(InsufficientStockError):
            move(store, "SKU-002", "C9", 99)

    def test_cannot_move_to_same_location(self, store: Store) -> None:
        with pytest.raises(ValidationError):
            move(store, "SKU-001", "A1")

    def test_unknown_sku(self, store: Store) -> None:
        with pytest.raises(NotFoundError):
            move(store, "NOPE", "C9")


class TestRemove:
    def test_refuses_when_stock_remains(self, store: Store) -> None:
        with pytest.raises(ValidationError, match="still holds stock"):
            remove_item(store, "SKU-001")

    def test_allows_zero_quantity(self, store: Store) -> None:
        remove_item(store, "SKU-003")
        assert "SKU-003" not in store.items

    def test_force(self, store: Store) -> None:
        remove_item(store, "SKU-001", force=True)
        assert "SKU-001" not in store.items


class TestSearch:
    def test_case_insensitive(self, store: Store) -> None:
        assert [i.sku for i in search(store, "WIDGET")] == ["SKU-001"]

    def test_searches_tags(self, store: Store) -> None:
        assert {i.sku for i in search(store, "fast")} == {"SKU-001", "SKU-004"}

    def test_field_restriction(self, store: Store) -> None:
        assert search(store, "fast", fields=("name",)) == []

    def test_no_matches(self, store: Store) -> None:
        assert search(store, "zzzz") == []


class TestFilter:
    def test_location_prefix(self, store: Store) -> None:
        assert {i.sku for i in filtered(store, location_prefix="A")} == {
            "SKU-001", "SKU-002"}

    def test_quantity_range(self, store: Store) -> None:
        assert [i.sku for i in filtered(store, min_qty=1, max_qty=50)] == [
            "SKU-001", "SKU-002"]

    def test_sorting_and_limit(self, store: Store) -> None:
        top = filtered(store, sort_by="qty", descending=True, limit=2)
        assert [i.sku for i in top] == ["SKU-004", "SKU-001"]

    def test_bad_sort_key(self, store: Store) -> None:
        with pytest.raises(ValidationError, match="must be one of"):
            filtered(store, sort_by="colour")
