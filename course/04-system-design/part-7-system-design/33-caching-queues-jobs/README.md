# Module 33 — Caching, Queues, and Background Jobs

**Level:** System Design  |  **Time:** L4 E7  |  **Prerequisite:** Modules 27 (Databases), 31 (Design Fundamentals), 32 (Service Architecture)

---

## Why this module

Databases are the common bottleneck in web systems. To scale beyond a few hundred requests per second, you must move hot reads into in-memory caches (Redis/Memcached) and move slow writes, batch jobs, and third-party integrations into asynchronous task queues (Celery, ARQ, Redis Streams).

This module covers caching topology, cache-aside, write-through, write-behind, cache stampede mitigation (probabilistic early expiration and single-flight locking), task queues, retry policies, and idempotency guarantees.

---

## 1. Caching Strategies

| Pattern | Write Path | Read Path | Pros & Cons |
|---|---|---|---|
| **Cache-Aside (Lazy)** | App writes to DB, evicts key from cache | App reads cache; on miss, reads DB and populates cache | Most flexible; cache holds only active keys; initial read penalty |
| **Write-Through** | App writes to cache; cache synchronously writes to DB | App reads cache | Strong consistency; slower write latency |
| **Write-Behind (Async)** | App writes to cache; cache queues async flush to DB | App reads cache | Ultra-fast writes; risk of data loss on cache node crash |

---

## 2. The Cache Stampede (Thundering Herd) Problem

When a hot key (e.g. homepage banner) expires under heavy traffic, thousands of concurrent requests miss simultaneously and overwhelm the database.

### Mitigation Strategies
1. **Single-Flight Request Coalescing:** Mutex lock ensuring only one worker queries the database while other requests await the result.
2. **Probabilistic Early Expiration (XFetch):** Background re-computation triggered before the key formally expires based on read frequency and computation cost.

---

## 3. Idempotent Background Task Workers

Distributed queues guarantee **at-least-once delivery**, meaning tasks can be delivered multiple times during network partition retries.

**Rule:** Every task handler must accept an `idempotency_key`. The handler checks a durable store before executing side-effects, guaranteeing that duplicates are safely ignored.

---

## Exercises

- `exercises/ex01_cache_aside_pattern.ipynb`: Cache-aside implementation with TTL and invalidation.
- `exercises/ex02_stampede_singleflight.ipynb`: Single-flight lock preventing thundering herd spikes.
- `exercises/ex03_task_queue_idempotency.ipynb`: Asynchronous queue worker with idempotency guarantees.

---

## Solutions

See [`solutions/SOLUTIONS.md`](solutions/SOLUTIONS.md) for full commentary and design analysis.
