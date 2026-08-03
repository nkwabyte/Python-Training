"""Exercise 03.3 — Text toolkit.

Nine utilities. Each has exactly one obvious right method in the standard
library; the exercise is choosing it rather than reaching for a regex or a loop.

For each function, after implementing it, write a one-line comment naming the
method you used and why it beats the alternatives.

Run:  python ex03_text_toolkit.py
"""

from __future__ import annotations


def normalise_key(raw: str) -> str:
    """'  User Name  ' -> 'user_name'. Trim, lowercase for COMPARISON (not
    display), collapse internal whitespace runs to single underscores."""
    raise NotImplementedError


def parse_header(line: str) -> tuple[str, str]:
    """'Content-Type: text/html; charset=utf-8'
       -> ('Content-Type', 'text/html; charset=utf-8')

    Split on the FIRST colon only. Values legitimately contain colons.
    Must not raise on a line with no colon -- return (line, '') instead."""
    raise NotImplementedError


def strip_extension(filename: str) -> str:
    """'report.final.pdf' -> 'report.final'.  'noext' -> 'noext'.
    '.hidden' -> '.hidden'  (a leading dot is not an extension)."""
    raise NotImplementedError


def is_url(text: str) -> bool:
    """True for http:// or https:// prefixes, case-insensitively.
    One call, no regex, no `or` chain."""
    raise NotImplementedError


def truncate_words(text: str, max_words: int) -> str:
    """Keep the first max_words words, appending '...' if anything was cut."""
    raise NotImplementedError


def to_snake_case(name: str) -> str:
    """'HTTPResponseCode' -> 'http_response_code'
       'getUserID'        -> 'get_user_id'
       'already_snake'    -> 'already_snake'

    The consecutive-capitals case is what makes this non-trivial. A regex is
    acceptable here; state why this one earns it and the others did not."""
    raise NotImplementedError


def mask_secret(text: str, keep: int = 4) -> str:
    """'sk-1234567890abcdef' -> '**************cdef'
    Keep the last `keep` characters. Handle strings shorter than keep."""
    raise NotImplementedError


def align_table(rows: list[tuple[str, ...]]) -> str:
    """Render rows as a plain-text table with columns aligned to their widest
    cell. No dependencies. Use the format mini-language, not manual padding."""
    raise NotImplementedError


def caseless_equal(a: str, b: str) -> bool:
    """Compare two strings ignoring case, CORRECTLY for non-English text.
    Must return True for ('straße', 'STRASSE'). This is the one where .lower()
    gives the wrong answer -- explain why in your comment."""
    raise NotImplementedError


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
