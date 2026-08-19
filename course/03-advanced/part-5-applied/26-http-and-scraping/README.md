# Module 26 — HTTP, APIs, and Scraping

**Time budget:** 4 hours lesson, 7 hours exercises
**Prerequisite:** Modules 07 (CLI), 16 (Error Handling), 19 (Serialization & Files), 22 (Asyncio)

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

Modern software spends most of its time talking to other software across a network.
Treating HTTP requests as simple magic function calls (`requests.get(url)`) works
until the network is slow, an API returns 429 Too Many Requests, connections leak,
or a page renders dynamically.

This module teaches you to treat HTTP as an explicit protocol: understanding connection
lifecycles, headers, query parameters, authentication methods, status codes, timeouts,
retries with backoff, and respectful web scraping.

---

## 1. HTTP as a Protocol: The Request-Response Cycle

Every HTTP interaction is an exchange of plain text messages governed by RFC specifications:

```
CLIENT REQUEST:
GET /api/v1/users?limit=10 HTTP/1.1
Host: api.example.com
User-Agent: DataSyncWorker/1.0
Accept: application/json
Authorization: Bearer sec_tok_998a

SERVER RESPONSE:
HTTP/1.1 200 OK
Date: Wed, 19 Aug 2026 12:00:00 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 184
Retry-After: 60

{"data": [...], "has_more": false}
```

### Core HTTP Status Codes Every Engineer Must Know

| Code Range | Category | Key Codes to Handle |
|---|---|---|
| **2xx** | Success | `200 OK`, `201 Created`, `204 No Content` |
| **3xx** | Redirection | `301 Moved Permanently`, `302 Found`, `304 Not Modified` |
| **4xx** | Client Error | `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `429 Too Many Requests` |
| **5xx** | Server Error | `500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable`, `504 Gateway Timeout` |

---

## 2. Modern HTTP Clients in Python: `httpx`

While `requests` remains popular, `httpx` is the modern standard offering:
1. Identical sync API to `requests`.
2. Native `asyncio` support with `httpx.AsyncClient`.
3. HTTP/2 protocol support.
4. Strict, explicit timeout handling by default.

### Connection Reuse via Client Context Manager

```python
import httpx

# Anti-pattern: creating a new client/connection per request
# for url in urls:
#     resp = httpx.get(url)  # Performs DNS, TCP handshake, TLS handshake EVERY time!

# Pattern: Use a Client session for connection pooling and header persistence
with httpx.Client(
    base_url="https://api.github.com",
    headers={"Accept": "application/vnd.github.v3+json", "User-Agent": "MyDataApp/1.0"},
    timeout=httpx.Timeout(10.0, connect=3.0)
) as client:
    response = client.get("/users/octocat")
    response.raise_for_status()
    user_data = response.json()
    print(f"User: {user_data['name']}, Public Repos: {user_data['public_repos']}")
```

---

## 3. Resilient Requests: Timeouts, Retries, and Backoff

Networks fail unpredictably. A production client **always** enforces timeouts and handles transient failures.

```python
import time
import httpx
import logging

logger = logging.getLogger(__name__)

def fetch_with_backoff(
    client: httpx.Client,
    url: str,
    max_retries: int = 3,
    base_delay: float = 0.5
) -> httpx.Response:
    """Fetch a URL with exponential backoff and jitter on 5xx and 429 status codes."""
    for attempt in range(1, max_retries + 1):
        try:
            response = client.get(url)
            
            # If rate limited (429), respect Retry-After header if present
            if response.status_code == 429:
                retry_after = float(response.headers.get("Retry-After", base_delay * (2 ** attempt)))
                logger.warning("Rate limited (429). Backing off for %.2fs", retry_after)
                time.sleep(retry_after)
                continue
            
            # Retry transient server errors
            if response.status_code in (502, 503, 504):
                delay = base_delay * (2 ** attempt)
                logger.warning("Transient error %d. Retry %d/%d in %.2fs", response.status_code, attempt, max_retries, delay)
                time.sleep(delay)
                continue
            
            response.raise_for_status()
            return response
            
        except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.NetworkError) as err:
            if attempt == max_retries:
                logger.error("Request failed permanently after %d attempts: %s", max_retries, err)
                raise
            delay = base_delay * (2 ** attempt)
            logger.warning("Network issue (%s). Retrying in %.2fs", type(err).__name__, delay)
            time.sleep(delay)

    raise RuntimeError("Unreachable")
```

---

## 4. Web Scraping: Parsing, Politeness, and Ethics

Scraping is extracting data from HTML documents designed for human browsers.

### The Scraping Rules of Engagement

1. **Check `robots.txt`**: Respect `User-agent`, `Disallow`, and `Crawl-delay` directives.
2. **Set a clear `User-Agent`**: Include contact information or application identity.
3. **Rate limit client-side**: Never bombard a third-party server with concurrent requests.
4. **Cache aggressively**: If scraping static pages, cache responses locally to avoid re-fetching.

### HTML Parsing Example with BeautifulSoup

```python
from bs4 import BeautifulSoup
import httpx

html_content = """
<html>
  <body>
    <div class="product-card" data-id="101">
      <h2 class="title">Wireless Noise-Canceling Headphones</h2>
      <span class="price">$149.99</span>
      <span class="stock in-stock">In Stock</span>
    </div>
    <div class="product-card" data-id="102">
      <h2 class="title">Mechanical Gaming Keyboard</h2>
      <span class="price">$89.50</span>
      <span class="stock out-of-stock">Sold Out</span>
    </div>
  </body>
</html>
"""

soup = BeautifulSoup(html_content, "html.parser")
products = []

for card in soup.select("div.product-card"):
    product_id = card.get("data-id")
    title_elem = card.select_one("h2.title")
    price_elem = card.select_one("span.price")
    stock_elem = card.select_one("span.stock")
    
    title = title_elem.get_text(strip=True) if title_elem else "Unknown"
    price = float(price_elem.get_text(strip=True).replace("$", "")) if price_elem else 0.0
    in_stock = "in-stock" in stock_elem.get("class", []) if stock_elem else False
    
    products.append({"id": product_id, "title": title, "price": price, "in_stock": in_stock})

print(products)
```

---

## Exercises

- `exercises/ex01_http_client.ipynb`: Interactive REST client, query params, auth, and pagination.
- `exercises/ex02_crawler/`: Multi-page web crawler with link extraction, rate-limiting, and error tolerance. (Contains `crawler.py` and student instruction `README.md`).
- `exercises/ex03_retry_session.ipynb`: Custom transport and resilient HTTP session design.

---

## Solutions

See [`solutions/SOLUTIONS.md`](solutions/SOLUTIONS.md) for full commentary and solution explanations.
