"""Distributed URL Shortener and Analytics Service implementation."""

from __future__ import annotations

import string
import time
from typing import Dict, Optional


BASE62_ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase


def encode_base62(num: int) -> str:
    """Encode an integer ID into a Base62 token."""
    if num == 0:
        return BASE62_ALPHABET[0]
    result = []
    base = len(BASE62_ALPHABET)
    while num > 0:
        num, rem = divmod(num, base)
        result.append(BASE62_ALPHABET[rem])
    return "".join(reversed(result))


class URLShortenerService:
    """URL Shortener with in-memory DB sharding, Cache-Aside, and asynchronous click recording."""

    def __init__(self, num_shards: int = 4, cache_ttl: float = 300.0) -> None:
        self.num_shards = num_shards
        self.cache_ttl = cache_ttl
        self.db_shards: list[dict[str, str]] = [{} for _ in range(num_shards)]
        self.cache: dict[str, tuple[str, float]] = {}  # token -> (url, expire_at)
        self.analytics_log: list[dict] = []
        self._id_counter: int = 1000000

    def _get_shard_id(self, token: str) -> int:
        return hash(token) % self.num_shards

    def shorten_url(self, long_url: str) -> str:
        """Create a shortened token from an auto-incrementing counter and write to designated shard."""
        self._id_counter += 1
        token = encode_base62(self._id_counter)
        shard_id = self._get_shard_id(token)
        self.db_shards[shard_id][token] = long_url
        
        # Populate cache on write
        now = time.time()
        self.cache[token] = (long_url, now + self.cache_ttl)
        return token

    def resolve_url(self, token: str, user_agent: str = "Mozilla/5.0") -> Optional[str]:
        """Resolve short token via Cache-Aside and log analytics event."""
        now = time.time()
        long_url = None
        
        # 1. Check Cache
        if token in self.cache:
            cached_url, expire_at = self.cache[token]
            if now < expire_at:
                long_url = cached_url
            else:
                del self.cache[token]

        # 2. On Cache Miss, read from appropriate shard
        if long_url is None:
            shard_id = self._get_shard_id(token)
            long_url = self.db_shards[shard_id].get(token)
            if long_url:
                self.cache[token] = (long_url, now + self.cache_ttl)

        # 3. Asynchronously record click analytics if found
        if long_url:
            self.analytics_log.append({
                "token": token,
                "timestamp": now,
                "user_agent": user_agent
            })

        return long_url
