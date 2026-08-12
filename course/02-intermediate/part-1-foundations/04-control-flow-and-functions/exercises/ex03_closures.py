"""Exercise 04.3 — Four things built with closures only.

No classes. The constraint is the exercise: everything here can be done with a
class, and doing it with closures first is what makes decorators (Module 15)
feel like a natural next step rather than magic syntax.

Run:  python ex03_closures.py
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any


# TODO 1 -----------------------------------------------------------------------
def make_counter(start: int = 0, step: int = 1) -> tuple[Callable[[], int],
                                                          Callable[[], None]]:
    """Return (increment, reset).

    increment() adds step to the internal count and returns the NEW value.
    reset() sets it back to start.

    Both closures must share ONE count. That sharing is the whole point --
    write it, then inspect increment.__closure__ to see the cell they share.
    """
    raise NotImplementedError


# TODO 2 -----------------------------------------------------------------------
def memoize(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Return a wrapper that caches results by arguments.

    Requirements:
      - cache hits must not call fn again (prove it with a call counter)
      - keyword arguments must be part of the key
      - the wrapper must expose .cache_info() returning (hits, misses, size)
      - the wrapper must expose .cache_clear()

    Then answer, in a comment:
      - what happens if an argument is unhashable? What SHOULD happen?
      - f(1) and f(1.0) and f(True): same cache entry or different? Why?
      - why is caching a function with side effects a bug?

    functools.lru_cache does all this properly. Writing it once tells you what
    it is doing and when it is unsafe.
    """
    raise NotImplementedError


# TODO 3 -----------------------------------------------------------------------
def make_event_bus() -> tuple[Callable[[str, Callable[..., Any]], Callable[[], None]],
                              Callable[..., list[Any]]]:
    """Return (subscribe, emit).

    subscribe(event_name, handler) registers a handler and returns an
    UNSUBSCRIBE function -- a closure over the registration, so the caller does
    not need to hold an ID or pass the handler back.

    emit(event_name, *args) calls every handler for that event, in registration
    order, and returns their results.

    Requirements:
      - a handler that raises must not prevent later handlers from running
      - unsubscribing twice must be safe
      - unsubscribing during an emit must not corrupt the iteration
        (that last one is a real bug in many hand-rolled event systems --
         think about Module 02's "never mutate while iterating")
    """
    raise NotImplementedError


# TODO 4 -----------------------------------------------------------------------
def with_retry(
    attempts: int = 3,
    delay: float = 0.01,
    backoff: float = 2.0,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """A decorator FACTORY: with_retry(attempts=5) returns a decorator.

    Three nested functions. Getting this right is the whole skill that Module
    15 formalises:

        with_retry(...)  -> decorator  -> wrapper  -> the actual call

    Requirements:
      - retry only on the listed exception types; everything else propagates
        immediately
      - sleep `delay` after a failure, multiplying by `backoff` each time
      - after the last attempt, re-raise the LAST exception (not a new one)
      - the wrapper must keep the original function's __name__ and __doc__
        (do it by hand first, then look at functools.wraps and see that it is
         exactly what you just wrote)

    Then answer: why is retrying a non-idempotent operation dangerous, and what
    would you add to make it safe? (Module 33 answers this properly.)
    """
    raise NotImplementedError


# --- tests --------------------------------------------------------------------
def test_counter() -> None:
    inc, reset = make_counter(start=10, step=5)
    assert inc() == 15
    assert inc() == 20
    reset()
    assert inc() == 15

    a_inc, _ = make_counter()
    b_inc, _ = make_counter()
    a_inc()
    assert b_inc() == 1, "separate counters must not share a cell"


def test_memoize() -> None:
    calls = 0

    @memoize
    def slow(n: int, offset: int = 0) -> int:
        nonlocal calls
        calls += 1
        return n * 2 + offset

    assert slow(5) == 10
    assert slow(5) == 10
    assert calls == 1, "second call should have hit the cache"
    assert slow(5, offset=1) == 11
    assert calls == 2, "keyword arguments must be part of the key"

    hits, misses, size = slow.cache_info()
    assert (hits, misses, size) == (1, 2, 2), (hits, misses, size)
    slow.cache_clear()
    assert slow.cache_info()[2] == 0


def test_event_bus() -> None:
    subscribe, emit = make_event_bus()
    seen: list[str] = []

    un_a = subscribe("tick", lambda: seen.append("a"))
    subscribe("tick", lambda: seen.append("b"))

    def explodes() -> None:
        raise RuntimeError("handler failure")

    subscribe("tick", explodes)
    subscribe("tick", lambda: seen.append("c"))

    emit("tick")
    assert seen == ["a", "b", "c"], f"a raising handler broke the bus: {seen}"

    seen.clear()
    un_a()
    un_a()  # must be safe
    emit("tick")
    assert "a" not in seen

    emit("no-such-event")  # must not raise


def test_retry() -> None:
    attempts = 0

    @with_retry(attempts=3, delay=0.001)
    def flaky() -> str:
        """docstring preserved?"""
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ConnectionError("boom")
        return "ok"

    assert flaky() == "ok"
    assert attempts == 3
    assert flaky.__name__ == "flaky", "wrapper lost the function's name"
    assert flaky.__doc__ == "docstring preserved?"

    @with_retry(attempts=2, delay=0.001, exceptions=(ConnectionError,))
    def wrong_error() -> None:
        raise ValueError("not retryable")

    start = time.perf_counter()
    try:
        wrong_error()
    except ValueError:
        pass
    else:
        raise AssertionError("unlisted exceptions must propagate")
    assert time.perf_counter() - start < 0.05, "it retried something it should not"


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"  PASS  {t.__name__}")
    print(f"\n{len(tests)} tests passed")
