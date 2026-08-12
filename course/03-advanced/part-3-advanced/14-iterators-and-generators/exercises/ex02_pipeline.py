"""Exercise 14.2 — A pipeline over a file larger than you want in memory.

Generates a large log file, then processes it two ways and measures both.

Run:  python ex02_pipeline.py            (default ~50 MB)
      python ex02_pipeline.py --big      (~500 MB -- check your disk first)
"""

from __future__ import annotations

import random
import sys
import tempfile
import tracemalloc
from collections.abc import Iterable, Iterator
from itertools import islice
from pathlib import Path
from typing import Any

LEVELS = ["DEBUG"] * 60 + ["INFO"] * 30 + ["WARN"] * 8 + ["ERROR"] * 2
USERS = [f"u{i}" for i in range(500)]


def generate(path: Path, lines: int) -> None:
    rng = random.Random(0)
    with path.open("w", encoding="utf-8") as fh:
        for i in range(lines):
            fh.write(f"2026-08-{i % 28 + 1:02d}T12:00:00\t{rng.choice(LEVELS)}\t"
                     f"{rng.choice(USERS)}\trequest {i} completed in "
                     f"{rng.randrange(1, 5000)}ms\n")


# --- the eager version, for comparison ----------------------------------------
def eager_top_errors(path: Path, limit: int) -> list[str]:
    """Reads the WHOLE file into memory, then filters. Do not run this on
    --big unless you want to meet the OOM killer."""
    lines = path.read_text(encoding="utf-8").splitlines()
    records = [dict(zip(("ts", "level", "user", "msg"), line.split("\t")))
               for line in lines]
    errors = [r for r in records if r["level"] == "ERROR"]
    return [f"{r['ts']} {r['user']}: {r['msg']}" for r in errors[:limit]]


# TODO 1 -----------------------------------------------------------------------
def read_lines(path: Path) -> Iterator[str]:
    """Yield lines. Note the `with` trap from the README: this generator holds
    the file open for as long as it lives. Decide how to handle that and write
    down why."""
    raise NotImplementedError


# TODO 2 -----------------------------------------------------------------------
def parse(lines: Iterable[str]) -> Iterator[dict[str, str]]:
    """Parse tab-separated lines into dicts. Skip malformed lines rather than
    raising -- but COUNT them, because silently dropping data is how a
    pipeline lies to you. How will you return that count from a generator?
    (There are three answers. Pick one and say why.)"""
    raise NotImplementedError


# TODO 3 -----------------------------------------------------------------------
def only_level(records: Iterable[dict[str, str]], level: str) -> Iterator[dict[str, str]]:
    raise NotImplementedError


# TODO 4 -----------------------------------------------------------------------
def format_records(records: Iterable[dict[str, str]]) -> Iterator[str]:
    raise NotImplementedError


# TODO 5 -----------------------------------------------------------------------
def lazy_top_errors(path: Path, limit: int) -> list[str]:
    """Compose the four stages and take the first `limit` results."""
    raise NotImplementedError


# TODO 6 -----------------------------------------------------------------------
def measure(path: Path, limit: int = 10) -> None:
    """Run both versions under tracemalloc and print peak memory and time.

    Predict BEFORE running:
      - roughly what will the eager peak be, relative to the file size?
      - roughly what will the lazy peak be?
      - which is FASTER for limit=10, and why?
      - which is faster for limit=1_000_000 (more errors than exist)?
    That last pair is the interesting one -- laziness is not universally
    faster, and knowing when it is not is the point.
    """
    raise NotImplementedError


# TODO 7 -----------------------------------------------------------------------
def count_by_user(path: Path, level: str) -> dict[str, int]:
    """Count ERROR lines per user across the WHOLE file.

    This one CANNOT terminate early -- it must see every line. Does laziness
    still help? Measure it and explain the result. (Hint: what is resident at
    any moment, and how big is the result?)
    """
    raise NotImplementedError


# TODO 8 -----------------------------------------------------------------------
def busiest_hour(path: Path) -> tuple[str, int]:
    """Find the hour with the most log lines.

    Now a harder question: this needs a full pass AND a grouping. Write it two
    ways -- with a Counter, and with itertools.groupby -- and say why groupby
    is the wrong tool here even though it looks like a grouping problem.
    """
    raise NotImplementedError


def main() -> int:
    lines = 5_000_000 if "--big" in sys.argv else 500_000
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "app.log"
        print(f"generating {lines:,} lines...")
        generate(path, lines)
        size_mb = path.stat().st_size / 1_048_576
        print(f"  {size_mb:.1f} MB\n")

        measure(path)
        print()
        print("errors by user (top 5):",
              sorted(count_by_user(path, "ERROR").items(),
                     key=lambda kv: -kv[1])[:5])
        print("busiest hour:", busiest_hour(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
