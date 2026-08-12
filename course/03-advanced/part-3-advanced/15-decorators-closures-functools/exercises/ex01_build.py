"""Exercise 15.1 — Eight decorators, all wraps-correct.

Every one must preserve __name__, __doc__ and the inspectable signature. The
tests check that, not just the behaviour.

Run:  python ex01_build.py
"""
from __future__ import annotations

import functools
import inspect
import time
from collections.abc import Callable
from typing import Any

# TODO 1  @timed          -- record elapsed time on wrapper.last_elapsed
# TODO 2  @retry(...)     -- attempts, delay, backoff, exception types
# TODO 3  @validate       -- enforce the function's own annotations at runtime,
#                            with a message naming the parameter and both types
# TODO 4  @deprecated(...) -- warnings.warn(DeprecationWarning), once per call
#                            site, with the replacement named
# TODO 5  @rate_limited(n, per) -- token bucket; raise or sleep (make it an
#                            option), and say which default is safer and why
# TODO 6  @memo_ttl(seconds)   -- lru_cache with expiry. What must you store
#                            besides the value?
# TODO 7  @synchronized   -- a lock per decorated function (previews Module 21).
#                            Why per function and not one global lock?
# TODO 8  @typed_dispatch -- singledispatch that also works on methods, with a
#                            clear error when no handler matches
#
# For 3 and 8: use inspect.signature().bind() to map arguments to parameter
# names. Doing it by position breaks for keyword arguments, defaults, *args,
# and positional-only parameters -- try the naive version first and find out.


def verify() -> None:
    @timed                                          # type: ignore[name-defined]
    def slow(x: int) -> int:
        """Doubles x, slowly."""
        time.sleep(0.01)
        return x * 2

    assert slow(21) == 42
    assert slow.last_elapsed >= 0.01                # type: ignore[attr-defined]
    assert slow.__name__ == "slow"
    assert slow.__doc__ == "Doubles x, slowly."
    assert str(inspect.signature(slow)) == "(x: int) -> int", (
        "the signature must survive the wrapper"
    )

    attempts = {"n": 0}

    @retry(attempts=3, delay=0.001)                 # type: ignore[name-defined]
    def flaky() -> str:
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise ConnectionError("boom")
        return "ok"

    assert flaky() == "ok" and attempts["n"] == 3

    @validate                                       # type: ignore[name-defined]
    def add(a: int, b: int = 0) -> int:
        return a + b

    assert add(1, 2) == 3
    assert add(1, b=2) == 3, "keyword arguments must bind correctly"
    try:
        add("x", 2)                                 # type: ignore[arg-type]
    except TypeError as exc:
        assert "a" in str(exc) and "int" in str(exc), str(exc)
    else:
        raise AssertionError("validate must reject a wrong type")

    import warnings

    @deprecated("use add() instead")                # type: ignore[name-defined]
    def old_add(a: int, b: int) -> int:
        return a + b

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert old_add(1, 2) == 3
        assert len(caught) == 1
        assert issubclass(caught[0].category, DeprecationWarning)
        assert "add()" in str(caught[0].message)

    calls = {"n": 0}

    @memo_ttl(seconds=0.05)                         # type: ignore[name-defined]
    def cached(n: int) -> int:
        calls["n"] += 1
        return n * 2

    cached(1); cached(1)
    assert calls["n"] == 1, "second call should hit the cache"
    time.sleep(0.06)
    cached(1)
    assert calls["n"] == 2, "the entry should have expired"

    print("all decorator checks passed")


if __name__ == "__main__":
    verify()
