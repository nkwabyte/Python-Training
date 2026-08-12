"""Exercise 22.1 — Twelve asyncio predictions.

Predict the OUTPUT ORDER and the TOTAL TIME for each before running.

REQUIRES PYTHON 3.11+ for asyncio.TaskGroup (q07), except* (q07) and
asyncio.timeout (q10). On 3.10 those three are skipped with a message; the
other nine run unchanged. Check with:  python --version

Run:  python ex01_basics.py
"""

from __future__ import annotations

import asyncio
import sys
import time

HAS_311 = sys.version_info >= (3, 11)


async def work(name: str, seconds: float) -> str:
    print(f"      start {name}")
    await asyncio.sleep(seconds)
    print(f"      end   {name}")
    return name


async def q01() -> None:
    # PREDICTION: order? total time?
    await work("a", 0.2)
    await work("b", 0.2)


async def q02() -> None:
    # PREDICTION:
    await asyncio.gather(work("a", 0.2), work("b", 0.2))


async def q03() -> None:
    # PREDICTION: what does this print, and what warning appears?
    work("never-awaited", 0.1)
    await asyncio.sleep(0.05)


async def q04() -> None:
    # PREDICTION: does creating the task start it? When does it run?
    task = asyncio.create_task(work("task", 0.1))
    print("      created the task")
    await asyncio.sleep(0)          # what does sleep(0) do?
    print("      after sleep(0)")
    await task


async def q05() -> None:
    # PREDICTION: total time? Which finishes first?
    results = await asyncio.gather(work("slow", 0.3), work("fast", 0.1))
    print("      results:", results)


async def q06() -> None:
    # PREDICTION: what happens to "b" when "a" raises?
    async def failing() -> None:
        await asyncio.sleep(0.05)
        raise ValueError("a failed")

    try:
        await asyncio.gather(failing(), work("b", 0.3))
    except ValueError as exc:
        print(f"      caught {exc}; is b still running?")
    await asyncio.sleep(0.4)


async def q07() -> None:
    # PREDICTION: same, but with TaskGroup. What is different?
    if not HAS_311:
        print("      SKIPPED: TaskGroup and except* need Python 3.11+")
        return
    # The 3.11+ body lives in a separate file so this module still imports on
    # 3.10 -- `except*` is a SYNTAX error, not a runtime one, so a version
    # check cannot guard it in the same file. That is worth noticing: syntax
    # introduced by a new version cannot be feature-detected inline.
    from _tg_311 import q07_taskgroup      # type: ignore[import-not-found]
    await q07_taskgroup(work)


async def q08() -> None:
    # PREDICTION: THE BIG ONE. What is the total time, and why?
    async def blocking() -> None:
        print("      blocking start")
        time.sleep(0.3)              # NOT asyncio.sleep
        print("      blocking end")

    start = time.perf_counter()
    await asyncio.gather(blocking(), work("a", 0.1), work("b", 0.1))
    print(f"      total {time.perf_counter() - start:.2f}s")


async def q09() -> None:
    # PREDICTION: and with to_thread?
    def blocking() -> None:
        time.sleep(0.3)

    start = time.perf_counter()
    await asyncio.gather(asyncio.to_thread(blocking), work("a", 0.1))
    print(f"      total {time.perf_counter() - start:.2f}s")


async def q10() -> None:
    # PREDICTION: does the cleanup run? Does the timeout fire?
    async def stubborn() -> None:
        try:
            await asyncio.sleep(10)
        except asyncio.CancelledError:
            print("      stubborn: caught cancellation, cleaning up")
            # note: NOT re-raised
    if not HAS_311:
        print("      partial: asyncio.timeout needs 3.11+; using wait_for")
        try:
            await asyncio.wait_for(stubborn(), timeout=0.1)
            print("      wait_for returned -- the timeout did NOT cancel it")
        except asyncio.TimeoutError:
            print("      TimeoutError raised")
        return
    try:
        async with asyncio.timeout(0.1):
            await stubborn()
        print("      timeout did NOT fire")
    except TimeoutError:
        print("      TimeoutError raised")


async def q11() -> None:
    # PREDICTION: single-threaded. Can this race?
    counter = 0

    async def increment() -> None:
        nonlocal counter
        for _ in range(1000):
            current = counter
            await asyncio.sleep(0)      # a suspension point
            counter = current + 1

    await asyncio.gather(*(increment() for _ in range(5)))
    print(f"      counter = {counter} (expected 5000)")


async def q12() -> None:
    # PREDICTION: what does the semaphore change about the timing?
    sem = asyncio.Semaphore(2)

    async def limited(name: str) -> None:
        async with sem:
            await work(name, 0.1)

    start = time.perf_counter()
    await asyncio.gather(*(limited(f"t{i}") for i in range(6)))
    print(f"      total {time.perf_counter() - start:.2f}s for 6 tasks, limit 2")


async def main() -> None:
    for fn in [q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11, q12]:
        print(f"\n{fn.__name__}")
        start = time.perf_counter()
        await fn()
        print(f"    ({time.perf_counter() - start:.2f}s)")


if __name__ == "__main__":
    asyncio.run(main())
