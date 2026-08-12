"""Solution 05.1 — Predict, then measure."""

from __future__ import annotations

import random
import sys
import timeit
from collections import deque

SIZES = [1_000, 2_000, 4_000, 8_000, 16_000]


def measure(setup: str, stmt: str, sizes: list[int], number: int = 2000) -> list[float]:
    """Return microseconds per operation at each size.

    Uses MIN of several repeats, not the mean. This is the standard practice
    and the reason is worth internalising: timing noise is one-sided. Nothing
    can make your code run faster than it actually can, but anything on the
    machine -- another process, a GC pause, CPU frequency scaling, a cache
    miss -- can make it slower. So the minimum is the closest estimate of the
    true cost, and the mean is a measure of how busy your laptop was.
    (Module 23 returns to this.)
    """
    out = []
    for n in sizes:
        best = min(timeit.repeat(stmt, setup.format(n=n), number=number, repeat=5))
        out.append(best / number * 1e6)
    return out


def growth_ratio(times: list[float]) -> list[float]:
    return [b / a if a else float("inf") for a, b in zip(times, times[1:])]


def classify(ratios: list[float]) -> str:
    """Doubling n each step, so the mean ratio names the class."""
    if not ratios:
        return "?"
    mean = sum(ratios) / len(ratios)
    if mean < 1.4:
        return "O(1)"
    if mean < 2.6:
        return "O(n) or O(n log n)"
    if mean < 5.0:
        return "O(n^2)"
    return "worse than O(n^2)"


# `number` is deliberately SMALL for the mutating operations. Each repetition
# of `lst.insert(0, 1)` makes the list one element longer, so 20000 repetitions
# against a list of 1000 would be measuring a list of 21000 by the end -- the
# measurement would destroy the thing being measured. 200 repetitions against
# n >= 1000 changes the size by at most 20 percent, which is tolerable.
CASES: list[tuple[str, str, str, int]] = [
    # label,                setup,                                stmt,             number
    ("list[i]",             "lst = list(range({n}))",             "lst[len(lst)//2]", 20000),
    ("list.append",         "lst = list(range({n}))",             "lst.append(1)",    200),
    ("list.insert(0,x)",    "lst = list(range({n}))",             "lst.insert(0, 1)", 200),
    ("list.pop()",          "lst = list(range({n}))",             "lst.pop()",        200),
    ("list.pop(0)",         "lst = list(range({n}))",             "lst.pop(0)",       200),
    ("x in list (missing)", "lst = list(range({n}))",             "-1 in lst",        200),
    ("x in set (missing)",  "s = set(range({n}))",                "-1 in s",          20000),
    ("x in dict (missing)", "d = dict.fromkeys(range({n}))",      "-1 in d",          20000),
    ("dict[k] = v",         "d = dict.fromkeys(range({n}))",      "d[1] = 1",         20000),
    ("deque.appendleft",    "from collections import deque\nd = deque(range({n}))", "d.appendleft(1)", 200),
    ("sorted(shuffled)",    "import random\nrandom.seed(0)\nlst = list(range({n}))\nrandom.shuffle(lst)",
                            "sorted(lst)",     50),
    ("lst[:] full copy",    "lst = list(range({n}))",             "lst[:]",           2000),
]


def run_all() -> None:
    """Measurement traps handled here:

    (a) DESTRUCTIVE ops. `lst.pop()` shortens the list on every repetition,
        and `lst.insert(0, x)` lengthens it. Run 20000 repetitions against a
        list of 1000 and you are no longer measuring a list of 1000 -- you have
        destroyed the thing you were measuring. The fix used here is a small
        `number` relative to n, so the size changes by at most a fifth.
        timeit cannot express "reset between repetitions" without putting the
        reset inside the timed statement, where it would itself be measured.
        Knowing this limitation is most of what separates a benchmark you can
        believe from one you cannot.

    (b) Setup is NOT timed, so building the structure is free.

    (c) MEMBERSHIP must search for a MISSING element. `0 in lst` returns
        immediately and measures nothing at all.

    (d) SORTING an already-sorted list is O(n) with Timsort -- it detects the
        existing run and stops. Always shuffle first.
    """
    print(f"{'operation':<22}" + "".join(f"{n:>10,}" for n in SIZES) + f"{'class':>22}")
    print("-" * (22 + 10 * len(SIZES) + 22))
    for label, setup, stmt, number in CASES:
        times = measure(setup, stmt, SIZES, number)
        ratios = growth_ratio(times)
        cells = "".join(f"{t:>10.3f}" for t in times)
        print(f"{label:<22}{cells}{classify(ratios):>22}")
    print("\n(numbers are microseconds per operation)")


def amortization_demo() -> None:
    """Find the resize events by watching sys.getsizeof."""
    lst: list[int] = []
    last = sys.getsizeof(lst)
    jumps: list[tuple[int, int]] = []
    for i in range(100_000):
        lst.append(i)
        size = sys.getsizeof(lst)
        if size != last:
            jumps.append((i + 1, size))
            last = size

    print("\namortization: reallocations while appending 100,000 items")
    print(f"  {len(jumps)} reallocations for 100,000 appends "
          f"({len(jumps) / 100_000:.3%} of appends pay the copy)")
    shown = jumps[:6] + [("...", 0)] + jumps[-3:]
    for n, size in shown:
        print(f"    at n={n!s:>7}  allocated {size if size else '':>9}")

    growth = [b[0] / a[0] for a, b in zip(jumps[2:], jumps[3:])]
    if growth:
        print(f"  mean growth factor between reallocations: "
              f"{sum(growth) / len(growth):.3f}")

    print(
        "\n  WHY 'AMORTIZED O(1)' IS HONEST RATHER THAN A FUDGE:\n"
        "  the list grows geometrically, so the number of reallocations for n\n"
        "  appends is O(log n), and the TOTAL copying work across all of them\n"
        "  is a geometric series that sums to O(n). Divide O(n) total work by n\n"
        "  appends and you get O(1) per append, on average, over ANY sequence\n"
        "  of appends -- not just on lucky ones. That is what amortized means,\n"
        "  and it is a worst-case guarantee over a sequence, not an average\n"
        "  over random inputs.\n"
        "  (CPython's exact growth factor is an implementation detail and has\n"
        "  changed between versions. The geometric SHAPE is what matters.)"
    )


def crossover_point() -> None:
    """Where does set beat list for membership, INCLUDING build cost?"""
    print("\ncrossover: k membership tests against n items, set build included")
    print(f"  {'n':>6}{'k':>6}{'list ms':>12}{'set ms':>12}  winner")
    rng = random.Random(0)
    for n in [1, 2, 4, 8, 16, 32, 64, 128, 512, 4096]:
        data = list(range(n))
        k = 10
        probes = [rng.randrange(n * 3) for _ in range(k)]

        t_list = timeit.timeit(lambda: [p in data for p in probes], number=2000)
        t_set = timeit.timeit(
            lambda: [p in set(data) for p in probes], number=2000)
        t_set_once = timeit.timeit(
            lambda: [p in s for s in [set(data)] for p in probes], number=2000)
        winner = "set" if t_set_once < t_list else "list"
        print(f"  {n:>6}{k:>6}{t_list * 1000:>12.2f}{t_set_once * 1000:>12.2f}  {winner}")

    print(
        "\n  The crossover is low -- typically a few dozen items for k=10 --\n"
        "  and it moves LEFT as k grows, because the set build is paid once\n"
        "  while the list scans are paid k times. Rebuilding the set INSIDE the\n"
        "  loop (the second timing above, not shown) is the common mistake and\n"
        "  makes the set version SLOWER at every size. Build the set once,\n"
        "  outside the loop. That single habit is most of what container\n"
        "  awareness buys you in practice."
    )


if __name__ == "__main__":
    run_all()
    amortization_demo()
    crossover_point()
