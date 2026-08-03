"""Solution 03.2 — The encoding boundary."""

from __future__ import annotations

import codecs
import sys
import tempfile
from pathlib import Path

SAMPLE_LINES = [
    "2026-08-01 INFO  user=José action=login",
    "2026-08-01 WARN  user=Müller action=retry café=true",
    "2026-08-01 ERROR user=Ωmega action=crash naïve=yes",
    "2026-08-01 INFO  user=张伟 action=logout",
]


def make_fixtures(tmp: Path) -> dict[str, Path]:
    files = {}
    for name, enc in [("utf8.log", "utf-8"), ("latin1.log", "latin-1"),
                      ("utf16.log", "utf-16")]:
        p = tmp / name
        try:
            p.write_text("\n".join(SAMPLE_LINES), encoding=enc)
        except UnicodeEncodeError:
            p.write_bytes("\n".join(SAMPLE_LINES[:2]).encode("latin-1"))
        files[name] = p
    return files


def count_users(path: Path, encoding: str = "utf-8") -> dict[str, int]:
    """Explicit encoding, explicit error policy.

    SHOULD MALFORMED BYTES RAISE OR BE REPLACED? Raise, by default. A log line
    that fails to decode signals either the wrong encoding (a configuration
    bug) or corrupted input (a data bug). Both deserve attention. errors=
    'replace' converts a loud, findable problem into a silent one whose only
    trace is a U+FFFD somewhere downstream.

    The exception: bulk pipelines where partial results beat no results. There,
    replace + a counter of replacement characters + an alert threshold is the
    right shape. The policy should be a decision, never a default.
    """
    counts: dict[str, int] = {}
    with path.open(encoding=encoding, errors="strict") as fh:
        for line in fh:
            for field in line.split():
                if field.startswith("user="):
                    user = field.removeprefix("user=")
                    counts[user] = counts.get(user, 0) + 1
    return counts


BOMS: list[tuple[bytes, str]] = [
    (codecs.BOM_UTF32_LE, "utf-32"),
    (codecs.BOM_UTF32_BE, "utf-32"),
    (codecs.BOM_UTF8, "utf-8-sig"),
    (codecs.BOM_UTF16_LE, "utf-16"),
    (codecs.BOM_UTF16_BE, "utf-16"),
]
# NOTE the ordering: UTF-32-LE begins with the same two bytes as UTF-16-LE
# (FF FE 00 00 vs FF FE), so the longer BOM must be tested first. Getting this
# order wrong is a classic bug in hand-rolled detectors.


def detect_encoding(path: Path) -> str:
    raw = path.read_bytes()

    for bom, name in BOMS:
        if raw.startswith(bom):
            return name

    try:
        raw.decode("utf-8")
    except UnicodeDecodeError:
        pass
    else:
        return "utf-8"

    # WHY "latin-1 never fails" IS A WARNING, NOT A FEATURE:
    # latin-1 maps every one of the 256 byte values to a character, so decoding
    # ALWAYS succeeds -- including on data that is not latin-1 at all, and
    # including on binary data like a JPEG. It cannot report an error because
    # it has no invalid inputs. So it never tells you that you guessed wrong;
    # it hands you plausible-looking mojibake and lets you write it to your
    # database. It is a safe LAST resort precisely because it round-trips
    # bytes losslessly, and a terrible first guess for the same reason.
    return "cp1252"


def read_any(path: Path) -> str:
    encoding = detect_encoding(path)
    try:
        text = path.read_text(encoding=encoding)
    except UnicodeDecodeError:
        print(f"warning: {path.name} failed as {encoding}; falling back to "
              f"latin-1 (output may be mojibake)", file=sys.stderr)
        return path.read_text(encoding="latin-1")
    print(f"note: read {path.name} as {encoding}", file=sys.stderr)
    return text


def safe_truncate(text: str, max_bytes: int, encoding: str = "utf-8") -> str:
    """Approach (a): encode, slice, decode with errors='ignore'.

    Slicing the encoded bytes may cut a multi-byte sequence in half; decoding
    with errors='ignore' discards that dangling partial sequence, which is
    exactly the behaviour we want here. This is the one place where 'ignore' is
    correct rather than negligent, because the discarded bytes are known to be
    an incomplete character, not lost data.

    Approach (b) walks characters accumulating byte lengths and stops before
    exceeding the budget. It is O(n) in characters rather than O(n) in bytes,
    is clearer to a reader unfamiliar with UTF-8's self-synchronising property,
    and is required if you need to append an ellipsis within the budget.

    Do they always agree? For UTF-8, yes -- UTF-8 is self-synchronising, so the
    truncated tail is always a partial character and never a valid different
    one. For UTF-16 or a stateful encoding they can differ, which is another
    reason to name the encoding explicitly rather than assume.
    """
    encoded = text.encode(encoding)
    if len(encoded) <= max_bytes:
        return text
    return encoded[:max_bytes].decode(encoding, errors="ignore")


def safe_truncate_walking(text: str, max_bytes: int, encoding: str = "utf-8") -> str:
    """Approach (b), for comparison."""
    used = 0
    out: list[str] = []
    for ch in text:
        size = len(ch.encode(encoding))
        if used + size > max_bytes:
            break
        out.append(ch)
        used += size
    return "".join(out)


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

    for fn in (safe_truncate, safe_truncate_walking):
        assert fn("café", 4) == "caf", fn("café", 4)
        assert fn("café", 5) == "café"  # é is 2 bytes: "café" is 5 bytes total
        assert fn("张伟好", 7) == "张伟"
        assert len(fn("张伟好", 7).encode("utf-8")) <= 7
        assert fn("plain", 100) == "plain"

    print("all encoding checks passed")


if __name__ == "__main__":
    verify()
