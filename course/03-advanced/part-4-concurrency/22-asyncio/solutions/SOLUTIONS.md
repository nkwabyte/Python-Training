# Solutions & Commentary — Module 22: Asyncio

## Key Takeaways
- Never execute blocking I/O (e.g. `time.sleep`, `requests.get`) inside async coroutines; use `asyncio.sleep` or `loop.run_in_executor`.
- In Python 3.11+, use `asyncio.TaskGroup` for structured concurrency instead of `asyncio.gather`.
- Handle task cancellation cleanly with `try...except asyncio.CancelledError`.
