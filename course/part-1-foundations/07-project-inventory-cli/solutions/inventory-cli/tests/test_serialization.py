from __future__ import annotations

import pytest

from inventory import DataFileError, Store
from inventory.models import Item, Money
from inventory.operations import filtered
from inventory.serialization import apply_import, plan_import, to_csv, to_json


def test_csv_round_trip(store: Store) -> None:
    """The single highest-value serialization test. Export, import into a fresh
    store, and compare. It catches quoting bugs, type-coercion bugs, and
    dropped fields all at once."""
    text = to_csv(filtered(store))
    fresh = Store()
    plan = plan_import(fresh, text)
    assert plan.ok, plan.errors
    apply_import(fresh, plan)

    for sku, original in store.items.items():
        copy = fresh.get(sku)
        assert (copy.name, copy.quantity, copy.unit_price, copy.location,
                copy.tags) == (original.name, original.quantity,
                               original.unit_price, original.location,
                               original.tags)


def test_names_containing_commas_and_quotes_survive() -> None:
    s = Store()
    s.put(Item("SKU-1", 'Widget, "blue", large', 1, Money.parse("1.00"), "A1"))
    fresh = Store()
    apply_import(fresh, plan_import(fresh, to_csv(filtered(s))))
    assert fresh.get("SKU-1").name == 'Widget, "blue", large'
    # This is why the csv module exists. str.split(",") fails this test, and
    # every hand-rolled CSV writer fails it the first time a product name has a
    # comma in it -- which is roughly week two of production.


def test_import_plan_is_pure(store: Store) -> None:
    before = dict(store.items)
    to_add = to_csv([Item("SKU-NEW", "New", 1, Money.parse("1.00"), "C1")])
    plan = plan_import(store, to_add)
    assert len(plan.to_add) == 1
    assert store.items == before, "planning must not mutate; --dry-run depends on it"


def test_import_detects_updates_and_unchanged(store: Store) -> None:
    text = to_csv(filtered(store))
    plan = plan_import(store, text)
    assert len(plan.unchanged) == len(store.items)
    assert not plan.to_add and not plan.to_update


def test_import_collects_errors_without_aborting() -> None:
    text = ("sku,name,quantity,unit_price,location,tags\n"
            "GOOD-1,Fine,1,1.00,A1,\n"
            "bad sku,Bad,1,1.00,A1,\n"
            "GOOD-2,Also fine,2,2.00,A2,\n"
            "GOOD-3,Negative,-5,1.00,A1,\n")
    plan = plan_import(Store(), text)
    assert len(plan.to_add) == 2
    assert len(plan.errors) == 2
    assert "line 3" in plan.errors[0]      # header is line 1, so row 2 is line 3
    assert not plan.ok


def test_apply_refuses_a_plan_with_errors() -> None:
    plan = plan_import(Store(), "sku,name,quantity,unit_price,location,tags\n"
                                "bad sku,X,1,1.00,A1,\n")
    with pytest.raises(DataFileError, match="refusing to import"):
        apply_import(Store(), plan)


def test_headerless_csv() -> None:
    with pytest.raises(DataFileError, match="no header row"):
        plan_import(Store(), "SKU-1,Widget,1,1.00,A1,\n")


def test_json_export_is_valid_json(store: Store) -> None:
    import json
    parsed = json.loads(to_json(filtered(store)))
    assert len(parsed) == len(store.items)
