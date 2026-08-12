"""Exercise 10.3 — The same plugin system, three ways.

Build a text-transformation plugin system as (a) an ABC hierarchy,
(b) a Protocol, and (c) plain duck typing. Then compare them against five
concrete pressures.

Run:  python ex03_protocols.py
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

# --- the third-party class you do NOT control ---------------------------------
class VendorSlugifier:
    """Pretend this comes from a library you cannot modify. Note it already has
    exactly the right method -- it just has never heard of you."""

    def transform(self, text: str) -> str:
        return text.lower().replace(" ", "-")


# TODO 1: the ABC version ------------------------------------------------------
class TransformABC(ABC):
    """Abstract `transform`, plus a concrete `apply_twice` helper."""


# TODO 2: the Protocol version -------------------------------------------------
class TransformProto(Protocol):
    """Structural. Implementations do not import this."""


# TODO 3: three implementations ------------------------------------------------
# Write Upper, Reverse and Repeat as ABC subclasses AND as standalone classes
# that satisfy the Protocol without inheriting anything.


# TODO 4: the pipeline ---------------------------------------------------------
def run_pipeline(text: str, steps: list) -> str:  # type: ignore[type-arg]
    """Apply every step in order. Type the `steps` parameter three ways and see
    which the type checker accepts."""
    raise NotImplementedError


# TODO 5: the five pressures ---------------------------------------------------
# Answer each with a demonstration, not just prose.
#
# P1 THIRD-PARTY TYPE. Make VendorSlugifier work in your pipeline. How much code
#    does each of the three approaches need? (This is the decisive one.)
#
# P2 MISSING METHOD. Define a class that forgets `transform`. When is the error
#    reported for each approach -- at class definition, at instantiation, at
#    pipeline construction, or at call time? Which is most useful?
#
# P3 WRONG SIGNATURE. Define transform(self, text, extra) with a required extra
#    argument. Which approach catches it, and when? Try
#    isinstance(x, TransformProto) with @runtime_checkable and note what it
#    misses -- this is the limitation you must remember.
#
# P4 SHARED CODE. All three implementations want apply_twice(). Which approach
#    gives it to them for free, and what does the other pay?
#
# P5 TESTING. Write a fake transformer for a test. How much ceremony does each
#    approach require?


def verify() -> None:
    steps_abc = [Upper(), Reverse()]                 # type: ignore[name-defined]
    assert run_pipeline("abc", steps_abc) == "CBA"

    steps_proto = [UpperProto(), ReverseProto()]     # type: ignore[name-defined]
    assert run_pipeline("abc", steps_proto) == "CBA"

    steps_mixed = [UpperProto(), VendorSlugifier()]  # type: ignore[name-defined]
    assert run_pipeline("Hello World", steps_mixed) == "hello-world"

    print("all pipeline checks passed")


if __name__ == "__main__":
    verify()
