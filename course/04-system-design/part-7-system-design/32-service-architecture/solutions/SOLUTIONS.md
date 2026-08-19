# Solutions & Commentary — Module 32: Service Architecture

## Overview of Exercises

This module covered Gunicorn/Uvicorn worker concurrency models, bounded queuing with load shedding, and microservice boundary decomposition.

---

## Exercise 32.1: Worker Concurrency

### Key Takeaways
- Async coroutines handle thousands of concurrent idle I/O connections with minimal memory overhead compared to thread stacks (which allocate 8MB virtual memory per thread).
- Any CPU-bound operation inside an async event loop will block all other concurrent coroutines on that worker; CPU work must be delegated to process pools (`ProcessPoolExecutor`).

---

## Exercise 32.2: Backpressure and Bounded Queues

### Key Takeaways
- Bounded queues prevent unbounded memory allocation and keep p99 latency predictable by failing fast when capacity limits are breached.
