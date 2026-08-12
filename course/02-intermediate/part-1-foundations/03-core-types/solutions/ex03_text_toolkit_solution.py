"""Solution 03.3 — Text toolkit. One right method each."""

from __future__ import annotations

import re


def normalise_key(raw: str) -> str:
    # .split() with NO argument splits on ANY whitespace run and drops empties,
    # which handles trimming and collapsing in one call. .split(" ") would not.
    return "_".join(raw.split()).lower()


def parse_header(line: str) -> tuple[str, str]:
    # .partition() always returns a 3-tuple and never raises, unlike
    # .split(":", 1) which returns a 1-list when there is no colon, forcing the
    # caller to check the length. Partition makes the no-separator case fall
    # out for free.
    name, sep, value = line.partition(":")
    return (name.strip(), value.strip()) if sep else (line, "")


def strip_extension(filename: str) -> str:
    # .rpartition() from the right handles multi-dot names. The `if head` guard
    # is what makes ".hidden" work: partitioning it gives ("", ".", "hidden"),
    # an empty head, meaning the dot was leading, not an extension separator.
    head, sep, _tail = filename.rpartition(".")
    return head if sep and head else filename


def is_url(text: str) -> bool:
    # startswith accepts a TUPLE of prefixes. One call, no `or` chain, no regex.
    return text.lower().startswith(("http://", "https://"))


def truncate_words(text: str, max_words: int) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + "..."


_SNAKE_BOUNDARY = re.compile(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")


def to_snake_case(name: str) -> str:
    """A regex earns its place HERE and did not in the others.

    The rule is a lookaround condition on a boundary between characters --
    "split where a lowercase or digit is followed by an uppercase, OR where an
    uppercase is followed by an uppercase-then-lowercase". That second clause
    is what turns HTTPResponse into HTTP + Response rather than H+T+T+P+...,
    and expressing it with str methods would take a character loop with two
    lookahead conditions. The regex states the rule directly.

    The other eight functions have a single obvious method; reaching for a
    regex there would be slower, harder to read, and easier to get wrong.
    """
    if "_" in name and name.islower():
        return name
    return _SNAKE_BOUNDARY.sub("_", name).lower()


def mask_secret(text: str, keep: int = 4) -> str:
    if len(text) <= keep:
        return "*" * len(text)
    return "*" * (len(text) - keep) + text[-keep:]


def align_table(rows: list[tuple[str, ...]]) -> str:
    if not rows:
        return ""
    # zip(*rows) transposes; max over each column gives its width.
    widths = [max(len(cell) for cell in col) for col in zip(*rows, strict=False)]
    lines = []
    for row in rows:
        # The nested-brace form takes the width from a variable at format time.
        cells = [f"{cell:<{w}}" for cell, w in zip(row, widths, strict=False)]
        lines.append("  ".join(cells).rstrip())
    return "\n".join(lines)


def caseless_equal(a: str, b: str) -> bool:
    """.casefold(), not .lower().

    .lower() does a simple per-character mapping. The German sharp s, ß, has no
    single uppercase form -- its uppercase is the two characters SS. .lower()
    leaves ß alone, so "straße".lower() != "STRASSE".lower(). .casefold()
    applies the full Unicode case-folding algorithm, which maps ß to "ss", and
    handles Greek final sigma, Turkish dotted I, Cherokee, and others the same
    way.

    Rule: .lower() for DISPLAY, .casefold() for COMPARISON.
    """
    return a.casefold() == b.casefold()


def verify() -> None:
    assert normalise_key("  User  Name ") == "user_name"
    assert normalise_key("ID") == "id"

    assert parse_header("Content-Type: text/html; charset=utf-8") == (
        "Content-Type", "text/html; charset=utf-8")
    assert parse_header("garbage") == ("garbage", "")

    assert strip_extension("report.final.pdf") == "report.final"
    assert strip_extension("noext") == "noext"
    assert strip_extension(".hidden") == ".hidden"

    assert is_url("HTTPS://example.com") is True
    assert is_url("ftp://example.com") is False

    assert truncate_words("one two three four", 2) == "one two..."
    assert truncate_words("one two", 5) == "one two"

    assert to_snake_case("HTTPResponseCode") == "http_response_code"
    assert to_snake_case("getUserID") == "get_user_id"
    assert to_snake_case("already_snake") == "already_snake"

    assert mask_secret("sk-1234567890abcdef") == "***************cdef"
    assert mask_secret("ab") == "**"

    table = align_table([("name", "role"), ("Ada", "engineer"), ("Bo", "PM")])
    assert "Ada   engineer" in table, table  # col width comes from "name"

    assert caseless_equal("straße", "STRASSE") is True
    assert caseless_equal("abc", "ABC") is True
    assert caseless_equal("abc", "abd") is False

    print("all text toolkit checks passed")


if __name__ == "__main__":
    verify()
