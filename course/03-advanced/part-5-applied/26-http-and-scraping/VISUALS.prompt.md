# Visual Companion Prompt — Module 26: HTTP, APIs, and Scraping

## Video Steering Prompt
> Generate a comprehensive visual explanation of the HTTP protocol and client architecture in Python. Illustrate the TCP handshake, TLS negotiation, and HTTP/1.1 vs HTTP/2 connection pooling with persistent keep-alive sockets. Contrast naive unpooled requests against session-based client architectures. Diagram the exponential backoff algorithm with full jitter under server rate-limiting (429) and transient 503 errors. Finally, illustrate DOM tree traversal and CSS selector matching during HTML scraping workflows.

## Mind Map & Concept Hierarchy
- **HTTP Fundamentals**
  - Request/Response format (Headers, Body, Status Codes)
  - HTTP Verbs: GET, POST, PUT, PATCH, DELETE
  - Status Families: 2xx (Success), 3xx (Redirect), 4xx (Client), 5xx (Server)
- **Client Architecture**
  - Connection Pooling & Keep-Alive
  - Synchronous vs Asynchronous (`httpx.Client` vs `httpx.AsyncClient`)
  - Timeouts: Connect, Read, Write, Pool timeouts
- **Resilience Engineering**
  - Transient error detection (502, 503, 504, 429)
  - Exponential Backoff with Jitter
  - Circuit breaking and rate limiting
- **Web Scraping**
  - `robots.txt` compliance & politeness
  - DOM parsing with BeautifulSoup / selectolax
  - Data sanitization and extraction pipelines

## Accuracy Guardrails
- Ensure timeouts are taught as multidimensional (connect vs read vs write) rather than a single vague timeout.
- Explicitly emphasize that `requests.get()` without session creates new TCP sockets each call.
- Distinguish client errors (4xx - non-retryable except 429) from server errors (5xx - retryable).
