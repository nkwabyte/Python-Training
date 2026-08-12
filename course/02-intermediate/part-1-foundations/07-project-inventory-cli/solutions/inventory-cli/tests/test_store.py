from __future__ import annotations

import json
from pathlib import Path

import pytest

from inventory import DataFileError, NotFoundError, Store
from inventory.models import Item, Money


def test_round_trip(store: Store, data_file: Path) -> None:
    store.save(data_file)
    loaded = Store.load(data_file)
    assert loaded.items == store.items


def test_absent_file_is_an_empty_store(tmp_path: Path) -> None:
    assert Store.load(tmp_path / "nope.json").items == {}


def test_empty_file_is_an_empty_store(data_file: Path) -> None:
    data_file.write_text("", encoding="utf-8")
    assert Store.load(data_file).items == {}


def test_corrupt_json_gives_a_useful_message(data_file: Path) -> None:
    data_file.write_text("{not json", encoding="utf-8")
    with pytest.raises(DataFileError, match="not valid JSON"):
        Store.load(data_file)


def test_directory_instead_of_file(tmp_path: Path) -> None:
    d = tmp_path / "adir"
    d.mkdir()
    with pytest.raises(DataFileError):
        Store.load(d)


def test_future_schema_version_is_refused(data_file: Path) -> None:
    data_file.write_text(json.dumps({"schema_version": 99, "items": []}),
                         encoding="utf-8")
    with pytest.raises(DataFileError, match="Upgrade the tool"):
        Store.load(data_file)


def test_missing_schema_version_is_refused(data_file: Path) -> None:
    data_file.write_text(json.dumps({"items": []}), encoding="utf-8")
    with pytest.raises(DataFileError, match="schema_version"):
        Store.load(data_file)


def test_malformed_item_record(data_file: Path) -> None:
    data_file.write_text(json.dumps(
        {"schema_version": 1, "items": [{"sku": "X"}]}), encoding="utf-8")
    with pytest.raises(DataFileError, match="malformed item"):
        Store.load(data_file)


def test_save_is_atomic_under_failure(store: Store, data_file: Path,
                                      monkeypatch: pytest.MonkeyPatch) -> None:
    """The requirement N5 test, done for real.

    Save once successfully, then make serialization explode mid-save and try
    again. The original file must be byte-identical afterwards -- which is only
    true because we write to a temp file and rename, rather than opening the
    target for writing (which truncates it before a single byte is written).
    """
    store.save(data_file)
    original = data_file.read_bytes()

    def explode(*_a: object, **_k: object) -> str:
        raise OSError("disk full")

    monkeypatch.setattr("inventory.store.json.dumps", explode)
    with pytest.raises(DataFileError):
        store.save(data_file)

    assert data_file.read_bytes() == original, "the old data was damaged"
    assert not list(data_file.parent.glob("*.tmp")), "temp file left behind"


def test_unknown_sku(store: Store) -> None:
    with pytest.raises(NotFoundError, match="SKU-999"):
        store.get("SKU-999")


def test_unicode_survives_a_round_trip(data_file: Path) -> None:
    s = Store()
    s.put(Item("SKU-1", "Café ☕ 张伟", 1, Money.parse("1.00"), "A1"))
    s.save(data_file)
    assert Store.load(data_file).get("SKU-1").name == "Café ☕ 张伟"
