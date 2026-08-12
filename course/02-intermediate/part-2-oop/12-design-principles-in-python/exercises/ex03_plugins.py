"""Exercise 12.3 — A plugin registry, four ways.

Build the same text-processing plugin system with four registration
mechanisms, then compare them against the pressures that actually decide the
choice.

Run:  python ex03_plugins.py
"""

from __future__ import annotations

from typing import Callable, Protocol


class Processor(Protocol):
    name: str
    def process(self, text: str) -> str: ...


# TODO 1: a manual dict -------------------------------------------------------
# REGISTRY_MANUAL: dict[str, Processor] built by explicit assignment in one
# place. Underrated: greppable, no import-order surprises, no mechanism.


# TODO 2: a decorator ---------------------------------------------------------
# @register("upper") above each function or class. Note that this registers at
# IMPORT time -- write down what happens if the module is never imported.


# TODO 3: __init_subclass__ ---------------------------------------------------
# class ProcessorBase with __init_subclass__ auto-registering every subclass.
# Include a way to opt out (an abstract intermediate class must not register).


# TODO 4: entry points --------------------------------------------------------
# You cannot fully demonstrate this without installing a package, so instead:
#   - write the pyproject.toml snippet that declares the entry point
#   - write the discovery code using importlib.metadata.entry_points()
#   - explain what this does that the other three cannot


# TODO 5: the comparison ------------------------------------------------------
# Fill in this table with a demonstration for each cell you can run:
#
#                        | manual | decorator | __init_subclass__ | entry points
#   third-party plugin   |        |           |                   |
#   needs importing      |        |           |                   |
#   discoverable list    |        |           |                   |
#   name collisions      |        |           |                   |
#   import order matters |        |           |                   |
#   testable in isolation|        |           |                   |
#
# Then answer the question that decides it in practice:
#
#   A user pip-installs `myapp-plugin-pdf`. It defines a processor. With each
#   of the four mechanisms, what must happen for your application to find it?
#   Which mechanisms make it possible at all?


def verify() -> None:
    for registry in (REGISTRY_MANUAL, REGISTRY_DECORATED,  # type: ignore[name-defined]
                     ProcessorBase.registry):              # type: ignore[name-defined]
        assert "upper" in registry, f"missing in {registry}"
        assert registry["upper"].process("abc") == "ABC"

    assert "abstract" not in ProcessorBase.registry, (      # type: ignore[name-defined]
        "an abstract intermediate class must not register itself"
    )
    print("all plugin registry checks passed")


if __name__ == "__main__":
    verify()
