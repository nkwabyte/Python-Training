# Exercise 32.3 — Decomposing a Monolith into Services

**Estimated Time:** 40 minutes

---

## Scenario

An e-commerce monolith is experiencing high checkout latency during flash sales. The monolithic system handles:
1. **User Authentication & Profiles**
2. **Product Catalog Browsing** (Read-heavy, 95% traffic)
3. **Cart & Checkout Processing** (Write-heavy, transactional)
4. **Order Notification & Email Dispatch** (Slow external network I/O)
5. **Analytics & Recommendations** (Heavy CPU / batch computation)

---

## Tasks

### Task 1: Identify Service Boundaries
Determine which domains should remain together and which should be extracted into separate services.

**Recommended Decomposition:**
1. **Catalog Service:** Read-heavy, heavily cached in Redis/CDN, separate read replicas.
2. **Order & Checkout Service:** High-consistency transactional database (PostgreSQL), strict ACID constraints.
3. **Notification Worker:** Asynchronous background consumer off a message queue (RabbitMQ / Redis stream).
4. **Analytics Pipeline:** Decoupled event emission to a data lake / ClickHouse.

### Task 2: Failure Domain Analysis
If the Notification Service or external email provider goes down, should a user's checkout fail?
- *Answer:* No. Decoupling notification dispatch via asynchronous task queues ensures checkout succeeds immediately upon payment capture, isolating external provider outages from the critical revenue path.
