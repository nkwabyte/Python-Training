"""Exercise 19.4 — Five vulnerabilities. Exploit each, then fix it.

Every function below is exploitable. For each: write the exploit input, run it,
observe the damage, then fix the function so the same input is harmless.

Do this on your own machine, in a temp directory. The point is to see the
attacks work once, because a vulnerability you have only read about is one you
will write again.

Run:  python ex04_security.py
"""
from __future__ import annotations

import hashlib
import os
import pickle
import sqlite3
import subprocess
import tempfile
import time
from pathlib import Path


# --- 1: SQL injection ---------------------------------------------------------
def find_user_vulnerable(conn: sqlite3.Connection, name: str) -> list[tuple]:
    query = f"SELECT id, name, email FROM users WHERE name = '{name}'"
    return conn.execute(query).fetchall()


# EXPLOIT 1a: return every row, not just the matching one.
#             name = ?
# EXPLOIT 1b: destroy the table.
#             name = ?
# EXPLOIT 1c: read a row from a DIFFERENT table (a UNION attack).
#             name = ?
#
# TODO: write find_user(conn, name) and verify all three exploits become
# ordinary, harmless searches that return zero rows.


# --- 2: command injection -----------------------------------------------------
def count_matches_vulnerable(pattern: str, path: str) -> str:
    return subprocess.run(
        f"grep -c '{pattern}' {path}", shell=True,
        capture_output=True, text=True,
    ).stdout


# EXPLOIT 2: run an arbitrary command.
#            pattern = ?
#
# TODO: rewrite with a list of arguments. Then answer: what happens to your
# exploit string now, and WHY can it not be interpreted?


# --- 3: path traversal --------------------------------------------------------
def read_user_file_vulnerable(base: Path, filename: str) -> str:
    return (base / filename).read_text(encoding="utf-8")


# EXPLOIT 3a: read a file outside `base`.
#             filename = ?
# EXPLOIT 3b: the same, using an absolute path. (Try it -- Path.__truediv__
#             does something surprising with an absolute right-hand side.)
#             filename = ?
#
# TODO: fix with resolve() and is_relative_to. Then test SIX attacks:
#   "../secret.txt", "../../etc/passwd", "/etc/passwd", "a/../../secret.txt",
#   "./../../secret.txt", and a symlink pointing outside the base.
# The symlink one is why resolve() rather than a string check is required.


# --- 4: unsafe deserialization ------------------------------------------------
def load_session_vulnerable(data: bytes) -> object:
    return pickle.loads(data)


# EXPLOIT 4: craft a payload whose unpickling runs a command. Use __reduce__.
#            (Write it, run it against a harmless command like `echo pwned`,
#            and see it execute.)
#
# TODO: replace with JSON. Then answer: could you make pickle safe by
# validating the bytes first? Try to state a validation rule that works, and
# explain why you cannot.


# --- 5: timing attack ---------------------------------------------------------
def check_token_vulnerable(supplied: str, expected: str) -> bool:
    return supplied == expected


# EXPLOIT 5: recover a secret token one character at a time by measuring
#            comparison time. The measurement below is deliberately crude; make
#            it work by averaging over many trials.
#
# TODO: fix with hmac.compare_digest. Then answer: why does == leak, and what
# exactly does compare_digest guarantee? Does it hide the token's LENGTH?


def demo_timing() -> None:
    """A crude demonstration that == returns faster on an early mismatch."""
    secret = "s" * 1000 + "X"
    trials = 2000
    for candidate, label in [("a" + "s" * 1000, "differs at position 0"),
                             ("s" * 1000 + "Y", "differs at position 1000")]:
        start = time.perf_counter()
        for _ in range(trials):
            candidate == secret            # noqa: B015
        elapsed = time.perf_counter() - start
        print(f"    {label:<28} {elapsed * 1e6 / trials:8.3f} us/comparison")


def setup_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.executescript("""
        CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT);
        CREATE TABLE secrets (id INTEGER PRIMARY KEY, api_key TEXT);
        INSERT INTO users VALUES (1, 'ada', 'ada@example.com');
        INSERT INTO users VALUES (2, 'bo', 'bo@example.com');
        INSERT INTO secrets VALUES (1, 'sk-super-secret');
    """)
    return conn


if __name__ == "__main__":
    print("1. SQL injection")
    conn = setup_db()
    print("    normal search:", find_user_vulnerable(conn, "ada"))
    print("    TODO: write the three exploit strings and run them here")

    print("\n5. timing")
    demo_timing()
    print("    the difference is small but measurable, and it is enough")
