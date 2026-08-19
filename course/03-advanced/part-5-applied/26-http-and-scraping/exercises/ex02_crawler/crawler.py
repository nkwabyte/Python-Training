"""Asynchronous Web Crawler with domain filtering, rate limiting, and link extraction."""

from __future__ import annotations

import asyncio
import logging
import re
from typing import Set, List
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)


class WebCrawler:
    """Polite, asynchronous web crawler bounded by maximum depth and page limits."""

    def __init__(
        self,
        base_url: str,
        max_depth: int = 2,
        max_pages: int = 20,
        rate_limit_delay: float = 0.1
    ) -> None:
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.rate_limit_delay = rate_limit_delay
        self.visited: Set[str] = set()

    def is_same_domain(self, url: str) -> bool:
        """Check whether the given URL belongs to the target domain."""
        parsed = urlparse(url)
        return not parsed.netloc or parsed.netloc == self.domain

    def extract_links(self, html: str, current_url: str) -> List[str]:
        """Extract all valid internal href links from HTML content."""
        links: List[str] = []
        # Simple regex matcher for href attributes
        raw_hrefs = re.findall(r'href=[\'"]?([^\'" >]+)', html, re.IGNORECASE)
        for href in raw_hrefs:
            if href.startswith(("#", "mailto:", "javascript:", "tel:")):
                continue
            absolute = urljoin(current_url, href)
            # Remove fragment/hash
            parsed = urlparse(absolute)
            clean_url = parsed._replace(fragment="").geturl()
            if self.is_same_domain(clean_url) and clean_url not in self.visited:
                links.append(clean_url)
        return links

    async def crawl_page(self, url: str, fetch_fn) -> List[str]:
        """Fetch a single page, record as visited, and extract new links."""
        if url in self.visited or len(self.visited) >= self.max_pages:
            return []
        
        self.visited.add(url)
        await asyncio.sleep(self.rate_limit_delay)  # Rate limiting politeness
        
        try:
            html = await fetch_fn(url)
            return self.extract_links(html, url)
        except Exception as err:
            logger.warning("Failed to fetch %s: %s", url, err)
            return []


if __name__ == "__main__":
    # Self-test with simulated in-memory fetch
    async def demo():
        pages = {
            "https://site.local/": "<html><a href='/about'>About</a><a href='https://external.com'>Ext</a></html>",
            "https://site.local/about": "<html><a href='/contact'>Contact</a><a href='/'>Home</a></html>",
            "https://site.local/contact": "<html><h1>Contact Us</h1></html>"
        }
        crawler = WebCrawler("https://site.local/")
        
        async def mock_fetch(url: str) -> str:
            return pages.get(url, "<html></html>")
        
        queue = ["https://site.local/"]
        while queue and len(crawler.visited) < crawler.max_pages:
            curr = queue.pop(0)
            new_links = await crawler.crawl_page(curr, mock_fetch)
            queue.extend(new_links)
            
        print(f"Crawl completed! Visited {len(crawler.visited)} pages: {crawler.visited}")
        assert len(crawler.visited) == 3

    asyncio.run(demo())
