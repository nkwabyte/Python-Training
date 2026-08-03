"""Exercise 03.2 — The encoding boundary.

A log-processing script that works fine on the developer's machine and corrupts
data in production. Fix it, then make it robust against files whose encoding
you do not control.

Run:  python ex02_encoding.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

SAMPLE_LINES = [
    "2026-08-01 INFO  user=José action=login",
    "2026-08-01 WARN  user=Müller action=retry café=true",
    "2026-08-01 ERROR user=Ωmega action=crash naïve=yes",
    "2026-08-01 INFO  user=张伟 action=logout",
]


def make_fixtures(tmp: Path) -> dict[str, Path]:
    """Write the same content in three different encodings."""
    files = {}
    for name, enc in [("utf8.log", "utf-8"), ("latin1.log", "latin-1"),
                      ("utf16.log", "utf-16")]:
        p = tmp / name
        try:
            p.write_text("\n".join(SAMPLE_LINES), encoding=enc)
        except UnicodeEncodeError:
            # latin-1 cannot represent every character -- that is the point
            p.write_bytes("\n".join(SAMPLE_LINES[:2]).encode("latin-1"))
        files[name] = p
    return files


# --- the broken version -------------------------------------------------------
def count_users_broken(path: Path) -> dict[str, int]:
    """BUG 1: no encoding specified. BUG 2: reads bytes and str inconsistently.

    TODO: find all the bugs by reading, before running.
    """
    counts: dict[str, int] = {}
    with open(path) as fh:                       # BUG: locale-dependent
        for line in fh:
            for field in line.split():
                if field.startswith("user="):
                    user = field[5:]
                    counts[user] = counts.get(user, 0) + 1
    return counts


# TODO 1 -----------------------------------------------------------------------
def count_users(path: Path, encoding: str = "utf-8") -> dict[str, int]:
    """Fix count_users_broken. Explicit encoding, explicit error handling.

    Decide and justify: should a malformed byte sequence raise, or be replaced?
    Write your answer as a docstring line.
    """
    raise NotImplementedError


# TODO 2 -----------------------------------------------------------------------
def detect_encoding(path: Path) -> str:
    """Guess a file's encoding well enough to read it.

    Strategy, in order:
      1. Check for a BOM (utf-8-sig, utf-16-le, utf-16-be, utf-32). The codecs
         module has the BOM constants.
      2. Try utf-8 strictly. If it decodes, it is almost certainly utf-8 --
         utf-8 is self-validating, and random bytes rarely decode cleanly.
      3. Fall back to a declared default (cp1252 or latin-1). latin-1 NEVER
         fails, because every byte 0-255 maps to some character. Explain in a
         comment why "never fails" is a warning rather than a feature.

    Real code uses charset-normalizer or chardet for this. Implementing the
    simple version once teaches you what those libraries are actually doing.
    """
    raise NotImplementedError


# TODO 3 -----------------------------------------------------------------------
def read_any(path: Path) -> str:
    """Read a text file of unknown encoding, never raising, never silently
    corrupting. Report on stderr which encoding was chosen."""
    raise NotImplementedError


# TODO 4 -----------------------------------------------------------------------
def safe_truncate(text: str, max_bytes: int, encoding: str = "utf-8") -> str:
    """Truncate text so its UTF-8 encoding is at most max_bytes, WITHOUT
    splitting a character in half.

    This is a real problem: database columns, log fields, and HTTP headers are
    limited in BYTES, while your text is measured in CHARACTERS.

    Naive `text[:max_bytes]` is wrong (wrong unit).
    Naive `text.encode()[:max_bytes].decode()` raises UnicodeDecodeError when it
    cuts mid-character.

    Two correct approaches -- implement either, and name the other in a comment:
      (a) encode, slice, then decode with errors='ignore'
      (b) walk characters accumulating byte lengths until the budget is spent
    Which is faster? Which is clearer? Do they always agree?
    """
    raise NotImplementedError


def verify() -> None:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        files = make_fixtures(tmp)

        counts = count_users(files["utf8.log"])
        assert counts.get("José") == 1, counts
        assert counts.get("张伟") == 1, counts

        assert detect_encoding(files["utf8.log"]).startswith("utf-8")
        assert detect_encoding(files["utf16.log"]).startswith("utf-16")

        text = read_any(files["latin1.log"])
        assert "user=" in text

    assert safe_truncate("café", 4) == "caf", safe_truncate("café", 4)
    assert safe_truncate("café", 5) == "café"  # é is 2 bytes: "café" is 5 bytes
    assert safe_truncate("张伟好", 7) == "张伟"
    assert len(safe_truncate("张伟好", 7).encode("utf-8")) <= 7

    print("all encoding checks passed")


if __name__ == "__main__":
    verify()
