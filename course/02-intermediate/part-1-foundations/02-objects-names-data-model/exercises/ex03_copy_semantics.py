"""Exercise 02.3 — Copy semantics, three ways, with measurements.

You have a nested configuration structure. Users need to derive variants of it
without disturbing the original. There are three strategies. Implement all
three, then measure them, then argue for one.

Run:  python ex03_copy_semantics.py
"""

from __future__ import annotations

import copy
import timeit
from typing import Any

BASE_CONFIG: dict[str, Any] = {
    "service": "api",
    "port": 8080,
    "retries": 3,
    "database": {
        "host": "db.internal",
        "port": 5432,
        "pool": {"min": 2, "max": 10},
        "replicas": ["r1.internal", "r2.internal"],
    },
    "features": {"beta": False, "tracing": True},
    "allowed_origins": ["https://app.example.com"],
}


# TODO 1 -----------------------------------------------------------------------
def derive_shallow(base: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    """Shallow copy plus top-level overrides.

    Implement it, then answer in a docstring comment:
      - which mutations of the RESULT would corrupt BASE?
      - which would not?
      - is this ever the right choice? When?
    """
    raise NotImplementedError


# TODO 2 -----------------------------------------------------------------------
def derive_deep(base: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    """Full deep copy plus top-level overrides.

    Correct, and the obvious answer. Then answer:
      - what does deepcopy do if the structure contains an open file handle,
        a database connection, or a socket?
      - what does it do with a reference cycle?  (Try it. It handles it. How?)
    """
    raise NotImplementedError


# TODO 3 -----------------------------------------------------------------------
def derive_merge(base: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    """Recursive merge that never mutates either input and copies only what it
    must. Nested dicts merge key by key; lists and scalars are replaced.

        derive_merge(BASE, {"database": {"pool": {"max": 50}}})

    must produce a config where database.pool.min is still 2, database.host is
    unchanged, and BASE is untouched.

    This is what real configuration libraries do, and it is the strategy that
    scales.
    """
    raise NotImplementedError


# TODO 4 -----------------------------------------------------------------------
def freeze(value: Any) -> Any:
    """Return a deeply immutable version of a nested structure.

    dict  -> a frozen mapping (use types.MappingProxyType, and recurse)
    list  -> tuple (recursing into elements)
    set   -> frozenset
    other -> unchanged

    Then answer: MappingProxyType is a read-only VIEW. What does that mean for
    the underlying dict, and why is this weaker protection than it looks?
    """
    raise NotImplementedError


# TODO 5 -----------------------------------------------------------------------
def measure() -> None:
    """Time all three strategies over 10_000 iterations and print a table.

    Then answer:
      - what is the ratio between the cheapest and the most expensive?
      - at what call rate would that difference actually matter?
      - and therefore: is 'deepcopy is slow' a reason to avoid it here?
    """
    raise NotImplementedError


# --- verification -------------------------------------------------------------
def verify() -> None:
    snapshot = copy.deepcopy(BASE_CONFIG)

    merged = derive_merge(BASE_CONFIG, {"database": {"pool": {"max": 50}}})
    assert merged["database"]["pool"]["max"] == 50
    assert merged["database"]["pool"]["min"] == 2, "merge must not drop siblings"
    assert merged["database"]["host"] == "db.internal"
    assert BASE_CONFIG == snapshot, "derive_merge mutated its input"

    merged["database"]["replicas"].append("r3")
    assert BASE_CONFIG == snapshot, "result shares mutable state with the base"

    print("all checks passed")


if __name__ == "__main__":
    verify()
    measure()
