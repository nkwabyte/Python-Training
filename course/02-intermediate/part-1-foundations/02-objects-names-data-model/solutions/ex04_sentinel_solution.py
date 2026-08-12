"""Solution 02.4 — Sentinels, or: when None is a real value."""

from __future__ import annotations

from typing import Any, Final


class _Missing:
    """A unique sentinel type.

    WHY THIS OVER `MISSING = object()`:
      - It reprs usefully. A bare object() shows up in tracebacks and debugger
        output as <object object at 0x7f3c...>, which tells a reader nothing.
      - It is nameable in type annotations, so a signature can say
        `default: T | _Missing = MISSING` and a type checker can narrow on it.
      - Making __bool__ False is a small kindness: `if default:` behaves
        sensibly if someone writes the truthiness check by mistake.

    WHY NOT A STRING like "__missing__":
      - A caller could legitimately pass that exact string as a value, and then
        your "not provided" branch fires on real data. Sentinels must be
        unforgeable, and only object identity gives you that.
    """

    _instance: _Missing | None = None

    def __new__(cls) -> _Missing:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "<MISSING>"

    def __bool__(self) -> bool:
        return False


MISSING: Final = _Missing()


class Cache:
    """A cache in which None is a storable value."""

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}

    def get(self, key: str, default: Any = MISSING) -> Any:
        # Note the ordering: we consult the dict FIRST. A stored None must win
        # over the default. Writing `return self._data.get(key, default)` would
        # also work here, but only because dict.get uses the same sentinel
        # strategy internally -- and it would NOT work if we needed to
        # distinguish further states.
        if key in self._data:
            return self._data[key]
        if default is MISSING:          # `is`, never ==. Identity is the point.
            raise KeyError(key)
        return default

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def has(self, key: str) -> bool:
        # Implemented via a sentinel rather than `in`, to prove the mechanism is
        # sufficient on its own.
        #
        # NOTE THE SUBTLETY, and it is a real one: we cannot pass MISSING here.
        # MISSING is the public "no default was given" signal, so passing it
        # makes get() raise instead of returning it. We need a DIFFERENT unique
        # object that only this method knows about.
        #
        # This generalises: a sentinel is only unambiguous within the protocol
        # that defines it. A function that needs to distinguish more than one
        # "special" state needs more than one sentinel.
        probe = object()
        return self.get(key, probe) is not probe

    def __repr__(self) -> str:
        return f"Cache({self._data!r})"


def update_user(
    user_id: int,
    name: Any = MISSING,
    email: Any = MISSING,
    nickname: Any = MISSING,
) -> dict[str, Any]:
    """Build a partial update payload with three distinguishable intents.

        update_user(1)                      -> {}              nothing changes
        update_user(1, name="Ada")          -> {"name": "Ada"} set it
        update_user(1, nickname=None)       -> {"nickname": None}  CLEAR it

    This is precisely why HTTP PATCH is harder than PUT: the payload must
    distinguish "absent" from "explicitly null", and JSON gives you only one
    null. Real APIs solve it the same way -- pydantic's `model_fields_set`, or
    an explicit Unset sentinel. You will meet this again in Module 28.
    """
    payload: dict[str, Any] = {}
    for field, value in (("name", name), ("email", email), ("nickname", nickname)):
        if value is not MISSING:
            payload[field] = value
    return payload


def verify() -> None:
    c = Cache()
    c.set("a", 1)
    c.set("b", None)

    assert c.get("a") == 1
    assert c.get("b") is None, "a stored None must be returned, not treated as absent"
    assert c.has("b") is True
    assert c.has("zzz") is False
    assert c.get("zzz", "fallback") == "fallback"
    assert c.get("zzz", None) is None, "an explicit None default must be honoured"

    try:
        c.get("zzz")
    except KeyError:
        pass
    else:
        raise AssertionError("absent key with no default must raise KeyError")

    assert update_user(1) == {}
    payload = update_user(1, name="Ada", nickname=None)
    assert payload == {"name": "Ada", "nickname": None}, payload
    assert "email" not in payload

    assert repr(MISSING) == "<MISSING>"
    assert _Missing() is MISSING, "sentinel must be a singleton"

    print("all checks passed")


if __name__ == "__main__":
    verify()
