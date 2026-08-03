"""Solution 02.3 — Copy semantics, three ways, with measurements."""

from __future__ import annotations

import copy
import timeit
from types import MappingProxyType
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


def derive_shallow(base: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    """Shallow copy plus top-level overrides.

    WHICH MUTATIONS CORRUPT THE BASE:
      result["port"] = 9999            -> safe. Rebinds a key in the new dict.
      result["database"]["port"] = 1   -> CORRUPTS. Same nested dict object.
      result["allowed_origins"].append -> CORRUPTS. Same list object.

    WHEN IS THIS RIGHT: when every value is immutable, or when you have a
    written guarantee that nobody mutates nested values. Both are fragile
    assumptions in a codebase with more than one author, which is why this is
    the strategy that produces the most surprising bugs of the three.
    """
    result = base.copy()
    result.update(overrides)
    return result


def derive_deep(base: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    """Full deep copy plus top-level overrides. Correct and obvious.

    NON-COPYABLE CONTENTS: deepcopy recurses through everything reachable. If
    the structure holds a socket, an open file, a thread lock, or a database
    connection, deepcopy will either raise TypeError ("cannot pickle") or -- far
    worse -- produce a broken duplicate that looks fine until it is used. Some
    objects define __deepcopy__ to return self for exactly this reason.

    CYCLES: deepcopy handles them. It keeps a memo dict keyed by id() of every
    object already copied, so a cycle resolves to a reference to the copy it
    already made rather than infinite recursion. You can watch this by passing
    your own memo dict as the second argument and inspecting it afterwards.
    """
    result = copy.deepcopy(base)
    result.update(overrides)
    return result


def derive_merge(base: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    """Recursive merge. Copies only what it must; mutates neither input.

    This is what real config systems do (Kubernetes strategic merge, Helm
    values, pydantic-settings, Django settings layering). It scales because the
    caller expresses only the delta, and because untouched subtrees are cheap.
    """
    result: dict[str, Any] = {}
    for key, value in base.items():
        if key in overrides:
            override = overrides[key]
            if isinstance(value, dict) and isinstance(override, dict):
                result[key] = derive_merge(value, override)   # recurse
            elif isinstance(value, list):
                result[key] = list(override)                  # replace, but copy
            else:
                result[key] = override
        elif isinstance(value, dict):
            result[key] = derive_merge(value, {})             # copy the subtree
        elif isinstance(value, list):
            result[key] = list(value)
        else:
            result[key] = value                               # immutable: share
    # keys present only in the overrides
    for key, override in overrides.items():
        if key not in base:
            result[key] = copy.deepcopy(override)
    return result


def freeze(value: Any) -> Any:
    """Deeply immutable view of a nested structure.

    MappingProxyType IS A VIEW, NOT A SNAPSHOT. It forbids writes THROUGH the
    proxy, but the underlying dict is still writable by anyone who holds a
    reference to it, and those writes show up through the proxy immediately.

        d = {"a": 1}
        p = MappingProxyType(d)
        p["a"] = 2      # TypeError
        d["a"] = 2      # fine
        p["a"]          # 2  -- the proxy saw it

    So a proxy protects against ACCIDENT, not against an adversary or against a
    caller who kept the original. For real immutability, copy first
    (`MappingProxyType(dict(d))`) or use a frozen dataclass / tuple, which is
    what Module 11 recommends.
    """
    if isinstance(value, dict):
        return MappingProxyType({k: freeze(v) for k, v in value.items()})
    if isinstance(value, list):
        return tuple(freeze(v) for v in value)
    if isinstance(value, set):
        return frozenset(value)
    return value


def measure() -> None:
    n = 10_000
    results = {
        "shallow (copy + update)": timeit.timeit(
            lambda: derive_shallow(BASE_CONFIG, port=9000), number=n
        ),
        "deepcopy": timeit.timeit(
            lambda: derive_deep(BASE_CONFIG, port=9000), number=n
        ),
        "recursive merge": timeit.timeit(
            lambda: derive_merge(BASE_CONFIG, {"port": 9000}), number=n
        ),
        "freeze": timeit.timeit(lambda: freeze(BASE_CONFIG), number=n),
    }
    fastest = min(results.values())
    print(f"\n{n:,} iterations")
    print(f"{'strategy':<26} {'total (s)':>10} {'per call':>12} {'relative':>10}")
    print("-" * 62)
    for name, total in results.items():
        print(
            f"{name:<26} {total:>10.4f} {total / n * 1e6:>10.2f}us "
            f"{total / fastest:>9.1f}x"
        )

    print(
        "\nInterpretation:\n"
        "  deepcopy is typically 20-60x the shallow copy on a structure this\n"
        "  size. In absolute terms that is single-digit microseconds. At 1000\n"
        "  requests per second, choosing deepcopy costs a few milliseconds of\n"
        "  CPU per second -- roughly 0.3 percent of one core.\n\n"
        "  So 'deepcopy is slow' is TRUE as a ratio and IRRELEVANT as a cost,\n"
        "  at this size, at this call rate. It becomes relevant when the\n"
        "  structure is large (megabytes), when it is deeply recursive, or when\n"
        "  it is on a per-item path in a tight loop rather than a per-request\n"
        "  path. Measure the thing you actually do, at the rate you actually do\n"
        "  it. This is the Module 23 lesson, arriving early."
    )


def verify() -> None:
    snapshot = copy.deepcopy(BASE_CONFIG)

    merged = derive_merge(BASE_CONFIG, {"database": {"pool": {"max": 50}}})
    assert merged["database"]["pool"]["max"] == 50
    assert merged["database"]["pool"]["min"] == 2, "merge must not drop siblings"
    assert merged["database"]["host"] == "db.internal"
    assert BASE_CONFIG == snapshot, "derive_merge mutated its input"

    merged["database"]["replicas"].append("r3")
    assert BASE_CONFIG == snapshot, "result shares mutable state with the base"

    # the shallow version demonstrates the bug it is meant to demonstrate
    shallow = derive_shallow(BASE_CONFIG, port=1)
    shallow["database"]["pool"]["max"] = 999
    assert BASE_CONFIG["database"]["pool"]["max"] == 999, "expected shallow leak"
    BASE_CONFIG["database"]["pool"]["max"] = 10  # repair for the timing run

    frozen = freeze(BASE_CONFIG)
    try:
        frozen["port"] = 1  # type: ignore[index]
    except TypeError:
        pass
    else:
        raise AssertionError("freeze() did not prevent writes")
    assert isinstance(frozen["allowed_origins"], tuple)

    print("all checks passed")


if __name__ == "__main__":
    verify()
    measure()
