# Exercise 36.3 — Distributed URL Shortener Service Implementation & Load Test

**Directory:** `ex03_service_implementation/`
**Files:** `service.py`, `load_test.py`, `test_service.py`
**Estimated Time:** 1 hour

---

## Background & Objective

In this capstone implementation, you explore the full URL Shortener service written in Python:
- **Base62 ID Encoding:** Translates sequential database row IDs into short URL tokens.
- **Database Sharding:** Hashes tokens across multiple independent shard dictionaries.
- **Cache-Aside Layer:** Stores hot tokens in an in-memory cache with TTL expiration.
- **Analytics Event Logging:** Captures request metadata and user-agent information.

---

## Instructions

1. Run the test suite:
   ```bash
   pytest test_service.py
   ```
2. Execute the load test benchmark:
   ```bash
   python load_test.py
   ```
3. Observe the write and read throughput metrics and verify how shard distribution remains balanced across shards.
