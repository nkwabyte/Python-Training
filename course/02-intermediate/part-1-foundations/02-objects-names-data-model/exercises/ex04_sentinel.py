"""Exercise 02.4 — Sentinels, or: when None is a real value.

The problem: you are writing a cache. Callers may legitimately store None as a
cached value ("we looked this up and the answer really is nothing"). You must
distinguish that from "not in the cache". None cannot do both jobs.

This is the canonical use of `is` beyond None-checking, and it appears
constantly in real APIs -- dict.get, argparse defaults, dataclass fields,
functools.lru_cache internals, and every ORM you will ever use.

Run:  python ex04_sentinel.py
"""

from __future__ import annotations

from typing import Any

# TODO 1 -----------------------------------------------------------------------
# Create a module-level sentinel. Three options, in increasing quality:
#   MISSING = object()
#   MISSING = "__missing__"                      # bad: a caller could pass it
#   class _Missing:  ...  ; MISSING = _Missing() # best: reprs nicely, typeable
# Pick one and justify it in a comment. Give it a __repr__ if you take option 3
# -- a sentinel that prints as <object object at 0x7f...> in a traceback is a
# small cruelty to your future self.


class Cache:
    """A cache where None is a storable value."""

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}

    # TODO 2: get(key, default=<sentinel>)
    #   - key present            -> return the stored value, even if it is None
    #   - key absent, no default -> raise KeyError
    #   - key absent, default    -> return the default, even if it is None
    def get(self, key: str, default: Any = None) -> Any:
        raise NotImplementedError

    # TODO 3: set(key, value)
    def set(self, key: str, value: Any) -> None:
        raise NotImplementedError

    # TODO 4: has(key) -- without using `in` on the dict, to prove you can
    def has(self, key: str) -> bool:
        raise NotImplementedError


# TODO 5 -----------------------------------------------------------------------
def update_user(
    user_id: int,
    name: Any = None,
    email: Any = None,
    nickname: Any = None,
) -> dict[str, Any]:
    """Build a partial update payload.

    The API distinguishes three intents, and your signature must too:
      - argument not passed       -> leave the field alone
      - argument passed as None   -> CLEAR the field (set it to null)
      - argument passed as a value-> set the field

    With None as the default this is impossible. Fix the signature using your
    sentinel, and return a dict containing only the fields the caller actually
    mentioned, with None preserved where the caller passed it explicitly.

    This exact problem is why PATCH endpoints are harder than PUT endpoints,
    and you will meet it again in Module 28.
    """
    raise NotImplementedError


def verify() -> None:
    c = Cache()

    c.set("a", 1)
    c.set("b", None)

    assert c.get("a") == 1
    assert c.get("b") is None
    assert c.has("b") is True
    assert c.has("zzz") is False
    assert c.get("zzz", "fallback") == "fallback"
    assert c.get("zzz", None) is None

    try:
        c.get("zzz")
    except KeyError:
        pass
    else:
        raise AssertionError("absent key with no default must raise KeyError")

    payload = update_user(1, name="Ada", nickname=None)
    assert payload == {"name": "Ada", "nickname": None}, payload
    assert "email" not in payload, "unmentioned fields must not appear"

    print("all checks passed")


if __name__ == "__main__":
    verify()
