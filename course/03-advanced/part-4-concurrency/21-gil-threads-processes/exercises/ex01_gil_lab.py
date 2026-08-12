"""Exercise 21.1 — Measure the GIL.

Four workloads, three execution strategies. Predict all twelve results BEFORE
running. The predictions are the exercise; the numbers merely grade them.

Run:  python ex01_gil_lab.py
"""
from __future__ import annotations

import hashlib
import math
import time
import urllib.request
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

N_TASKS = 8

PREDICTIONS = """
Fill this in BEFORE running. Write the expected speedup versus serial.

                        | serial | threads | processes
  pure-Python CPU       |  1.0x  |         |
  hashlib (C, releases) |  1.0x  |         |
  time.sleep (fake I/O) |  1.0x  |         |
  file reads (real I/O) |  1.0x  |         |

Then, for each cell, write ONE WORD explaining why: "GIL", "released",
"waiting", "pickling", "startup".
"""


def cpu_pure(n: int) -> float:
    """Pure Python arithmetic. The GIL applies fully."""
    total = 0.0
    for i in range(1, 2_000_000):   # tune this until serial takes ~2s
        total += math.sqrt(i) / (i + n)
    return total


def cpu_c_extension(n: int) -> str:
    """hashlib releases the GIL for large inputs."""
    data = bytes(2_000_000)
    h = hashlib.sha256()
    for _ in range(4):
        h.update(data)
    return h.hexdigest()


def fake_io(n: int) -> int:
    """time.sleep releases the GIL. This is the cleanest demonstration."""
    time.sleep(0.25)
    return n


def real_io(n: int) -> int:
    """Reading a file. Adjust the path if needed."""
    total = 0
    with open("/usr/share/dict/words" if _has_words() else __file__, "rb") as fh:
        for _ in range(20):
            fh.seek(0)
            total += len(fh.read())
    return total


def _has_words() -> bool:
    import os
    return os.path.exists("/usr/share/dict/words")


def run_serial(fn, tasks):  # type: ignore[no-untyped-def]
    return [fn(i) for i in tasks]


def run_threads(fn, tasks):  # type: ignore[no-untyped-def]
    with ThreadPoolExecutor(max_workers=len(tasks)) as ex:
        return list(ex.map(fn, tasks))


def run_processes(fn, tasks):  # type: ignore[no-untyped-def]
    with ProcessPoolExecutor(max_workers=len(tasks)) as ex:
        return list(ex.map(fn, tasks))


def measure(label: str, fn) -> None:  # type: ignore[no-untyped-def]
    tasks = list(range(N_TASKS))
    times: dict[str, float] = {}
    for name, runner in [("serial", run_serial), ("threads", run_threads),
                         ("processes", run_processes)]:
        start = time.perf_counter()
        runner(fn, tasks)
        times[name] = time.perf_counter() - start

    base = times["serial"]
    print(f"\n  {label}")
    for name, elapsed in times.items():
        print(f"    {name:<10} {elapsed:6.2f}s   {base / elapsed:5.2f}x")


# TODO 1: run it, and compare against your predictions. How many did you get?

# TODO 2: explain the hashlib row. Look at CPython's Modules/_hashopenssl.c or
#         the docs -- above what input size does hashlib release the GIL, and
#         why is there a threshold at all rather than always releasing?

# TODO 3: the processes column for fake_io is probably NOT 8x. Explain the gap.
#         Then reduce the sleep to 0.001 and re-run. What happened to the
#         process speedup, and what does that tell you about when process
#         overhead dominates?

# TODO 4: sys.setswitchinterval(0.000001) and re-run the pure-Python CPU row
#         with threads. Predict first: faster, slower, or the same? Explain the
#         result in terms of what a switch costs.

# TODO 5: write a FIFTH workload that is half CPU and half I/O, and find the
#         strategy that wins. Then explain why "it depends" is the correct
#         answer to "should I use threads or processes".


if __name__ == "__main__":
    print(PREDICTIONS)
    print(f"running {N_TASKS} tasks per workload...")
    measure("pure-Python CPU", cpu_pure)
    measure("hashlib (C extension)", cpu_c_extension)
    measure("time.sleep (fake I/O)", fake_io)
    measure("file reads (real I/O)", real_io)
