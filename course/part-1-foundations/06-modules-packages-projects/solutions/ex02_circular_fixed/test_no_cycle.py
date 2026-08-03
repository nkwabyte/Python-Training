"""The regression test: importing any module first, in a FRESH interpreter,
must work.

A cycle often survives in the test suite because some earlier test already
imported the modules in the lucky order and left them in sys.modules. Only a
fresh subprocess proves the cycle is gone. This test has caught reintroduced
cycles in real codebases more than once.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

MODULES = ["shop.models", "shop.pricing", "shop.main"]


def test_every_module_imports_first() -> None:
    root = Path(__file__).parent
    for module in MODULES:
        result = subprocess.run(
            [sys.executable, "-c", f"import {module}"],
            cwd=root, capture_output=True, text=True, check=False,
        )
        assert result.returncode == 0, (
            f"importing {module} first failed:\n{result.stderr}"
        )
    print(f"  PASS  all {len(MODULES)} modules import cleanly in isolation")


def test_behaviour_unchanged() -> None:
    sys.path.insert(0, str(Path(__file__).parent))
    from shop.models import Customer, Order

    c = Customer("Ada", tier="gold")
    o = Order(c, [("widget", 3, 9.99), ("gizmo", 1, 24.50)])
    c.place(o)
    expected = round((3 * 9.99 + 24.50) * 0.95 * 1.20, 2)
    assert o.total() == expected, (o.total(), expected)
    print("  PASS  pricing behaviour preserved")


if __name__ == "__main__":
    test_every_module_imports_first()
    test_behaviour_unchanged()
