"""Exercise 15.2 — Stacking order puzzles.

Ten cases. Predict the output BEFORE running. Case 7 is the one that matters:
it runs without error and silently disables authentication.

Run:  python ex02_order.py
"""

from __future__ import annotations

import functools
from typing import Any, Callable

TRACE: list[str] = []


def make(label: str) -> Callable[[Callable], Callable]:  # type: ignore[type-arg]
    """A decorator that records when it WRAPS and when it CALLS."""
    def decorator(fn: Callable) -> Callable:  # type: ignore[type-arg]
        TRACE.append(f"wrap:{label}")
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            TRACE.append(f"enter:{label}")
            result = fn(*args, **kwargs)
            TRACE.append(f"exit:{label}")
            return result
        return wrapper
    return decorator


def q01() -> None:
    # PREDICTION: what is in TRACE after DEFINITION, before any call?
    TRACE.clear()

    @make("a")
    @make("b")
    @make("c")
    def f() -> str:
        TRACE.append("body")
        return "done"

    print("q01 after definition:", TRACE.copy())
    TRACE.clear()
    f()
    print("q01 after call:      ", TRACE.copy())


def q02() -> None:
    # PREDICTION: how many times does "wrap:x" appear for three calls?
    TRACE.clear()

    @make("x")
    def g() -> None: ...

    g(); g(); g()
    print("q02:", [t for t in TRACE if t.startswith("wrap")])


def q03() -> None:
    # PREDICTION: does this even work? What is __name__?
    def no_wraps(fn):  # type: ignore[no-untyped-def]
        def wrapper(*a, **kw):  # type: ignore[no-untyped-def]
            return fn(*a, **kw)
        return wrapper

    @no_wraps
    def documented() -> None:
        """A docstring."""

    print("q03:", documented.__name__, repr(documented.__doc__))


def q04() -> None:
    # PREDICTION: what does inspect.signature report for each?
    import inspect

    def bare(fn):  # type: ignore[no-untyped-def]
        def wrapper(*a, **kw):  # type: ignore[no-untyped-def]
            return fn(*a, **kw)
        return wrapper

    def wrapped(fn):  # type: ignore[no-untyped-def]
        @functools.wraps(fn)
        def wrapper(*a, **kw):  # type: ignore[no-untyped-def]
            return fn(*a, **kw)
        return wrapper

    @bare
    def one(a: int, b: str = "x") -> None: ...

    @wrapped
    def two(a: int, b: str = "x") -> None: ...

    print("q04 bare:   ", inspect.signature(one))
    print("q04 wrapped:", inspect.signature(two))


def q05() -> None:
    # PREDICTION: what error, and why does the message not mention parentheses?
    def retry(attempts: int = 3):  # type: ignore[no-untyped-def]
        def decorator(fn):  # type: ignore[no-untyped-def]
            @functools.wraps(fn)
            def wrapper(*a, **kw):  # type: ignore[no-untyped-def]
                return fn(*a, **kw)
            return wrapper
        return decorator

    try:
        @retry                       # note: NO parentheses
        def flaky() -> str:
            return "ok"
        print("q05:", flaky())
    except Exception as exc:
        print("q05:", type(exc).__name__, exc)


def q06() -> None:
    # PREDICTION: does the cache see the log, or does the log see the cache?
    calls = {"real": 0, "logged": 0}

    def logging_deco(fn):  # type: ignore[no-untyped-def]
        @functools.wraps(fn)
        def wrapper(*a, **kw):  # type: ignore[no-untyped-def]
            calls["logged"] += 1
            return fn(*a, **kw)
        return wrapper

    @functools.cache
    @logging_deco
    def cached_outside(n: int) -> int:
        calls["real"] += 1
        return n * 2

    for _ in range(3):
        cached_outside(5)
    print("q06 cache outside log:", dict(calls))

    calls["real"] = calls["logged"] = 0

    @logging_deco
    @functools.cache
    def cache_inside(n: int) -> int:
        calls["real"] += 1
        return n * 2

    for _ in range(3):
        cache_inside(5)
    print("q06 log outside cache:", dict(calls))
    # Which order do you want for a metrics decorator? For an audit log?


def q07() -> None:
    # THE IMPORTANT ONE. Predict what each route registry ends up holding.
    routes: dict[str, Callable] = {}  # type: ignore[type-arg]

    def route(path: str):  # type: ignore[no-untyped-def]
        def register(fn):  # type: ignore[no-untyped-def]
            routes[path] = fn
            return fn
        return register

    def require_auth(fn):  # type: ignore[no-untyped-def]
        @functools.wraps(fn)
        def wrapper(user: str | None = None, *a, **kw):  # type: ignore[no-untyped-def]
            if user is None:
                raise PermissionError("not authenticated")
            return fn(user, *a, **kw)
        return wrapper

    @route("/right")
    @require_auth
    def right(user: str) -> str:
        return f"admin page for {user}"

    @require_auth
    @route("/wrong")
    def wrong(user: str) -> str:
        return f"admin page for {user}"

    for path in ("/right", "/wrong"):
        try:
            result = routes[path](None)          # an UNAUTHENTICATED request
            print(f"q07 {path}: SERVED -> {result!r}")
        except PermissionError as exc:
            print(f"q07 {path}: blocked ({exc})")
    # Note that BOTH definitions ran without error, and a smoke test calling
    # wrong("ada") would pass. Where would you catch this?


def q08() -> None:
    # PREDICTION: does the decorator see the method or the staticmethod object?
    def show_type(fn):  # type: ignore[no-untyped-def]
        print(f"q08 decorator received: {type(fn).__name__}")
        return fn

    class C:
        @show_type
        @staticmethod
        def inner_static() -> None: ...

        @staticmethod
        @show_type
        def outer_static() -> None: ...


def q09() -> None:
    # PREDICTION: what does each print?
    def add_attr(name: str, value: Any):  # type: ignore[no-untyped-def]
        def decorator(fn):  # type: ignore[no-untyped-def]
            @functools.wraps(fn)
            def wrapper(*a, **kw):  # type: ignore[no-untyped-def]
                return fn(*a, **kw)
            setattr(wrapper, name, value)
            return wrapper
        return decorator

    @add_attr("outer", 1)
    @add_attr("inner", 2)
    def f() -> None: ...

    print("q09:", getattr(f, "outer", "MISSING"), getattr(f, "inner", "MISSING"))
    # Why is one of them missing? What does functools.wraps do to __dict__?


def q10() -> None:
    # PREDICTION: how many entries does the cache have after these four calls?
    @functools.cache
    def f(n: Any) -> Any:
        return n

    f(1); f(1.0); f(True); f(n=1)
    print("q10 cache entries:", f.cache_info().currsize)


if __name__ == "__main__":
    for fn in [q01, q02, q03, q04, q05, q06, q07, q08, q09, q10]:
        fn()
