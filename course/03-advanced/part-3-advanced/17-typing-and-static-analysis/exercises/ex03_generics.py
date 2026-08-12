"""Exercise 17.3 — Typed abstractions.

Run:  mypy --strict ex03_generics.py && python ex03_generics.py
"""
from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar

T = TypeVar("T")
E = TypeVar("E")
U = TypeVar("U")


# TODO 1 -----------------------------------------------------------------------
# Result[T, E] -- a value or an error, without exceptions.
#
#   Ok(42).map(str)                -> Ok("42")
#   Err("nope").map(str)           -> Err("nope")   (map is skipped)
#   Ok(42).unwrap()                -> 42
#   Err("nope").unwrap()           -> raises
#   Ok(42).unwrap_or(0)            -> 42
#   Ok(2).and_then(safe_divide)    -> chains, short-circuiting on the first Err
#
# Make mypy able to tell Ok from Err after a check -- that is the hard part.
# Look up how to make `if result.is_ok():` narrow the type, and note what it
# costs compared with exceptions.
#
# Then answer: Rust and Go use this style; Python has exceptions. When is
# Result better in Python, and when is it fighting the language?


# TODO 2 -----------------------------------------------------------------------
# A typed Pipeline: Pipeline[A] with .then(f: Callable[[A], B]) -> Pipeline[B]
#
#   Pipeline(5).then(str).then(len).value    # -> 1, and mypy knows it is an int
#
# The type must change as it flows. Getting mypy to track that through three
# stages is the exercise.


# TODO 3 -----------------------------------------------------------------------
# A generic Repository Protocol:
#
#   class Repository(Protocol[T]):
#       def get(self, id: str) -> T | None: ...
#       def save(self, entity: T) -> None: ...
#       def all(self) -> Iterable[T]: ...
#
# Write InMemoryRepository[T] satisfying it, and a function that accepts any
# Repository[User] -- including one backed by a dict, and one backed by a fake.
#
# Then answer: should Protocol[T] be covariant, contravariant, or invariant
# here, and why? Try declaring it covariant and see what mypy says about save().


# TODO 4 -----------------------------------------------------------------------
# A bounded TypeVar: write `largest(items)` that works for anything supporting
# <, and rejects things that do not -- at CHECK time, not runtime.
#   largest([3, 1, 2])         -> 3
#   largest(["b", "a"])        -> "b"
#   largest([object(), object()])  -> mypy error
#
# Hint: you need a Protocol with __lt__, and the TypeVar bound to it. Note the
# subtlety in typing __lt__'s parameter -- and why the standard library's own
# SupportsRichComparison is defined the way it is.


def verify() -> None:
    ok: Result[int, str] = Ok(42)              # type: ignore[name-defined]
    err: Result[int, str] = Err("nope")        # type: ignore[name-defined]

    assert ok.unwrap() == 42
    assert err.unwrap_or(0) == 0
    assert ok.map(lambda x: x * 2).unwrap() == 84
    assert err.map(lambda x: x * 2).unwrap_or(-1) == -1

    def safe_div(x: int) -> Result[int, str]:  # type: ignore[name-defined]
        return Ok(100 // x) if x else Err("division by zero")  # type: ignore[name-defined]

    assert ok.and_then(safe_div).unwrap() == 2
    assert Ok(0).and_then(safe_div).unwrap_or(-1) == -1        # type: ignore[name-defined]

    assert Pipeline(5).then(str).then(len).value == 1          # type: ignore[name-defined]

    repo = InMemoryRepository[str]()                            # type: ignore[name-defined]
    repo.save("a")
    assert list(repo.all()) == ["a"]

    assert largest([3, 1, 2]) == 3                              # type: ignore[name-defined]
    assert largest(["b", "a"]) == "b"                           # type: ignore[name-defined]

    print("all generic checks passed (now run mypy --strict)")


if __name__ == "__main__":
    verify()
