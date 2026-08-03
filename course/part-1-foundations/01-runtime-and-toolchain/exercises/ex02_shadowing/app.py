"""Entry point. Run me:  python app.py"""

from __future__ import annotations

import random

import stats


def main() -> int:
    readings = [random.randint(1, 100) for _ in range(20)]
    print(f"readings: {readings}")
    print(f"mean:     {stats.mean(readings):.2f}")
    print(f"spread:   {stats.spread_of(readings):.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
