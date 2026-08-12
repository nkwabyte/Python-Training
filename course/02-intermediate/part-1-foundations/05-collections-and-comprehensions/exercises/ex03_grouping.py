"""Exercise 05.3 — An analytics pipeline over realistic data.

You have a week of web request logs. Answer eight questions about them using
the right container each time. No pandas -- the point is to know what pandas is
doing for you before you let it (Module 29).

Run:  python ex03_grouping.py
"""

from __future__ import annotations

import random
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class Request:
    day: date
    path: str
    user: str
    status: int
    ms: int
    bytes_out: int


def generate(n: int = 5000, seed: int = 7) -> list[Request]:
    rng = random.Random(seed)
    start = date(2026, 7, 27)
    paths = ["/", "/login", "/api/items", "/api/items/1", "/search",
             "/static/app.js", "/admin"]
    users = [f"u{i}" for i in range(120)] + ["anon"] * 40
    out = []
    for _ in range(n):
        path = rng.choices(paths, weights=[30, 10, 25, 15, 12, 20, 2])[0]
        status = rng.choices([200, 200, 200, 301, 404, 500],
                             weights=[70, 10, 5, 5, 8, 2])[0]
        out.append(Request(
            day=start + timedelta(days=rng.randrange(7)),
            path=path,
            user=rng.choice(users),
            status=status,
            ms=max(1, int(rng.lognormvariate(3.2, 0.9))),
            bytes_out=rng.randrange(200, 50_000),
        ))
    return out


# TODO 1 -----------------------------------------------------------------------
def status_counts(requests: Iterable[Request]) -> dict[int, int]:
    """How many requests per status code, most common first.
    Container: ?"""
    raise NotImplementedError


# TODO 2 -----------------------------------------------------------------------
def requests_by_day(requests: Iterable[Request]) -> dict[date, list[Request]]:
    """Group requests by day. Container: ?"""
    raise NotImplementedError


# TODO 3 -----------------------------------------------------------------------
def top_paths(requests: Iterable[Request], k: int = 3) -> list[tuple[str, int]]:
    """The k most requested paths with their counts.
    There is a one-method answer. Find it."""
    raise NotImplementedError


# TODO 4 -----------------------------------------------------------------------
def slowest_per_path(requests: Iterable[Request]) -> dict[str, int]:
    """The worst latency seen for each path.
    Do it in ONE pass. A dict of running maxima, not a group-then-max."""
    raise NotImplementedError


# TODO 5 -----------------------------------------------------------------------
def percentiles(values: list[int], ps: tuple[float, ...] = (50, 95, 99)) -> dict[float, int]:
    """Compute percentile latencies.

    Sort once, index. Then answer in a comment:
      - why is p95 a more useful SLO than the mean?
      - why does averaging the p95 of each server give the wrong overall p95?
    (Both questions come back in Module 35.)
    """
    raise NotImplementedError


# TODO 6 -----------------------------------------------------------------------
def users_seeing_errors(requests: Iterable[Request]) -> set[str]:
    """The set of users who received any 5xx response."""
    raise NotImplementedError


# TODO 7 -----------------------------------------------------------------------
def churned_users(requests: Iterable[Request], first_day: date,
                  last_day: date) -> set[str]:
    """Users active on first_day but NOT on last_day.

    This is set difference. Write it as one expression using set algebra, and
    note in a comment what the loop-based version would have cost."""
    raise NotImplementedError


# TODO 8 -----------------------------------------------------------------------
def daily_report(requests: Iterable[Request]) -> str:
    """Render an aligned table: one row per day, with columns for request
    count, error rate as a percentage, p95 latency, and total megabytes out.

    Sort by day. Use the format mini-language for alignment (Module 03), not
    manual padding. Requests may arrive as an ITERATOR, so consume it once.
    """
    raise NotImplementedError


def verify() -> None:
    reqs = generate()

    counts = status_counts(reqs)
    assert sum(counts.values()) == len(reqs)
    assert list(counts)[0] == 200, "most common status should come first"

    by_day = requests_by_day(reqs)
    assert len(by_day) == 7
    assert sum(len(v) for v in by_day.values()) == len(reqs)

    top = top_paths(reqs, 3)
    assert len(top) == 3 and top[0][1] >= top[1][1] >= top[2][1]

    slowest = slowest_per_path(reqs)
    assert set(slowest) <= {r.path for r in reqs}

    p = percentiles([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    assert p[50] <= p[95] <= p[99]

    errs = users_seeing_errors(reqs)
    assert all(isinstance(u, str) for u in errs)

    churned = churned_users(reqs, date(2026, 7, 27), date(2026, 8, 2))
    assert isinstance(churned, set)

    report = daily_report(reqs)
    assert report.count("\n") >= 7, report

    print("all checks passed\n")
    print(report)


if __name__ == "__main__":
    verify()
