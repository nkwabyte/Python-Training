# Module 32 — Service Architecture and Concurrency Models

**Level:** System Design  |  **Time:** L4 E7  |  **Prerequisite:** Modules 21 (GIL & Processes), 22 (Asyncio), 31 (Design Fundamentals)

---

## Why this module

A single Python process cannot utilize all cores on a multi-core machine due to the Global Interpreter Lock (GIL). Scaling a Python web backend requires choosing the right process, worker, and event-loop concurrency model:
- **Sync Multi-Process (Gunicorn Sync Workers):** Forking multiple worker processes, suitable for CPU-heavy tasks or blocking legacy DB drivers.
- **Async Event-Loop (Uvicorn / Gunicorn with UvicornWorker):** High-concurrency I/O multiplexing.
- **Hybrid (Async with Threadpool Offloading):** Running fast async endpoints while offloading blocking operations (`run_in_executor` / Starlette threadpool) to prevent loop stalling.

This module teaches you how to architect services, handle graceful shutdowns, manage backpressure, and decompose monoliths into modular services.

---

## 1. Process & Worker Topologies

```
                     [ Reverse Proxy (Nginx / Cloudflare) ]
                                       |
                   +-------------------+-------------------+
                   | (Unix Domain Socket / TCP)            |
                   v                                       v
      [ Gunicorn Master (PID 100) ]           [ Gunicorn Master (PID 200) ]
        |            |            |
        v            v            v
    [Worker 1]   [Worker 2]   [Worker 3] (Worker Recycle after --max-requests)
    (Uvicorn)    (Uvicorn)    (Uvicorn)
```

### Worker Sizing Formula
- **CPU-bound:** `Workers = (2 * Num_CPUs) + 1`
- **I/O-bound (Async):** `Workers = (2 to 4) * Num_CPUs` (with thousands of active coroutines per worker).

---

## 2. Backpressure and Load Shedding

When arrival rate exceeds capacity ($R_{in} > R_{process}$), unbounded buffering increases queue latency until requests time out while still consuming server CPU.

**Rule:** Drop or reject excess requests immediately with `503 Service Unavailable` or `429 Too Many Requests` rather than letting queues grow unbounded.

---

## Exercises

- `exercises/ex01_worker_concurrency.ipynb`: Benchmarking threadpool workers vs async event loops.
- `exercises/ex02_backpressure_queue.ipynb`: Bounded queue implementation with load shedding.
- `exercises/ex03_service_boundaries.md`: Architectural decomposition design worksheet.

---

## Solutions

See [`solutions/SOLUTIONS.md`](solutions/SOLUTIONS.md) for full solution analysis.
