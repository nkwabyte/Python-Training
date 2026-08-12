"""CLI tests.

Every one of these calls main(argv, env) directly. No subprocess, no
monkeypatching of sys.argv or os.environ. That is possible only because main
takes both as parameters -- which is the Module 01 and Module 06 lesson turned
into a design constraint.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from inventory.cli import EXIT_DATA, EXIT_FAILED, EXIT_OK, EXIT_USAGE, main


def run(argv: list[str], env: dict[str, str]) -> int:
    return main(argv, env)


class TestExitCodes:
    def test_success_is_zero(self, env: dict[str, str]) -> None:
        assert run(["list"], env) == EXIT_OK

    def test_usage_error_is_two(self, env: dict[str, str]) -> None:
        with pytest.raises(SystemExit) as exc:
            run(["nosuchcommand"], env)
        assert exc.value.code == EXIT_USAGE      # argparse exits 2 itself

    def test_validation_error_is_two(self, env: dict[str, str]) -> None:
        assert run(["add", "bad sku", "X", "--qty", "1", "--price", "1.00",
                    "--location", "A1"], env) == EXIT_USAGE

    def test_not_found_is_one(self, env: dict[str, str]) -> None:
        assert run(["history", "NOPE"], env) == EXIT_FAILED

    def test_corrupt_data_file_is_three(self, env: dict[str, str],
                                        data_file: Path) -> None:
        data_file.write_text("{ broken", encoding="utf-8")
        assert run(["list"], env) == EXIT_DATA

    def test_search_with_no_hits_is_one(self, env: dict[str, str]) -> None:
        run(["add", "SKU-1", "Widget", "--qty", "1", "--price", "1.00",
             "--location", "A1"], env)
        assert run(["search", "zzzz"], env) == EXIT_FAILED


class TestStreams:
    def test_data_goes_to_stdout_and_messages_to_stderr(
        self, env: dict[str, str], capsys: pytest.CaptureFixture[str]
    ) -> None:
        run(["add", "SKU-1", "Widget", "--qty", "5", "--price", "2.00",
             "--location", "A1"], env)
        captured = capsys.readouterr()
        assert captured.out == "", "add is not a data command; nothing on stdout"
        assert "added SKU-1" in captured.err

        run(["list"], env)
        captured = capsys.readouterr()
        assert "SKU-1" in captured.out, "list output must be pipeable"
        assert captured.err == ""

    def test_errors_never_reach_stdout(
        self, env: dict[str, str], capsys: pytest.CaptureFixture[str]
    ) -> None:
        run(["history", "NOPE"], env)
        captured = capsys.readouterr()
        assert captured.out == "", "an error corrupted the data stream"
        assert "error:" in captured.err


class TestJsonOutput:
    def test_list_json_is_parseable(
        self, env: dict[str, str], capsys: pytest.CaptureFixture[str]
    ) -> None:
        run(["add", "SKU-1", "Widget", "--qty", "5", "--price", "2.00",
             "--location", "A1"], env)
        capsys.readouterr()
        run(["--json", "list"], env)
        payload = json.loads(capsys.readouterr().out)
        assert payload[0]["sku"] == "SKU-1"

    def test_errors_are_structured_in_json_mode(
        self, env: dict[str, str], capsys: pytest.CaptureFixture[str]
    ) -> None:
        run(["--json", "history", "NOPE"], env)
        payload = json.loads(capsys.readouterr().err)
        assert payload["error"] == "NotFoundError"


class TestPersistence:
    def test_changes_survive_between_invocations(self, env: dict[str, str],
                                                  data_file: Path) -> None:
        run(["add", "SKU-1", "Widget", "--qty", "5", "--price", "2.00",
             "--location", "A1"], env)
        assert data_file.exists()
        run(["adjust", "SKU-1", "--delta", "-2", "--reason", "sold"], env)

        from inventory import Store
        assert Store.load(data_file).get("SKU-1").quantity == 3

    def test_read_commands_do_not_write(self, env: dict[str, str],
                                        data_file: Path) -> None:
        run(["add", "SKU-1", "Widget", "--qty", "5", "--price", "2.00",
             "--location", "A1"], env)
        before = data_file.stat().st_mtime_ns
        run(["list"], env)
        run(["report", "value"], env)
        assert data_file.stat().st_mtime_ns == before

    def test_failed_operation_does_not_write(self, env: dict[str, str],
                                             data_file: Path) -> None:
        run(["add", "SKU-1", "Widget", "--qty", "5", "--price", "2.00",
             "--location", "A1"], env)
        before = data_file.read_bytes()
        run(["adjust", "SKU-1", "--delta", "-99", "--reason", "oops"], env)
        assert data_file.read_bytes() == before


class TestFilePathResolution:
    def test_explicit_flag_beats_environment(self, tmp_path: Path,
                                             env: dict[str, str]) -> None:
        other = tmp_path / "other.json"
        run(["--file", str(other), "add", "SKU-1", "W", "--qty", "1",
             "--price", "1.00", "--location", "A1"], env)
        assert other.exists()
        assert not Path(env["INVENTORY_FILE"]).exists()

    def test_first_run_with_no_file_works(self, env: dict[str, str]) -> None:
        assert run(["list"], env) == EXIT_OK


class TestImportExport:
    def test_export_import_round_trip_reports_no_changes(
        self, env: dict[str, str], tmp_path: Path,
        capsys: pytest.CaptureFixture[str]
    ) -> None:
        for sku in ("SKU-1", "SKU-2"):
            run(["add", sku, f"Item {sku}", "--qty", "3", "--price", "1.50",
                 "--location", "A1"], env)
        capsys.readouterr()

        run(["export", "--format", "csv"], env)
        csv_text = capsys.readouterr().out
        exported = tmp_path / "out.csv"
        exported.write_text(csv_text, encoding="utf-8")

        run(["import", str(exported), "--dry-run"], env)
        assert "0 to add, 0 to update" in capsys.readouterr().err

    def test_dry_run_does_not_write(self, env: dict[str, str], tmp_path: Path,
                                    data_file: Path) -> None:
        run(["add", "SKU-1", "W", "--qty", "1", "--price", "1.00",
             "--location", "A1"], env)
        before = data_file.read_bytes()
        csv_path = tmp_path / "in.csv"
        csv_path.write_text(
            "sku,name,quantity,unit_price,location,tags\n"
            "SKU-2,New,9,2.00,B1,\n", encoding="utf-8")
        run(["import", str(csv_path), "--dry-run"], env)
        assert data_file.read_bytes() == before
