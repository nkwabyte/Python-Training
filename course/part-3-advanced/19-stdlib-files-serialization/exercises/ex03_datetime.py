"""Exercise 19.3 — Twelve datetime puzzles.

Predict each answer before running. Every one has a timezone or DST trap.

Run:  python ex03_datetime.py
"""
from __future__ import annotations

import time
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

UTC = timezone.utc
LONDON = ZoneInfo("Europe/London")
NEW_YORK = ZoneInfo("America/New_York")
TOKYO = ZoneInfo("Asia/Tokyo")


def q01() -> None:
    # PREDICTION: can these be compared? What happens?
    naive = datetime(2026, 6, 1, 12, 0)
    aware = datetime(2026, 6, 1, 12, 0, tzinfo=UTC)
    try:
        print("q01", naive == aware, naive < aware)
    except TypeError as exc:
        print("q01 TypeError:", exc)


def q02() -> None:
    # PREDICTION: adding 24 hours across a DST boundary.
    # 2026-03-29 is when the UK springs forward.
    before = datetime(2026, 3, 29, 0, 30, tzinfo=LONDON)
    print("q02 +timedelta(hours=24):", before + timedelta(hours=24))
    print("q02 +timedelta(days=1):  ", before + timedelta(days=1))
    # Are those the same? Should they be? What did the user MEAN?


def q03() -> None:
    # PREDICTION: this local time occurs TWICE in 2026. Which one is this?
    ambiguous = datetime(2026, 10, 25, 1, 30, tzinfo=LONDON)
    print("q03", ambiguous, ambiguous.utcoffset())
    print("q03 fold=1:", ambiguous.replace(fold=1),
          ambiguous.replace(fold=1).utcoffset())
    # What is `fold`, and what should a booking system do with an ambiguous
    # time submitted by a user?


def q04() -> None:
    # PREDICTION: this local time NEVER occurs in 2026. What does Python do?
    nonexistent = datetime(2026, 3, 29, 1, 30, tzinfo=LONDON)
    print("q04", nonexistent, nonexistent.utcoffset())
    print("q04 in UTC:", nonexistent.astimezone(UTC))
    # Does it raise? Should it? What would a scheduled job at this time do?


def q05() -> None:
    # PREDICTION: same instant, three renderings.
    instant = datetime(2026, 8, 3, 12, 0, tzinfo=UTC)
    for tz, label in [(LONDON, "London"), (NEW_YORK, "New York"), (TOKYO, "Tokyo")]:
        print(f"q05 {label:<10}", instant.astimezone(tz))


def q06() -> None:
    # PREDICTION: is this the right way to get "now" in a timezone?
    print("q06 a:", datetime.now(TOKYO))
    print("q06 b:", datetime.now().replace(tzinfo=TOKYO))
    print("q06 c:", datetime.now(UTC).astimezone(TOKYO))
    # Two of these are correct and one is a bug. Which, and why?


def q07() -> None:
    # PREDICTION: what does subtracting two aware datetimes in DIFFERENT zones
    # give you?
    a = datetime(2026, 8, 3, 12, 0, tzinfo=LONDON)
    b = datetime(2026, 8, 3, 12, 0, tzinfo=TOKYO)
    print("q07", b - a, a == b)


def q08() -> None:
    # PREDICTION: round-tripping through isoformat.
    original = datetime(2026, 8, 3, 12, 0, 30, 123456, tzinfo=TOKYO)
    text = original.isoformat()
    back = datetime.fromisoformat(text)
    print("q08", text)
    print("q08 equal?", back == original, "| same tzinfo?", back.tzinfo == original.tzinfo)
    # It compares equal. Is anything lost? What?


def q09() -> None:
    # PREDICTION: date arithmetic on month boundaries.
    d = date(2026, 1, 31)
    print("q09 +30 days:", d + timedelta(days=30))
    try:
        print("q09 +1 month:", d.replace(month=2))
    except ValueError as exc:
        print("q09 replace(month=2):", exc)
    # There is no timedelta(months=1). Why not? What does "one month after
    # January 31" even mean?


def q10() -> None:
    # PREDICTION: which of these can go backwards?
    t1, p1, m1 = time.time(), time.perf_counter(), time.monotonic()
    time.sleep(0.01)
    t2, p2, m2 = time.time(), time.perf_counter(), time.monotonic()
    print(f"q10 time():        {t2 - t1:.6f}")
    print(f"q10 perf_counter():{p2 - p1:.6f}")
    print(f"q10 monotonic():   {m2 - m1:.6f}")
    # All three look the same here. Under what circumstance do they differ, and
    # which one would you use for a request timeout?


def q11() -> None:
    # PREDICTION: timestamps and naive datetimes.
    ts = 1785000000
    print("q11 utcfromtimestamp:", datetime.fromtimestamp(ts, UTC))
    print("q11 fromtimestamp   :", datetime.fromtimestamp(ts))
    # The second depends on the machine's timezone. Where does that bite?


def q12() -> None:
    # PREDICTION: storing a future appointment.
    # A user in London books a meeting for 2026-10-25 at 01:30 local time.
    # You store it as UTC. The DST rules for 2027 then change (governments do
    # this). What is wrong with what you stored?
    print("q12 -- no code. Answer in a comment:")
    print("     for a FUTURE local appointment, should you store UTC or")
    print("     local-time-plus-zone-name? Justify. Which does Google Calendar")
    print("     do, and why?")


if __name__ == "__main__":
    for fn in [q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11, q12]:
        fn()
