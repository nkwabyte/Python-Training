# Module 35 — Reliability, Observability, and Security

**Level:** System Design  |  **Time:** L4 E6  |  **Prerequisite:** Modules 16 (Error Handling), 25 (Automation & Logging), 31 (Design Fundamentals)

---

## Why this module

In production, failures are not exceptions to normal behavior—they are guaranteed daily occurrences. Designing resilient systems requires:
1. **Failure isolation:** Preventing local failures from cascading (Circuit Breakers, Bulkheads, Timeouts).
2. **Traffic regulation:** Protecting internal services against bursts (Token Bucket Rate Limiters).
3. **Observability:** Structured JSON logs, telemetry metrics (Prometheus), and distributed tracing (OpenTelemetry).
4. **Security Hardening:** OWASP Top 10 defenses, dependency auditing, and secrets management.

---

## 1. The Circuit Breaker Pattern

A circuit breaker monitors downstream call failures and transitions across three states:
```
           +-------------------------+
           |                         |
           v    failure >= threshold |
      [ CLOSED ] ----------------> [ OPEN ]
         ^                           |
         | success                   | recovery timeout elapsed
         |                           v
         +------------------- [ HALF-OPEN ]
                                (1 trial call)
```

- **CLOSED:** Requests execute normally. Failures increment counter.
- **OPEN:** Fails fast immediately without attempting the downstream call.
- **HALF-OPEN:** Permits a single trial call. If successful, resets to `CLOSED`. If failing, trips back to `OPEN`.

---

## 2. Rate Limiting: Token Bucket

The Token Bucket algorithm accumulates tokens at a constant rate up to a fixed burst capacity:
- Each incoming request consumes 1 token.
- If tokens are available, request is processed.
- If bucket is empty, request is rejected with `429 Too Many Requests`.

---

## 3. The Three Pillars of Observability

| Pillar | Question It Answers | Python Standard |
|---|---|---|
| **Logs** | *Why did a specific request fail?* | Structured JSON logging with `logging` / `structlog` |
| **Metrics** | *Is the overall system healthy right now?* | Prometheus client metrics (`Counter`, `Gauge`, `Histogram`) |
| **Traces** | *Where was time spent across microservices?* | OpenTelemetry spans with shared `trace_id` |

---

## Exercises

- `exercises/ex01_circuit_breaker.ipynb`: 3-state Circuit Breaker implementation with fail-fast timeouts.
- `exercises/ex02_token_bucket_ratelimiter.ipynb`: Thread-safe / async Token Bucket rate limiter.
- `exercises/ex03_structured_logging.ipynb`: Structured JSON log formatter with correlation ID propagation.

---

## Solutions

See [`solutions/SOLUTIONS.md`](solutions/SOLUTIONS.md) for full design commentary.
