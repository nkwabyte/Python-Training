"""Exercise 02.2 — Six aliasing bugs from real code.

Each function below is subtly wrong. For each one:

  1. Read it and predict what goes wrong, and under what input.
  2. Run the demo at the bottom to confirm.
  3. Fix it.
  4. Write the assert (or pytest test) that would have caught it. Add these to
     the TESTS section at the bottom and make them pass.

These are not contrived. Every one of these is a bug pattern that ships to
production regularly.
"""

from __future__ import annotations


# --- bug 1: the shared default -----------------------------------------------
def record_event(name: str, log: list[str] = []) -> list[str]:
    """Append an event to a log, creating a new one if none is given."""
    log.append(name)
    return log


# --- bug 2: the leaked internal ----------------------------------------------
class Playlist:
    """A playlist that hands out its internal list."""

    def __init__(self, tracks: list[str]) -> None:
        self._tracks = tracks

    def get_tracks(self) -> list[str]:
        return self._tracks

    def add(self, track: str) -> None:
        self._tracks.append(track)


# --- bug 3: the config that is not a copy ------------------------------------
DEFAULT_CONFIG: dict[str, object] = {
    "host": "localhost",
    "port": 8080,
    "features": {"beta": False, "debug": False},
}


def make_config(**overrides: object) -> dict[str, object]:
    """Return DEFAULT_CONFIG with the given overrides applied."""
    config = DEFAULT_CONFIG.copy()
    config.update(overrides)
    return config


def enable_debug(config: dict[str, object]) -> dict[str, object]:
    features = config["features"]
    assert isinstance(features, dict)
    features["debug"] = True
    return config


# --- bug 4: mutating while iterating -----------------------------------------
def drop_expired(sessions: dict[str, int], now: int) -> dict[str, int]:
    """Remove sessions whose expiry is in the past."""
    for key, expiry in sessions.items():
        if expiry < now:
            del sessions[key]
    return sessions


# --- bug 5: the matrix that is one row ---------------------------------------
def make_board(size: int) -> list[list[str]]:
    """Create a size x size game board of empty cells."""
    return [["."] * size] * size


# --- bug 6: sort returning None ----------------------------------------------
def top_n(scores: list[int], n: int) -> list[int]:
    """Return the n highest scores, without disturbing the caller's list."""
    ordered = scores
    ordered.sort(reverse=True)
    return ordered[:n]


# --- demo ---------------------------------------------------------------------
def demo() -> None:
    print("bug 1:", record_event("login"), record_event("logout"))

    original = ["a", "b"]
    p = Playlist(original)
    p.get_tracks().append("SNEAKY")
    original.append("ALSO SNEAKY")
    print("bug 2:", p.get_tracks())

    c1 = make_config(port=9000)
    enable_debug(c1)
    c2 = make_config()
    print("bug 3:", c2["features"])

    try:
        print("bug 4:", drop_expired({"a": 1, "b": 5, "c": 2}, now=3))
    except RuntimeError as exc:
        print("bug 4: RuntimeError:", exc)

    board = make_board(3)
    board[0][0] = "X"
    print("bug 5:", board)

    scores = [10, 50, 20]
    print("bug 6:", top_n(scores, 2), "caller's list is now", scores)


if __name__ == "__main__":
    demo()


# --- TESTS: write these, then make them pass after fixing ---------------------
def test_record_event_does_not_share_state() -> None:
    ...


def test_playlist_does_not_leak_internals() -> None:
    ...


def test_config_defaults_are_not_polluted() -> None:
    ...


def test_drop_expired_removes_correct_keys() -> None:
    ...


def test_board_rows_are_independent() -> None:
    ...


def test_top_n_leaves_caller_list_alone() -> None:
    ...
