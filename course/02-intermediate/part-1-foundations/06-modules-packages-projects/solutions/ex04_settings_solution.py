"""Solution 06.4 — Layered, typed, validated settings."""

from __future__ import annotations

import os
import tempfile
try:
    import tomllib                       # stdlib since 3.11
except ModuleNotFoundError:              # 3.10 and older
    import tomli as tomllib              # type: ignore[no-redef]
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

VALID_LOG_LEVELS = frozenset({"DEBUG", "INFO", "WARN", "WARNING", "ERROR"})
TRUE_VALUES = frozenset({"1", "true", "yes", "on", "y", "t"})
FALSE_VALUES = frozenset({"0", "false", "no", "off", "n", "f", ""})


class ConfigError(Exception):
    """Raised when configuration is missing or invalid."""


@dataclass(frozen=True)
class Settings:
    """Frozen: configuration cannot change halfway through a request.

    Note allowed_hosts is a TUPLE, not a list. A frozen dataclass with a list
    field is still mutable through that field -- frozen prevents REBINDING the
    attribute, not mutating what it points at. Module 02's tuple trap, applied.
    """

    database_url: str
    port: int = 8000
    debug: bool = False
    log_level: str = "INFO"
    timeout: float = 30.0
    allowed_hosts: tuple[str, ...] = ("localhost",)


def parse_bool(raw: str) -> bool:
    """The single most expensive one-line bug in twelve-factor config.

        DEBUG=false  ->  os.environ["DEBUG"]  ->  "false"  ->  bool("false")
                     ->  True

    Every non-empty string is truthy, so the operator sets DEBUG=false and
    turns debug mode ON, in production, with stack traces going to users.

    Raising on unrecognised input rather than defaulting to False is
    deliberate: DEBUG=maybe is a typo, and silently choosing an interpretation
    means the same incident happens again with a different spelling.
    """
    value = raw.strip().lower()
    if value in TRUE_VALUES:
        return True
    if value in FALSE_VALUES:
        return False
    raise ConfigError(
        f"cannot interpret {raw!r} as a boolean. "
        f"Use one of: {', '.join(sorted(TRUE_VALUES | FALSE_VALUES - {''}))}"
    )


def _from_file(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    try:
        with path.open("rb") as fh:          # tomllib requires BINARY mode
            return tomllib.load(fh)
    except FileNotFoundError:
        return {}                             # an absent file is not an error
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"{path}: invalid TOML: {exc}") from exc


def _from_env(env: dict[str, str], errors: list[str]) -> dict[str, Any]:
    """Read APP_-prefixed variables, converting each to its declared type."""
    out: dict[str, Any] = {}
    known = {f.name for f in fields(Settings)}
    for name in known:
        raw = env.get(f"APP_{name.upper()}")
        if raw is None:
            continue
        try:
            if name == "debug":
                out[name] = parse_bool(raw)
            elif name == "port":
                out[name] = int(raw)
            elif name == "timeout":
                out[name] = float(raw)
            elif name == "allowed_hosts":
                out[name] = tuple(h.strip() for h in raw.split(",") if h.strip())
            else:
                out[name] = raw
        except (ValueError, ConfigError) as exc:
            errors.append(f"APP_{name.upper()}={raw!r}: {exc}")
    return out


def load_settings(
    config_file: Path | None = None,
    env: dict[str, str] | None = None,
) -> Settings:
    """defaults <- file <- environment, then validate everything at once.

    `env` is a PARAMETER defaulting to os.environ, exactly like main(argv) in
    Module 01. Tests pass a dict; nothing has to mutate the real process
    environment, which is global mutable state shared by every test in the run.
    """
    env = os.environ.copy() if env is None else env
    errors: list[str] = []

    merged: dict[str, Any] = {}
    merged.update(_from_file(config_file))
    merged.update(_from_env(env, errors))

    # normalise types that TOML may have given us in another shape
    if "allowed_hosts" in merged and isinstance(merged["allowed_hosts"], list):
        merged["allowed_hosts"] = tuple(merged["allowed_hosts"])

    known = {f.name for f in fields(Settings)}
    for unknown in sorted(set(merged) - known):
        errors.append(f"unknown setting {unknown!r}")
        merged.pop(unknown)

    if not merged.get("database_url"):
        errors.append(
            "database_url is required. Set APP_DATABASE_URL, or add "
            "database_url to your config file."
        )

    # COLLECT every error before raising. A user fixing config in a container
    # wants the whole list, not one item per restart -- each restart cycle is a
    # deploy, and three of them is an afternoon.
    port = merged.get("port", 8000)
    if isinstance(port, int) and not 1 <= port <= 65535:
        errors.append(f"port must be between 1 and 65535, got {port}")

    timeout = merged.get("timeout", 30.0)
    if isinstance(timeout, (int, float)) and timeout <= 0:
        errors.append(f"timeout must be positive, got {timeout}")

    level = str(merged.get("log_level", "INFO")).upper()
    if level not in VALID_LOG_LEVELS:
        errors.append(
            f"log_level must be one of {sorted(VALID_LOG_LEVELS)}, got {level!r}"
        )
    merged["log_level"] = level

    if errors:
        raise ConfigError(
            "invalid configuration:\n  - " + "\n  - ".join(errors)
        )

    return Settings(**merged)


def redacted(settings: Settings) -> dict[str, Any]:
    """Safe to log.

    Connection strings in logs are one of the most common real credential
    leaks, because logs are shipped to an aggregator with a different access
    policy than the database. The password must never leave the process.

    Note this masks the password COMPONENT rather than regex-replacing likely
    secrets: parsing the URL means it works for every scheme and cannot be
    defeated by an unusual password character.
    """
    parts = urlsplit(settings.database_url)
    if parts.password:
        netloc = f"{parts.username}:***@{parts.hostname}"
        if parts.port:
            netloc += f":{parts.port}"
        safe_url = urlunsplit(
            (parts.scheme, netloc, parts.path, parts.query, parts.fragment)
        )
    else:
        safe_url = settings.database_url

    return {
        f.name: (safe_url if f.name == "database_url" else getattr(settings, f.name))
        for f in fields(settings)
    }


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
        assert "database_url" in str(exc)
    else:
        raise AssertionError("a missing required setting must raise")

    try:
        load_settings(env={**env, "APP_PORT": "99999", "APP_TIMEOUT": "-1"})
    except ConfigError as exc:
        msg = str(exc)
        assert "port" in msg.lower() and "timeout" in msg.lower(), msg
    else:
        raise AssertionError("invalid values must raise")

    out = redacted(load_settings(env=env))
    assert "secret" not in str(out), out
    assert "***" in str(out["database_url"])

    print("all settings checks passed")
    print("\nexample error output:")
    try:
        load_settings(env={"APP_PORT": "0", "APP_LOG_LEVEL": "LOUD",
                           "APP_DEBUG": "maybe"})
    except ConfigError as exc:
        print(exc)


if __name__ == "__main__":
    verify()
