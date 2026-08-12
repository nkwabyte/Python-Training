"""Solution 04.3 — Four things built with closures only."""

from __future__ import annotations

import functools
import time
from collections.abc import Callable
from typing import Any


def make_counter(start: int = 0, step: int = 1) -> tuple[Callable[[], int],
                                                          Callable[[], None]]:
    """Two closures sharing ONE cell.

    Both inner functions declare `nonlocal count`, so both are bound to the
    same cell object in make_counter's frame. Inspect it:

        inc, reset = make_counter()
        inc.__closure__[0] is reset.__closure__[0]     # True (same cell)
        inc.__code__.co_freevars                        # ('count', 'step')

    Each CALL to make_counter creates a fresh frame and therefore fresh cells,
    which is why two counters are independent.
    """
    count = start

    def increment() -> int:
        nonlocal count
        count += step
        return count

    def reset() -> None:
        nonlocal count
        count = start

    return increment, reset


def memoize(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Hand-rolled lru_cache, so you know what the real one is doing.

    UNHASHABLE ARGUMENTS: building the key raises TypeError. That is the right
    behaviour -- it fails immediately and loudly at the call that cannot be
    cached, rather than silently skipping the cache (which hides a performance
    cliff) or stringifying the argument (which produces wrong cache hits for
    distinct objects with equal reprs). functools.lru_cache does the same.

    f(1) vs f(1.0) vs f(True): ONE cache entry, because 1 == 1.0 == True and
    all three hash equally (bool is a subclass of int, Module 03). If your
    function treats them differently, the cache will return the wrong answer.
    This is a genuine footgun in lru_cache too.

    CACHING SIDE EFFECTS: a cached call does not run the body, so the side
    effect happens only on the first call. Caching `def save(x)` means the
    second save silently does nothing. Cache pure functions only.
    """
    cache: dict[tuple[Any, ...], Any] = {}
    hits = 0
    misses = 0

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        nonlocal hits, misses
        # sorted() so that f(a=1, b=2) and f(b=2, a=1) share an entry.
        # The marker object separates positional from keyword parts so that
        # f(1) and f(x=1) cannot accidentally collide.
        key = (args, _KWMARK, *sorted(kwargs.items()))
        if key in cache:
            hits += 1
            return cache[key]
        misses += 1
        result = fn(*args, **kwargs)
        cache[key] = result
        return result

    def cache_info() -> tuple[int, int, int]:
        return (hits, misses, len(cache))

    def cache_clear() -> None:
        nonlocal hits, misses
        cache.clear()
        hits = misses = 0

    wrapper.cache_info = cache_info      # type: ignore[attr-defined]
    wrapper.cache_clear = cache_clear    # type: ignore[attr-defined]
    return wrapper


_KWMARK = object()


def make_event_bus() -> tuple[Callable[[str, Callable[..., Any]], Callable[[], None]],
                              Callable[..., list[Any]]]:
    """subscribe returns its own unsubscribe closure."""
    handlers: dict[str, list[Callable[..., Any]]] = {}

    def subscribe(event: str, handler: Callable[..., Any]) -> Callable[[], None]:
        handlers.setdefault(event, []).append(handler)

        def unsubscribe() -> None:
            # Idempotent: unsubscribing twice must not raise. The closure holds
            # `event` and `handler`, so the caller needs no token or ID.
            bucket = handlers.get(event, [])
            if handler in bucket:
                bucket.remove(handler)

        return unsubscribe

    def emit(event: str, *args: Any, **kwargs: Any) -> list[Any]:
        results: list[Any] = []
        # list(...) SNAPSHOTS the handlers before calling any of them. Without
        # it, a handler that unsubscribes itself (a very common pattern -- a
        # "once" listener) would mutate the list being iterated and silently
        # skip the next handler. This is Module 02's never-mutate-while-
        # iterating rule showing up in production code.
        for handler in list(handlers.get(event, [])):
            try:
                results.append(handler(*args, **kwargs))
            except Exception as exc:
                # One bad subscriber must not take down the bus. Real systems
                # log this; swallowing silently is only acceptable because the
                # exception is recorded in the results.
                results.append(exc)
        return results

    return subscribe, emit


def with_retry(
    attempts: int = 3,
    delay: float = 0.01,
    backoff: float = 2.0,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Three nested functions: factory -> decorator -> wrapper.

        with_retry(attempts=5)      returns `decorator`
        @decorator on foo           returns `wrapper`
        wrapper(...)                does the retrying and calls foo

    That three-level shape is exactly what Module 15 formalises. Once you have
    written it by hand, `@decorator_with_arguments` stops being mysterious.

    WHY RETRYING NON-IDEMPOTENT OPERATIONS IS DANGEROUS: if `charge_card()`
    times out, you do not know whether the charge happened. Retrying may charge
    twice. The fix is an IDEMPOTENCY KEY: the caller generates a unique ID per
    logical operation, the server records it, and a repeat with the same key
    returns the original result instead of acting again. Module 33 covers this
    properly. Retry logic without idempotency is a duplicate-side-effect
    generator.
    """
    if attempts < 1:
        raise ValueError("attempts must be at least 1")

    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(fn)          # copies __name__, __doc__, __module__,
        def wrapper(*args: Any, **kwargs: Any) -> Any:   # __qualname__, __dict__
            wait = delay
            last: BaseException | None = None
            for attempt in range(1, attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as exc:
                    last = exc
                    if attempt == attempts:
                        break
                    time.sleep(wait)
                    wait *= backoff
            assert last is not None
            raise last                # re-raise the LAST one, preserving its
                                      # traceback rather than wrapping it
        return wrapper

    return decorator


# --- the manual version of functools.wraps, for comparison --------------------
def manual_wraps(fn: Callable[..., Any], wrapper: Callable[..., Any]) -> None:
    """What functools.wraps does, written out.

    Without this, every decorated function in your codebase is called
    'wrapper', has no docstring, and confuses help(), pdb, Sphinx, and every
    introspection-based framework (including pytest's fixture resolution and
    FastAPI's signature inspection).
    """
    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__
    wrapper.__module__ = fn.__module__
    wrapper.__qualname__ = fn.__qualname__
    wrapper.__dict__.update(fn.__dict__)
    wrapper.__wrapped__ = fn          # type: ignore[attr-defined]
                                      # this is what inspect.signature follows


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

    assert "count" in inc.__code__.co_freevars


def test_memoize() -> None:
    calls = 0

    @memoize
    def slow(n: int, offset: int = 0) -> int:
        nonlocal calls
        calls += 1
        return n * 2 + offset

    assert slow(5) == 10
    assert slow(5) == 10
    assert calls == 1
    assert slow(5, offset=1) == 11
    assert calls == 2

    assert slow.cache_info() == (1, 2, 2), slow.cache_info()
    slow.cache_clear()
    assert slow.cache_info()[2] == 0
    assert slow.__name__ == "slow"


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
    un_a()
    emit("tick")
    assert "a" not in seen

    emit("no-such-event")

    # the self-unsubscribing handler: the snapshot in emit() is what saves us
    seen.clear()
    once_un: list[Callable[[], None]] = []

    def once() -> None:
        seen.append("once")
        once_un[0]()

    once_un.append(subscribe("boom", once))
    subscribe("boom", lambda: seen.append("after"))
    emit("boom")
    assert seen == ["once", "after"], f"iteration corrupted: {seen}"


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
    assert flaky.__name__ == "flaky"
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
    assert time.perf_counter() - start < 0.05

    @with_retry(attempts=2, delay=0.001)
    def always_fails() -> None:
        raise ConnectionError("permanent")

    try:
        always_fails()
    except ConnectionError as exc:
        assert str(exc) == "permanent", "must re-raise the original, not a wrapper"
    else:
        raise AssertionError("should have raised after exhausting attempts")


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"  PASS  {t.__name__}")
    print(f"\n{len(tests)} tests passed")
