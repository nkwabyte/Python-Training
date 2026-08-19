# Solutions & Commentary — Module 33: Caching, Queues, and Background Jobs

## Overview of Exercises

This module drilled Cache-Aside lifecycle management, single-flight stampede prevention, and idempotent worker execution.

---

## Exercise 33.1: Cache-Aside with Invalidation

### Key Takeaways
- Always invalidate (delete) the cache key upon write mutation rather than updating the cache value directly. Updating the cache directly creates race conditions where two concurrent writes overwrite each other in reverse order.

---

## Exercise 33.2: Single-Flight Stampede Prevention

### Key Takeaways
- Coalescing concurrent reads into a single in-flight `asyncio.Task` drops database load from $N$ queries down to 1 query during cache refresh cycles.

---

## Exercise 33.3: Idempotent Task Workers

### Key Takeaways
- Idempotency stores must be queried before executing external side effects (e.g. charging cards, sending emails).
- Store operation status and results alongside the idempotency key so repeat invocations return the exact original response.
