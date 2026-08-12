"""Solution 05.3 — An analytics pipeline, no pandas."""

from __future__ import annotations

import random
from collections import Counter, defaultdict
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
            path=path, user=rng.choice(users), status=status,
            ms=max(1, int(rng.lognormvariate(3.2, 0.9))),
            bytes_out=rng.randrange(200, 50_000),
        ))
    return out


def status_counts(requests: Iterable[Request]) -> dict[int, int]:
    """Counter. It counts, and most_common() gives the ordering for free."""
    return dict(Counter(r.status for r in requests).most_common())


def requests_by_day(requests: Iterable[Request]) -> dict[date, list[Request]]:
    """defaultdict(list). The canonical grouping tool."""
    groups: dict[date, list[Request]] = defaultdict(list)
    for r in requests:
        groups[r.day].append(r)
    return dict(groups)
    # Returning dict(groups), not the defaultdict itself: a caller who writes
    # groups[some_missing_day] would otherwise silently INSERT an empty list
    # and get no KeyError. Never leak a defaultdict across an API boundary.


def top_paths(requests: Iterable[Request], k: int = 3) -> list[tuple[str, int]]:
    """One method: Counter.most_common(k). Internally it uses heapq.nlargest
    for small k, so it is O(n log k), not a full sort."""
    return Counter(r.path for r in requests).most_common(k)


def slowest_per_path(requests: Iterable[Request]) -> dict[str, int]:
    """One pass, running maxima.

    The group-then-max version builds every group in memory first:
        {p: max(r.ms for r in rs) for p, rs in requests_by_path.items()}
    That is O(n) memory for a result that is O(distinct paths). Running maxima
    is O(1) memory per key and works on a stream. On a log file larger than
    RAM, only this version runs at all -- which is Module 14's lesson in
    advance.
    """
    worst: dict[str, int] = {}
    for r in requests:
        if r.ms > worst.get(r.path, -1):
            worst[r.path] = r.ms
    return worst


def percentiles(values: list[int], ps: tuple[float, ...] = (50, 95, 99)) -> dict[float, int]:
    """Sort once, index. (The nearest-rank method; numpy uses interpolation by
    default, which gives slightly different answers -- worth knowing when your
    dashboard and your script disagree.)

    WHY p95 BEATS THE MEAN AS AN SLO: the mean is dominated by the bulk of fast
    requests and hides the tail entirely. A service where 95 percent of
    requests take 20ms and 5 percent take 8 seconds has a mean around 420ms --
    a number that describes no actual request and conceals that one user in
    twenty is having an unusable experience. The tail is where users live: a
    page making 20 backend calls hits the p95 of at least one of them most of
    the time.

    WHY YOU CANNOT AVERAGE PERCENTILES: a percentile is a position in a sorted
    distribution, not an additive quantity. Averaging the p95 of two servers
    gives a number with no meaning -- if server A serves 10 requests and server
    B serves 10,000, their p95s are not comparable, and even with equal traffic
    the combined p95 depends on the SHAPES of the two distributions. To get a
    real overall p95 you must merge the underlying observations (or their
    histograms, which is exactly why Prometheus stores histogram buckets rather
    than precomputed quantiles).
    """
    if not values:
        raise ValueError("percentiles of an empty sequence")
    ordered = sorted(values)
    out: dict[float, int] = {}
    for p in ps:
        idx = min(len(ordered) - 1, int(round(p / 100 * len(ordered) + 0.5)) - 1)
        out[p] = ordered[max(0, idx)]
    return out


def users_seeing_errors(requests: Iterable[Request]) -> set[str]:
    return {r.user for r in requests if r.status >= 500}


def churned_users(requests: Iterable[Request], first_day: date,
                  last_day: date) -> set[str]:
    """Set difference in one expression.

    The loop version needs two passes, an inner membership test against a list
    (O(n*m)), and about eight lines. This is O(n) with the set built in the
    same pass, and it says what it means.
    """
    reqs = list(requests)
    early = {r.user for r in reqs if r.day == first_day}
    late = {r.user for r in reqs if r.day == last_day}
    return early - late


def daily_report(requests: Iterable[Request]) -> str:
    """One pass over a possibly-iterator input, then format."""
    per_day: dict[date, list[Request]] = defaultdict(list)
    for r in requests:                       # consume the iterator ONCE
        per_day[r.day].append(r)

    header = f"{'day':<12}{'reqs':>8}{'err%':>8}{'p95 ms':>9}{'MB out':>10}"
    lines = [header, "-" * len(header)]
    for day in sorted(per_day):
        rs = per_day[day]
        errors = sum(1 for r in rs if r.status >= 400)
        p95 = percentiles([r.ms for r in rs], (95,))[95]
        mb = sum(r.bytes_out for r in rs) / 1_048_576
        lines.append(
            f"{day.isoformat():<12}{len(rs):>8}{errors / len(rs):>8.1%}"
            f"{p95:>9}{mb:>10.1f}"
        )
    return "\n".join(lines)


def verify() -> None:
    reqs = generate()

    counts = status_counts(reqs)
    assert sum(counts.values()) == len(reqs)
    assert list(counts)[0] == 200

    by_day = requests_by_day(reqs)
    assert len(by_day) == 7
    assert sum(len(v) for v in by_day.values()) == len(reqs)

    top = top_paths(reqs, 3)
    assert len(top) == 3 and top[0][1] >= top[1][1] >= top[2][1]

    slowest = slowest_per_path(reqs)
    assert set(slowest) <= {r.path for r in reqs}

    p = percentiles([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    assert p[50] <= p[95] <= p[99]

    assert all(isinstance(u, str) for u in users_seeing_errors(reqs))
    assert isinstance(churned_users(reqs, date(2026, 7, 27), date(2026, 8, 2)), set)

    report = daily_report(reqs)
    assert report.count("\n") >= 7
    print("all checks passed\n")
    print(report)


if __name__ == "__main__":
    verify()
