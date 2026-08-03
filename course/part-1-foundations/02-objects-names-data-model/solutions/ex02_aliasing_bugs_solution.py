"""Solution 02.2 — Six aliasing bugs, fixed, with the tests that catch them."""

from __future__ import annotations

import copy
from typing import Any


# --- bug 1: the shared default -----------------------------------------------
# CAUSE: the default [] is created ONCE, when `def` executes, and stored in
# record_event.__defaults__. Every call that omits `log` shares that one object.
def record_event(name: str, log: list[str] | None = None) -> list[str]:
    if log is None:          # `is None`, not `if not log` -- an empty list the
        log = []             # caller passed deliberately must be respected
    log.append(name)
    return log


# --- bug 2: the leaked internal ----------------------------------------------
# CAUSE: two leaks. The constructor stores the caller's list (so the caller can
# mutate the playlist from outside), and get_tracks hands the internal list out
# (so anyone can mutate it). Encapsulation that returns a mutable internal is
# not encapsulation.
class Playlist:
    def __init__(self, tracks: list[str]) -> None:
        self._tracks = list(tracks)          # copy IN

    def get_tracks(self) -> tuple[str, ...]:
        return tuple(self._tracks)           # immutable view OUT

    def add(self, track: str) -> None:
        self._tracks.append(track)

    # Alternatives, each defensible:
    #   return list(self._tracks)   -- a copy; caller may mutate their own copy
    #   yield from self._tracks     -- lazy, cheapest, but stale if we mutate
    #   return MappingProxyType-ish read-only view (Module 09)
    # tuple is the best default: cheap, obviously immutable, and the type
    # signature tells the caller not to expect to mutate it.


# --- bug 3: the config that is not a copy ------------------------------------
# CAUSE: dict.copy() is SHALLOW. config["features"] is the same dict object as
# DEFAULT_CONFIG["features"], so enable_debug() writes straight into the module
# level default and poisons every future call. This one is nasty because the
# corruption is invisible until an unrelated part of the program reads it.
DEFAULT_CONFIG: dict[str, Any] = {
    "host": "localhost",
    "port": 8080,
    "features": {"beta": False, "debug": False},
}


def make_config(**overrides: Any) -> dict[str, Any]:
    config = copy.deepcopy(DEFAULT_CONFIG)   # deep, because it nests
    config.update(overrides)
    return config


def enable_debug(config: dict[str, Any]) -> dict[str, Any]:
    features = config["features"]
    assert isinstance(features, dict)
    features["debug"] = True
    return config


# The stronger fix is to make the default un-mutatable in the first place:
#   DEFAULT_CONFIG = MappingProxyType({...})  -> writes raise TypeError loudly
# Best of all is a frozen dataclass (Module 11), which makes the whole class of
# bug unrepresentable.


# --- bug 4: mutating while iterating -----------------------------------------
# CAUSE: deleting from a dict during iteration raises
# "RuntimeError: dictionary changed size during iteration".
# The list equivalent (bug in the original ex01 q11) is WORSE: it does not
# raise, it silently skips elements, because the index advances while the list
# shrinks under it.
def drop_expired(sessions: dict[str, int], now: int) -> dict[str, int]:
    # Build a new dict. Cheapest, clearest, and does not mutate the caller's data.
    return {k: v for k, v in sessions.items() if v >= now}


def drop_expired_inplace(sessions: dict[str, int], now: int) -> None:
    """If in-place really is required, snapshot the keys first."""
    for key in list(sessions):        # list() materialises the keys up front
        if sessions[key] < now:
            del sessions[key]


# --- bug 5: the matrix that is one row ---------------------------------------
# CAUSE: `[x] * n` repeats the REFERENCE n times. All three rows are one list.
def make_board(size: int) -> list[list[str]]:
    return [["."] * size for _ in range(size)]
    # Note that ["."] * size is fine: str is immutable, so sharing is harmless.
    # It is only the OUTER multiplication that breaks.


# --- bug 6: sort returning None ----------------------------------------------
# CAUSE: two bugs in three lines. `ordered = scores` aliases rather than copies,
# and .sort() mutates in place. The caller's list is reordered as a side effect
# of a function that promised not to touch it.
def top_n(scores: list[int], n: int) -> list[int]:
    return sorted(scores, reverse=True)[:n]
    # sorted() returns a NEW list. .sort() mutates and returns None.
    # Python's convention: methods that mutate in place return None, precisely
    # so that `x = lst.sort()` fails loudly instead of silently binding None.
    # Same pair: list.reverse/reversed, and random.shuffle (mutates, no pair).


# --- tests --------------------------------------------------------------------
def test_record_event_does_not_share_state() -> None:
    first = record_event("login")
    second = record_event("logout")
    assert first == ["login"]
    assert second == ["logout"]
    assert first is not second


def test_record_event_respects_an_explicit_empty_list() -> None:
    given: list[str] = []
    returned = record_event("x", given)
    assert returned is given, "an explicitly passed list must be used, not replaced"


def test_playlist_does_not_leak_internals() -> None:
    original = ["a", "b"]
    p = Playlist(original)

    original.append("outside")
    assert "outside" not in p.get_tracks(), "constructor must copy its input"

    tracks = p.get_tracks()
    assert isinstance(tracks, tuple)
    try:
        tracks.append("sneaky")  # type: ignore[attr-defined]
    except AttributeError:
        pass
    else:
        raise AssertionError("get_tracks must not return a mutable internal")


def test_config_defaults_are_not_polluted() -> None:
    first = make_config()
    enable_debug(first)
    second = make_config()
    assert second["features"]["debug"] is False, "DEFAULT_CONFIG was mutated"
    assert DEFAULT_CONFIG["features"]["debug"] is False


def test_drop_expired_removes_correct_keys() -> None:
    sessions = {"a": 1, "b": 5, "c": 2, "d": 9}
    result = drop_expired(sessions, now=3)
    assert result == {"b": 5, "d": 9}
    assert sessions == {"a": 1, "b": 5, "c": 2, "d": 9}, "input must be untouched"


def test_drop_expired_inplace_is_correct_too() -> None:
    sessions = {"a": 1, "b": 5, "c": 2, "d": 9}
    drop_expired_inplace(sessions, now=3)
    assert sessions == {"b": 5, "d": 9}


def test_board_rows_are_independent() -> None:
    board = make_board(3)
    board[0][0] = "X"
    assert board[1][0] == ".", "rows share a single list object"
    assert board[0] is not board[1]


def test_top_n_leaves_caller_list_alone() -> None:
    scores = [10, 50, 20]
    assert top_n(scores, 2) == [50, 20]
    assert scores == [10, 50, 20], "top_n reordered the caller's list"


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"  PASS  {t.__name__}")
    print(f"\n{len(tests)} tests passed")
