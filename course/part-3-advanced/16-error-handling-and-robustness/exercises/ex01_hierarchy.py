"""Exercise 16.1 — Twelve predictions about control flow.

Predict the exact output of each before running.

Run:  python ex01_hierarchy.py
"""
from __future__ import annotations


def q01() -> str:
    # PREDICTION:
    try:
        return "try"
    finally:
        print("    q01 finally ran")


def q02() -> str:
    # PREDICTION: which value is returned, and what happens to the exception?
    try:
        raise ValueError("boom")
    finally:
        return "finally wins"        # noqa: B012


def q03() -> None:
    # PREDICTION: does the else clause run?
    for label, value in [("present", {"k": 1}), ("absent", {})]:
        try:
            v = value["k"]
        except KeyError:
            print(f"    q03 {label}: caught")
        else:
            print(f"    q03 {label}: else ran, v={v}")
        finally:
            print(f"    q03 {label}: finally")


def q04() -> None:
    # PREDICTION: which handler catches, and why is that a bug?
    def process(v: int) -> None:
        raise KeyError("something ELSE went wrong deep inside process")

    data = {"k": 1}
    try:
        value = data["k"]
        process(value)
    except KeyError as exc:
        print(f"    q04 caught: {exc}")
        print("    q04 -> and the code now thinks the KEY was missing")


def q05() -> None:
    # PREDICTION: is the ValueError visible in the traceback? What connects them?
    try:
        try:
            raise ValueError("original")
        except ValueError:
            raise RuntimeError("replacement")
    except RuntimeError as exc:
        print(f"    q05 __context__: {exc.__context__}")
        print(f"    q05 __cause__:   {exc.__cause__}")


def q06() -> None:
    # PREDICTION: same question, with `from`.
    try:
        try:
            raise ValueError("original")
        except ValueError as inner:
            raise RuntimeError("replacement") from inner
    except RuntimeError as exc:
        print(f"    q06 __context__: {exc.__context__}")
        print(f"    q06 __cause__:   {exc.__cause__}")


def q07() -> None:
    # PREDICTION: what does `from None` leave behind?
    try:
        try:
            raise ValueError("original")
        except ValueError:
            raise RuntimeError("replacement") from None
    except RuntimeError as exc:
        print(f"    q07 __context__: {exc.__context__}")
        print(f"    q07 __cause__:   {exc.__cause__}")
        print(f"    q07 suppress:    {exc.__suppress_context__}")


def q08() -> None:
    # PREDICTION: is `exc` still bound after the except block?
    try:
        raise ValueError("boom")
    except ValueError as exc:
        message = str(exc)
    try:
        print(f"    q08 exc is {exc}")      # type: ignore[possibly-undefined]
    except NameError:
        print(f"    q08 NameError -- exc was deleted. message={message!r}")
    # Why does Python delete it? (Hint: what does a traceback reference?)


def q09() -> None:
    # PREDICTION: which of these does `except Exception` catch?
    import sys
    for exc_cls in (ValueError, KeyboardInterrupt, SystemExit, GeneratorExit):
        try:
            raise exc_cls("x")
        except Exception:
            print(f"    q09 {exc_cls.__name__:<18} caught by except Exception")
        except BaseException:
            print(f"    q09 {exc_cls.__name__:<18} NOT caught -- BaseException")


def q10() -> None:
    # PREDICTION: what order do the finallys run in?
    def inner() -> None:
        try:
            raise ValueError("deep")
        finally:
            print("    q10 inner finally")

    def middle() -> None:
        try:
            inner()
        finally:
            print("    q10 middle finally")

    try:
        middle()
    except ValueError:
        print("    q10 caught at the top")


def q11() -> None:
    # PREDICTION: what happens when the finally itself raises?
    try:
        try:
            raise ValueError("original")
        finally:
            raise RuntimeError("from finally")
    except Exception as exc:
        print(f"    q11 surfaced: {type(exc).__name__}: {exc}")
        print(f"    q11 the original is at __context__: {exc.__context__}")
    # Which one would a caller see in a traceback? Which one do they NEED?


def q12() -> None:
    # PREDICTION: how many times does the loop body run?
    attempts = 0
    for i in range(3):
        try:
            attempts += 1
            raise ConnectionError("transient")
        except ConnectionError:
            continue
        finally:
            print(f"    q12 finally on iteration {i}")
    print(f"    q12 attempts={attempts}")


if __name__ == "__main__":
    print("q01:", q01())
    print("q02:", q02())
    for fn in [q03, q04, q05, q06, q07, q08, q09, q10, q11, q12]:
        fn()
