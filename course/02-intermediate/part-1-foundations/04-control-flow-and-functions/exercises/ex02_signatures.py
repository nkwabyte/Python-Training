"""Exercise 04.2 — Six bad signatures.

Each function below has a signature problem: unreadable call sites, a trap, or
a design that will break callers when it changes. Redesign each one, then make
the tests pass.

The tests check the CALLING CONVENTION, not just the behaviour -- some calls
must be rejected. That is the point.

Run:  python ex02_signatures.py
"""

from __future__ import annotations

from typing import Any


# --- 1 -----------------------------------------------------------------------
def resize(image: Any, w: int, h: int, keep_aspect: bool, upscale: bool,
           quality: int) -> Any:
    """PROBLEM: resize(img, 800, 600, True, False, 90) is unreadable, and any
    caller who swaps two booleans gets silently wrong output.

    TODO: make w and h positional (they have an obvious order), and everything
    else keyword-only. Give sensible defaults.
    """
    return (image, w, h, keep_aspect, upscale, quality)


# --- 2 -----------------------------------------------------------------------
def add_tag(item: dict[str, Any], tag: str, tags: list[str] = []) -> list[str]:
    """PROBLEM: the classic mutable default.

    TODO: fix it, and make sure an explicitly passed EMPTY list is still used
    rather than replaced.
    """
    tags.append(tag)
    return tags


# --- 3 -----------------------------------------------------------------------
def fetch(url: str, timeout: int = 30, retries: int = 3, backoff: float = 1.5,
          verify_ssl: bool = True, follow_redirects: bool = True,
          max_redirects: int = 10, headers: dict[str, str] | None = None,
          proxy: str | None = None, user_agent: str | None = None) -> str:
    """PROBLEM: ten parameters. Every call site is a wall of keywords, and
    adding an eleventh option means touching this signature again.

    TODO: keep `url` as the only required parameter and group the rest into a
    single options object (a frozen dataclass is ideal -- Module 11 -- but a
    plain class or a TypedDict is acceptable now). Callers should be able to
    build one options object and reuse it.
    """
    return url


# --- 4 -----------------------------------------------------------------------
def get_user(user_id: int | None = None, email: str | None = None,
             username: str | None = None) -> dict[str, Any]:
    """PROBLEM: three optional parameters where EXACTLY ONE must be given. The
    signature does not say that, so the check has to happen at runtime and the
    type checker cannot help.

    TODO: split into three functions with unambiguous names. Note in a comment
    what you gained and what you lost.
    """
    provided = [p for p in (user_id, email, username) if p is not None]
    if len(provided) != 1:
        raise ValueError("give exactly one of user_id, email, username")
    return {"found": provided[0]}


# --- 5 -----------------------------------------------------------------------
def parse_date(text: str, fmt: str = "%Y-%m-%d") -> Any:
    """PROBLEM: returns a date on success and None on failure, so every caller
    must remember to check, and the type is `date | None` forever.

    TODO: offer BOTH shapes, the way the standard library does:
      parse_date(text)            -> raises ValueError on bad input
      parse_date_or_none(text)    -> returns None on bad input
    Name them so the behaviour is obvious at the call site. (int() and
    dict.get() are the models here.)
    """
    from datetime import datetime
    try:
        return datetime.strptime(text, fmt).date()
    except ValueError:
        return None


# --- 6 -----------------------------------------------------------------------
def send_email(to, subject, body, cc, bcc, reply_to, attachments, priority,
               html):  # type: ignore[no-untyped-def]
    """PROBLEM: no type hints, no defaults, everything positional and required.

    TODO: full hints, sensible defaults, keyword-only for everything after
    `to`, and use Iterable rather than list for the address parameters so
    callers can pass a generator or a tuple.
    """
    return locals()


# --- tests --------------------------------------------------------------------
def test_resize_rejects_positional_booleans() -> None:
    resize(object(), 800, 600, keep_aspect=True)
    try:
        resize(object(), 800, 600, True)  # type: ignore[misc]
    except TypeError:
        return
    raise AssertionError("booleans must be keyword-only")


def test_add_tag_has_no_shared_state() -> None:
    assert add_tag({}, "a") == ["a"]
    assert add_tag({}, "b") == ["b"], "state leaked between calls"
    given: list[str] = []
    assert add_tag({}, "c", given) is given, "an explicit list must be used"


def test_fetch_takes_options_object() -> None:
    import inspect
    params = inspect.signature(fetch).parameters
    assert len(params) <= 3, f"still {len(params)} parameters"


def test_get_user_is_three_functions() -> None:
    assert "get_user_by_id" in globals(), "split get_user into named functions"
    assert "get_user_by_email" in globals()


def test_parse_date_pair() -> None:
    assert "parse_date_or_none" in globals()
    assert parse_date_or_none("nonsense") is None  # type: ignore[name-defined]  # noqa: F821
    try:
        parse_date("nonsense")
    except ValueError:
        return
    raise AssertionError("parse_date must raise on bad input")


def test_send_email_is_typed() -> None:
    import inspect
    sig = inspect.signature(send_email)
    assert all(p.annotation is not inspect.Parameter.empty
               for p in sig.parameters.values()), "add type hints"


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
        except Exception as exc:
            failed += 1
            print(f"  FAIL  {t.__name__}: {type(exc).__name__}: {exc}")
    print(f"\n{len(tests) - failed}/{len(tests)} passing")
