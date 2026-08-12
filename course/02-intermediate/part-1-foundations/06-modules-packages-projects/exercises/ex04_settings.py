"""Exercise 06.4 — Layered, typed, validated settings.

Build a Settings object that reads, in increasing order of precedence:

    1. built-in defaults
    2. a TOML config file          (tomllib, stdlib since 3.11)
    3. environment variables       (highest precedence)

and validates the result ONCE, at construction, with errors good enough that a
person reading a crashed container log knows exactly what to fix.

Run:  python ex04_settings.py
"""

from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class ConfigError(Exception):
    """Raised when configuration is missing or invalid."""


# TODO 1 -----------------------------------------------------------------------
@dataclass(frozen=True)
class Settings:
    """Frozen, so config cannot change mid-request.

    Fields:
      database_url : str          REQUIRED, no default
      port         : int          default 8000, must be 1..65535
      debug        : bool         default False
      log_level    : str          default "INFO", one of DEBUG/INFO/WARN/ERROR
      timeout      : float        default 30.0, must be > 0
      allowed_hosts: tuple[str,...] default ("localhost",)
                                  (tuple, not list -- frozen means hashable)
    """


# TODO 2 -----------------------------------------------------------------------
def parse_bool(raw: str) -> bool:
    """Environment variables are always strings, and bool("false") is True.

    That single fact has caused an enormous number of production incidents:
    someone sets DEBUG=false, and debug mode turns ON.

    Accept, case-insensitively: 1/true/yes/on  and  0/false/no/off/"".
    Raise ConfigError for anything else -- silently treating "maybe" as False
    is how the incident happens twice.
    """
    raise NotImplementedError


# TODO 3 -----------------------------------------------------------------------
def load_settings(
    config_file: Path | None = None,
    env: dict[str, str] | None = None,
) -> Settings:
    """Merge the three layers and validate.

    Take `env` as a PARAMETER defaulting to os.environ. That is what makes this
    testable without mutating the real environment -- the same lesson as
    main(argv) in Module 01.

    Environment variable names: prefix each field with APP_ and uppercase it.
      APP_DATABASE_URL, APP_PORT, APP_DEBUG, APP_LOG_LEVEL, APP_TIMEOUT,
      APP_ALLOWED_HOSTS  (comma-separated)

    Validation must collect ALL errors before raising, not stop at the first.
    A user fixing config wants the full list, not one item per restart cycle.
    """
    raise NotImplementedError


# TODO 4 -----------------------------------------------------------------------
def redacted(settings: Settings) -> dict[str, Any]:
    """Return a dict safe to log.

    database_url contains a password. It must appear as
    postgres://user:***@host/db -- never in full.

    This is not paranoia: connection strings in logs are one of the most common
    real-world credential leaks, because logs get shipped to a third-party
    aggregator that has a different access policy than your database.
    """
    raise NotImplementedError


def verify() -> None:
    env = {"APP_DATABASE_URL": "postgres://user:secret@db:5432/app"}
    s = load_settings(env=env)
    assert s.port == 8000 and s.debug is False and s.timeout == 30.0
    assert s.allowed_hosts == ("localhost",)

    with tempfile.TemporaryDirectory() as td:
        cfg = Path(td) / "config.toml"
        cfg.write_text(
            'port = 9000\ndebug = true\nallowed_hosts = ["a.com", "b.com"]\n',
            encoding="utf-8",
        )
        s = load_settings(cfg, env=env)
        assert s.port == 9000, s.port
        assert s.debug is True
        assert s.allowed_hosts == ("a.com", "b.com")

        # environment beats file
        s = load_settings(cfg, env={**env, "APP_PORT": "7000", "APP_DEBUG": "off"})
        assert s.port == 7000
        assert s.debug is False

    for bad in ["maybe", "yep", "2"]:
        try:
            parse_bool(bad)
        except ConfigError:
            pass
        else:
            raise AssertionError(f"parse_bool({bad!r}) should have raised")
    assert parse_bool("FALSE") is False
    assert parse_bool("on") is True

    try:
        load_settings(env={})
    except ConfigError as exc:
        assert "DATABASE_URL" in str(exc), str(exc)
    else:
        raise AssertionError("a missing required setting must raise")

    try:
        load_settings(env={**env, "APP_PORT": "99999", "APP_TIMEOUT": "-1"})
    except ConfigError as exc:
        msg = str(exc)
        assert "port" in msg.lower() and "timeout" in msg.lower(), (
            f"must report ALL errors at once, got: {msg}"
        )
    else:
        raise AssertionError("invalid values must raise")

    out = redacted(load_settings(env=env))
    assert "secret" not in str(out), out
    assert "***" in str(out["database_url"])

    print("all settings checks passed")


if __name__ == "__main__":
    verify()
