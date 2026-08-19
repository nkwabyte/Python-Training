# Module 36 — Capstone Milestone: Distributed URL Shortener & Analytics

**Level:** System Design  |  **Time:** P20  |  **Prerequisite:** Modules 31-35

---

## The Challenge

You will design, specify, implement, instrument, and load-test an end-to-end distributed URL Shortener and Real-Time Analytics service in Python.

### System Requirements & Target Load
1. **Shorten URL (`POST /shorten`):** Convert a long URL into a short Base62 token (`https://sho.rt/aX9zK`).
2. **Redirect URL (`GET /{token}`):** Redirect visitors with `302 Found` or `301 Moved Permanently` to the original URL in `< 10ms` p99 latency.
3. **Analytics Tracking:** Record timestamp, user-agent, and IP location for every click asynchronously without blocking the redirect response.
4. **Traffic Scale:**
   - 100 Million URLs created per month (~40 writes/sec average, 200 writes/sec peak).
   - 1 Billion URL redirections per month (~400 reads/sec average, 2,000 reads/sec peak).
   - 10:1 Read to Write ratio.
5. **Reliability:** 99.99% availability SLO, cache-aside read layer with Redis, database sharding, circuit breaking, and rate limiting.

---

## Stages

1. **Stage 1 — Requirements & Capacity Estimation:** [`exercises/ex01_system_requirements.md`](exercises/ex01_system_requirements.md)
2. **Stage 2 — Architecture Specification Document:** [`exercises/ex02_architecture_design.md`](exercises/ex02_architecture_design.md)
3. **Stage 3 — Runnable Service Implementation & Load Test:** [`exercises/ex03_service_implementation/`](exercises/ex03_service_implementation/)

---

## Solutions & Defense Guide

See [`solutions/SOLUTIONS.md`](solutions/SOLUTIONS.md) for the reference architecture, calculation checks, and defense answers.
