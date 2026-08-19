# Solutions & Commentary — Module 35: Reliability, Observability, and Security

## Overview of Exercises

This module drilled Circuit Breakers, Token Bucket rate limiting, and structured JSON telemetry.

---

## Exercise 35.1: Circuit Breaker

### Key Takeaways
- Circuit breakers prevent thread pool and socket exhaustion when downstream dependencies suffer total outages. Failing fast in microsecond time keeps frontend services responsive and protects downstream services during restart/recovery.

---

## Exercise 35.2: Token Bucket Rate Limiter

### Key Takeaways
- Refilling tokens lazily during `.allow()` calls using `time.monotonic()` elapsed math avoids background timer threads or continuous tick overhead.

---

## Exercise 35.3: Structured JSON Logging

### Key Takeaways
- Attaching a consistent `correlation_id` / `trace_id` to every log statement emitted across service boundaries allows aggregating all log events for a single user interaction in distributed log analyzers (Elasticsearch, Loki).
