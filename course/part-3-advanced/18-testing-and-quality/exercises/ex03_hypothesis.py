"""Exercise 18.3 — Six real bugs, findable by property testing.

Every function below has a bug that example-based tests miss and a property
test finds in seconds. Write the property, watch it fail, read the shrunk
counterexample, then fix the function.

Run:  pip install hypothesis && pytest ex03_hypothesis.py
"""
from __future__ import annotations

import math
from decimal import Decimal
from typing import Any

from hypothesis import given
from hypothesis import strategies as st


# --- 1 ------------------------------------------------------------------------
def normalise_whitespace(text: str) -> str:
    """Collapse runs of whitespace to single spaces and trim."""
    return " ".join(text.split(" ")).strip()


# --- 2 ------------------------------------------------------------------------
def chunk(items: list[Any], size: int) -> list[list[Any]]:
    """Split into chunks of at most `size`."""
    return [items[i:i + size] for i in range(0, len(items), size)]


# --- 3 ------------------------------------------------------------------------
def percentage(part: float, whole: float) -> float:
    """part as a percentage of whole, rounded to one decimal place."""
    return round(part / whole * 100, 1)


# --- 4 ------------------------------------------------------------------------
def merge_sorted(a: list[int], b: list[int]) -> list[int]:
    """Merge two sorted lists into one sorted list."""
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            result.append(a[i]); i += 1
        else:
            result.append(b[j]); j += 1
    result.extend(a[i:])
    return result


# --- 5 ------------------------------------------------------------------------
def truncate(text: str, limit: int) -> str:
    """Truncate to `limit` characters, appending '...' if it was cut."""
    if len(text) <= limit:
        return text
    return text[:limit - 3] + "..."


# --- 6 ------------------------------------------------------------------------
def split_evenly(total: int, parts: int) -> list[int]:
    """Split `total` into `parts` whole numbers summing to total."""
    base = total // parts
    result = [base] * parts
    result[0] += total - base * parts
    return result


# --- write the properties ------------------------------------------------------
#
# For each function, the property to assert (and the bug it exposes):
#
#  1  normalise_whitespace  -> the result contains no tab, newline, or double
#                              space, for ANY input string
#  2  chunk                 -> flattening the chunks reproduces the input
#                              exactly, for any list and any size
#  3  percentage            -> ??? think about what must be true. What input
#                              makes this raise, and what makes it lie?
#  4  merge_sorted          -> the output is sorted AND is a permutation of
#                              the two inputs combined
#  5  truncate              -> len(result) <= limit, for any text and limit
#  6  split_evenly          -> sum(result) == total, and every part is within
#                              1 of every other part
#
# Write each with @given, run it, and record the SHRUNK counterexample
# Hypothesis reports. That minimal example is the real deliverable -- write it
# down for each of the six before fixing anything.


@given(st.text())
def test_normalise_whitespace(text: str) -> None:
    result = normalise_whitespace(text)
    assert "\t" not in result
    assert "\n" not in result
    assert "  " not in result


# TODO: write the other five.


ANSWERS = """
Record the shrunk counterexample for each:

1  normalise_whitespace :
2  chunk                :
3  percentage           :
4  merge_sorted         :
5  truncate             :
6  split_evenly         :

Then answer:
- which of the six would you have found with example-based tests?
- which counterexample would you never have thought to write by hand?
- for bug 4, what does the SECOND property (permutation) catch that the first
  (sorted) does not? Construct an implementation that passes one and fails the
  other.
"""
