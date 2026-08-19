# Exercise 26.2 — Building an Asynchronous Web Crawler

**File:** `crawler.py`
**Estimated Time:** 45 minutes

---

## Background & Objective

Web crawling requires strict discipline:
1. **Domain boundaries:** Never crawl external domains inadvertently.
2. **Cycle detection:** URLs with circular cross-references (`/about` linking to `/` and vice-versa) must not cause infinite loops.
3. **Politeness:** Inject rate-limiting delays to avoid overloading the origin server.
4. **URL normalization:** Strip URL fragments (`#section`), normalize relative links (`/about` -> `https://example.com/about`), and discard invalid schemes (`mailto:`, `javascript:`).

In this exercise, you will inspect, complete, and test the `WebCrawler` class in `crawler.py`.

---

## Instructions

1. Open `crawler.py`.
2. Review the class methods:
   - `is_same_domain(url)`
   - `extract_links(html, current_url)`
   - `crawl_page(url, fetch_fn)`
3. Implement link deduplication so that already queued or visited links are not crawled twice.
4. Run the module directly to verify the self-test:
   ```bash
   python crawler.py
   ```
5. Ensure all assertions pass without error.
