"""Solution 04.2 — Six signatures, redesigned."""

from __future__ import annotations

import inspect
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any


# --- 1: booleans must be keyword-only -----------------------------------------
def resize(
    image: Any,
    width: int,
    height: int,
    /,                          # image, width, height are positional-only
    *,                          # everything after this is keyword-only
    keep_aspect: bool = True,
    upscale: bool = False,
    quality: int = 85,
) -> Any:
    """resize(img, 800, 600, keep_aspect=True) reads correctly at the call site.

    width and height are positional because their order is universally
    understood (it is width-then-height everywhere in computing). Everything
    else is keyword-only, because `resize(img, 800, 600, True, False, 90)`
    carries no information about which flag is which, and swapping two booleans
    produces silently wrong output rather than an error.

    RULE: any boolean parameter should be keyword-only. No exceptions.
    """
    return (image, width, height, keep_aspect, upscale, quality)


# --- 2: the mutable default ---------------------------------------------------
def add_tag(item: dict[str, Any], tag: str, tags: list[str] | None = None) -> list[str]:
    """`is None`, not `if not tags`.

    An explicitly passed empty list is falsy, so `if not tags: tags = []` would
    silently discard the caller's list and return a different object -- the
    caller's list would never receive the tag. The identity check distinguishes
    "not provided" from "provided and empty", which is Module 02's sentinel
    lesson in miniature.
    """
    if tags is None:
        tags = []
    tags.append(tag)
    return tags


# --- 3: ten parameters -> one options object ----------------------------------
@dataclass(frozen=True, slots=True)
class FetchOptions:
    """Frozen so it can be shared between call sites without aliasing risk.

    What this buys beyond tidiness:
      - one object to build once and reuse, instead of repeating nine keywords
      - options can be passed through layers without every layer re-declaring
        them (the "parameter drilling" problem)
      - adding an option does not change fetch()'s signature, so no caller
        breaks
      - the defaults live in one documented place a reader can find
      - it is testable and comparable: assert opts == expected
    """
    timeout: int = 30
    retries: int = 3
    backoff: float = 1.5
    verify_ssl: bool = True
    follow_redirects: bool = True
    max_redirects: int = 10
    headers: tuple[tuple[str, str], ...] = ()   # tuple, because frozen+hashable
    proxy: str | None = None
    user_agent: str | None = None


DEFAULT_FETCH = FetchOptions()


def fetch(url: str, options: FetchOptions = DEFAULT_FETCH) -> str:
    """A frozen dataclass IS a safe default value -- it cannot be mutated, so
    the Module 02 trap does not apply. That is a concrete, practical reason to
    prefer frozen dataclasses over dicts for configuration."""
    return url


# --- 4: mutually exclusive options -> separate functions ----------------------
def get_user_by_id(user_id: int) -> dict[str, Any]:
    return {"found": user_id}


def get_user_by_email(email: str) -> dict[str, Any]:
    return {"found": email}


def get_user_by_username(username: str) -> dict[str, Any]:
    return {"found": username}


# WHAT YOU GAINED:
#   - the "exactly one" constraint is now expressed in the type system, not in
#     a runtime check, so a wrong call is a type error rather than a ValueError
#   - each function has a real parameter type instead of `int | None`
#   - names at the call site say what is happening
#   - no runtime validation code to test
# WHAT YOU LOST:
#   - a caller that receives an already-tagged lookup ("by", value) at runtime
#     now needs its own dispatch. If that is a common case, add a thin
#     get_user(spec: UserLookup) taking a tagged union on top of the three.
#   - three names to remember instead of one.
# The trade is almost always worth it. "One function with mutually exclusive
# optional parameters" is a design smell with a name: it is a union type
# pretending to be a signature.


# --- 5: raising and non-raising pair ------------------------------------------
def parse_date(text: str, fmt: str = "%Y-%m-%d") -> date:
    """Raises ValueError on bad input. The default shape."""
    return datetime.strptime(text, fmt).date()


def parse_date_or_none(text: str, fmt: str = "%Y-%m-%d") -> date | None:
    """Returns None on bad input. For when invalid data is expected and normal."""
    try:
        return parse_date(text, fmt)
    except ValueError:
        return None


# The standard library models both shapes and names them consistently:
#   int("x")        raises          d["k"]        raises
#   d.get("k")      returns None    next(it, dflt) returns a default
# The rule: the RAISING version is the default and gets the plain name. The
# tolerant version gets a name that says so. Never make one function do both
# depending on a flag -- the return type then depends on an argument value,
# which no type checker can follow and every caller must re-derive.


# --- 6: full typing, sensible defaults ----------------------------------------
@dataclass(frozen=True, slots=True)
class Attachment:
    filename: str
    content: bytes
    mime_type: str = "application/octet-stream"


def send_email(
    to: Iterable[str],
    /,
    *,
    subject: str,
    body: str,
    cc: Iterable[str] = (),
    bcc: Iterable[str] = (),
    reply_to: str | None = None,
    attachments: Sequence[Attachment] = (),
    priority: int = 3,
    html: bool = False,
) -> dict[str, Any]:
    """Iterable for inputs we only walk once; Sequence for ones we may index.

    Empty TUPLE defaults, not empty list defaults: a tuple is immutable, so the
    mutable-default trap cannot occur. This is the cheapest possible fix for
    that whole category, and it costs nothing as long as the body does not
    mutate the argument -- which it should not anyway.

    `to` is positional-only because every mail API in existence puts the
    recipient first; everything else is keyword-only because a call like
    send_email(x, "hi", "body", None, None, [], 1, True) is unreadable.
    """
    return {
        "to": list(to), "subject": subject, "body": body,
        "cc": list(cc), "bcc": list(bcc), "reply_to": reply_to,
        "attachments": list(attachments), "priority": priority, "html": html,
    }


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
    assert add_tag({}, "b") == ["b"]
    given: list[str] = []
    assert add_tag({}, "c", given) is given


def test_fetch_takes_options_object() -> None:
    params = inspect.signature(fetch).parameters
    assert len(params) <= 3, f"still {len(params)} parameters"
    opts = FetchOptions(timeout=5)
    assert fetch("http://x", opts) == "http://x"
    try:
        opts.timeout = 10  # type: ignore[misc]
    except AttributeError:
        pass
    else:
        raise AssertionError("options should be frozen")


def test_get_user_is_three_functions() -> None:
    assert get_user_by_id(1) == {"found": 1}
    assert get_user_by_email("a@b") == {"found": "a@b"}
    assert get_user_by_username("ada") == {"found": "ada"}


def test_parse_date_pair() -> None:
    assert parse_date("2026-08-03") == date(2026, 8, 3)
    assert parse_date_or_none("nonsense") is None
    try:
        parse_date("nonsense")
    except ValueError:
        return
    raise AssertionError("parse_date must raise on bad input")


def test_send_email_is_typed() -> None:
    sig = inspect.signature(send_email)
    assert all(p.annotation is not inspect.Parameter.empty
               for p in sig.parameters.values())
    out = send_email(["a@b"], subject="hi", body="there")
    assert out["cc"] == []
    try:
        send_email(["a@b"], "hi", "there")  # type: ignore[misc]
    except TypeError:
        return
    raise AssertionError("subject and body must be keyword-only")


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"  PASS  {t.__name__}")
    print(f"\n{len(tests)} tests passed")
