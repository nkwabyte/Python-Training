"""Exercise 11.1 — Convert five classes. One should not be converted.

For each: convert it to a dataclass with the right options, or explain why a
dataclass is the wrong tool. Preserve behaviour; the tests check it.

Run:  python ex01_convert.py
"""

from __future__ import annotations

import threading
from datetime import datetime
from decimal import Decimal


# --- 1 ------------------------------------------------------------------------
class Coordinate:
    def __init__(self, lat: float, lon: float) -> None:
        if not -90 <= lat <= 90:
            raise ValueError(f"latitude out of range: {lat}")
        if not -180 <= lon <= 180:
            raise ValueError(f"longitude out of range: {lon}")
        self.lat, self.lon = lat, lon

    def __repr__(self) -> str:
        return f"Coordinate(lat={self.lat}, lon={self.lon})"

    def __eq__(self, other: object) -> bool:
        return (isinstance(other, Coordinate)
                and (self.lat, self.lon) == (other.lat, other.lon))

    def __hash__(self) -> int:
        return hash((self.lat, self.lon))


# --- 2 ------------------------------------------------------------------------
class HttpRequest:
    """Note the mutable default and the derived field."""

    def __init__(self, method, url, headers=None, body=b"", timeout=30):  # type: ignore[no-untyped-def]
        self.method = method.upper()
        self.url = url
        self.headers = headers if headers is not None else {}
        self.body = body
        self.timeout = timeout
        self.created = datetime.now()
        self.content_length = len(body)

    def __repr__(self) -> str:
        return f"HttpRequest({self.method} {self.url})"


# --- 3 ------------------------------------------------------------------------
class Money:
    """Ordering matters here, and so does what is hashed."""

    def __init__(self, cents: int, currency: str = "USD") -> None:
        self.cents, self.currency = cents, currency

    def __eq__(self, other: object) -> bool:
        return (isinstance(other, Money)
                and (self.cents, self.currency) == (other.cents, other.currency))

    def __lt__(self, other: Money) -> bool:
        if self.currency != other.currency:
            raise ValueError("cannot order different currencies")
        return self.cents < other.cents

    def __hash__(self) -> int:
        return hash((self.cents, self.currency))

    def __repr__(self) -> str:
        return f"Money({self.cents}, {self.currency!r})"


# --- 4 ------------------------------------------------------------------------
class CacheEntry:
    """Two fields must NOT participate in equality. Which, and why?"""

    def __init__(self, key: str, value: object) -> None:
        self.key, self.value = key, value
        self.created = datetime.now()
        self.hit_count = 0

    def touch(self) -> None:
        self.hit_count += 1

    def __eq__(self, other: object) -> bool:
        return (isinstance(other, CacheEntry)
                and (self.key, self.value) == (other.key, other.value))


# --- 5 ------------------------------------------------------------------------
class ConnectionPool:
    """This one should NOT become a dataclass. Work out why before reading on."""

    def __init__(self, dsn: str, size: int = 5) -> None:
        self._dsn = dsn
        self._size = size
        self._lock = threading.Lock()
        self._connections: list[object] = []
        self._in_use: set[object] = set()

    def acquire(self) -> object:
        with self._lock:
            if self._connections:
                conn = self._connections.pop()
            else:
                conn = object()
            self._in_use.add(conn)
            return conn

    def release(self, conn: object) -> None:
        with self._lock:
            self._in_use.discard(conn)
            self._connections.append(conn)


# TODO -------------------------------------------------------------------------
# Convert 1-4. For 5, write a paragraph answering:
#   - what would @dataclass generate that is actively WRONG here?
#   - what would __eq__ on this type even mean?
#   - what happens if someone calls asdict() on it?
#   - what does the presence of a Lock tell you about whether this is a record?
# The general rule you should end up with distinguishes types that ARE data from
# types that MANAGE something.


def verify() -> None:
    from dataclasses import fields, is_dataclass, replace

    c = Coordinate(51.5, -0.12)
    assert is_dataclass(c)
    assert c == Coordinate(51.5, -0.12)
    assert {c: "London"}[Coordinate(51.5, -0.12)] == "London"
    try:
        Coordinate(200, 0)
    except ValueError:
        pass
    else:
        raise AssertionError("validation must survive the conversion")
    try:
        c.lat = 0            # type: ignore[misc]
    except AttributeError:
        pass
    else:
        raise AssertionError("Coordinate should be frozen")

    r1 = HttpRequest("get", "http://x")
    r2 = HttpRequest("get", "http://x")
    r1.headers["a"] = "1"
    assert r2.headers == {}, "the mutable default is still shared"
    assert r1.method == "GET", "__post_init__ must still normalise the method"
    assert r1.content_length == 0

    assert sorted([Money(500), Money(100)]) == [Money(100), Money(500)]
    assert Money(500) == Money(500)
    assert {Money(500)} == {Money(500)}

    e1 = CacheEntry("k", "v")
    e2 = CacheEntry("k", "v")
    e1.touch()
    assert e1 == e2, "hit_count and created must not affect equality"
    names = {f.name for f in fields(e1)}
    assert names == {"key", "value", "created", "hit_count"}, names

    print("all conversion checks passed")


if __name__ == "__main__":
    verify()
