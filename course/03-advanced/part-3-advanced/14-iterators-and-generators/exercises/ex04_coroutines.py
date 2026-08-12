"""Exercise 14.4 — Generators that receive.

Run:  python ex04_coroutines.py
"""
from __future__ import annotations

from collections.abc import Callable, Generator, Iterator
from typing import Any


# TODO 1 -----------------------------------------------------------------------
def running_stats() -> Generator[dict[str, float], float, None]:
    """A coroutine that receives numbers and yields running statistics.

        s = running_stats(); next(s)
        s.send(10)  -> {"count": 1, "mean": 10.0, "min": 10, "max": 10, ...}

    Include a running standard deviation using Welford's algorithm -- computing
    it from a stored list defeats the point, which is CONSTANT memory over an
    unbounded stream.
    """
    raise NotImplementedError


# TODO 2 -----------------------------------------------------------------------
def prime(fn: Callable[..., Generator]) -> Callable[..., Generator]:  # type: ignore[type-arg]
    """A decorator that calls next() on a new coroutine automatically.

    Forgetting to prime gives 'TypeError: can't send non-None value to a
    just-started generator', which is confusing the first three times. This
    decorator is the standard fix, and it is a preview of Module 15.
    """
    raise NotImplementedError


# TODO 3 -----------------------------------------------------------------------
def broadcast(*targets: Generator[Any, Any, None]) -> Generator[None, Any, None]:
    """Fan out: everything sent here is forwarded to every target coroutine.

    Requirements:
      - a target that raises must not stop the others
      - close() must close every target
      - the first target must not be able to modify what the second receives
    """
    raise NotImplementedError


# TODO 4 -----------------------------------------------------------------------
def my_contextmanager(fn):  # type: ignore[no-untyped-def]
    """Implement contextlib.contextmanager from scratch.

    The whole mechanism, and it is a genuinely beautiful piece of design:
      __enter__  = next(gen), returning the yielded value
      __exit__   = gen.throw(exc) if the block raised, else next(gen)
                   and StopIteration means the generator finished normally

    Handle correctly:
      - the block raising -> throw INTO the generator so its finally runs
      - the generator suppressing the exception (yield inside try/except that
        does not re-raise) -> __exit__ returns True
      - the generator yielding twice -> RuntimeError("generator didn't stop")
      - the generator not yielding at all -> RuntimeError

    Then answer: why must __exit__ use throw() rather than simply calling
    next()? What would a `finally` in the generator do in each case?
    """
    raise NotImplementedError


def verify() -> None:
    s = running_stats()
    next(s)
    s.send(10)
    result = s.send(20)
    assert result["count"] == 2 and result["mean"] == 15.0
    assert result["min"] == 10 and result["max"] == 20

    @prime
    def collector() -> Generator[list[Any], Any, None]:
        items: list[Any] = []
        while True:
            items.append((yield items))

    c = collector()
    assert c.send("a") == ["a"]            # no manual next() needed

    seen_a: list[Any] = []
    seen_b: list[Any] = []

    @prime
    def recorder(into: list[Any]) -> Generator[None, Any, None]:
        while True:
            into.append((yield))

    @prime
    def exploder() -> Generator[None, Any, None]:
        while True:
            yield
            raise RuntimeError("bad target")

    b = broadcast(recorder(seen_a), exploder(), recorder(seen_b))
    b.send("x")
    b.send("y")
    assert seen_a == ["x", "y"], seen_a
    assert seen_b == ["x", "y"], "a raising target broke the broadcast"

    log: list[str] = []

    @my_contextmanager
    def managed(name: str):  # type: ignore[no-untyped-def]
        log.append(f"enter {name}")
        try:
            yield name.upper()
        finally:
            log.append(f"exit {name}")

    with managed("db") as handle:
        assert handle == "DB"
        log.append("body")
    assert log == ["enter db", "body", "exit db"], log

    log.clear()
    try:
        with managed("db"):
            raise ValueError("boom")
    except ValueError:
        pass
    assert log == ["enter db", "exit db"], "finally must run on an exception"

    print("all coroutine checks passed")


if __name__ == "__main__":
    verify()
