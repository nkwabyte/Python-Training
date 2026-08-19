# Solutions & Commentary — Module 26: HTTP, APIs, and Scraping

## Overview of Exercises

This module drilled HTTP client configuration, resilient retry transports with jitter, and asynchronous link crawling.

---

## Exercise 26.1: HTTP Client Basics

### Key Takeaways
- `httpx.Client` manages an internal connection pool across requests. In high-throughput systems, instantiating a client per request causes connection exhaustion and latency spikes from repeated TCP/TLS handshakes.
- `response.raise_for_status()` should be used when any non-2xx status represents an abnormal condition for the caller.

---

## Exercise 26.2: Asynchronous Web Crawler

### Solution Notes
- The crawler normalizes relative paths with `urllib.parse.urljoin` before checking `is_same_domain`.
- The `visited` set acts as both a deduplicator and a cycle detector.
- `asyncio.sleep` injects a polite crawl delay, ensuring concurrent worker routines do not overwhelm target origin servers.

---

## Exercise 26.3: Resilient Retry Transport

### Key Takeaways
- Exponential backoff (`base * 2^attempt`) paired with **full jitter** (`random.uniform(0, backoff)`) is standard industry practice. Fixed delays synchronize client retries and cause server-side queue overload upon recovery.
- Only retry transient errors (502, 503, 504) and rate limits (429). Never retry client errors (400 Bad Request, 401 Unauthorized, 404 Not Found) as repeated identical requests will produce identical failures.
