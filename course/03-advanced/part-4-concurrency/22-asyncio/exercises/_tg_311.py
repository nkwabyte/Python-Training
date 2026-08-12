"""The 3.11+ half of exercise 22.1 q07.

Separate file because `except*` is a SYNTAX error on 3.10 -- a version check in
the same module cannot guard it, since the module fails to compile before any
code runs. (Module 01: syntax is checked before execution.)
"""
from __future__ import annotations

import asyncio


async def q07_taskgroup(work) -> None:  # type: ignore[no-untyped-def]
    async def failing() -> None:
        await asyncio.sleep(0.05)
        raise ValueError("a failed")

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(failing())
            tg.create_task(work("b", 0.3))
    except* ValueError as eg:
        print(f"      ExceptionGroup with {len(eg.exceptions)} error(s)")
        print("      note: b was CANCELLED, not left running")
    await asyncio.sleep(0.4)
