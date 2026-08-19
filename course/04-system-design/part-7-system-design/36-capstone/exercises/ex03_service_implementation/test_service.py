"""Unit tests for Capstone URL Shortener."""

import time
import pytest
from service import URLShortenerService, encode_base62


def test_base62_encoding():
    assert encode_base62(0) == "0"
    assert encode_base62(61) == "Z"
    assert encode_base62(62) == "10"
    assert len(encode_base62(1000000)) >= 4


def test_shorten_and_resolve():
    svc = URLShortenerService(num_shards=2, cache_ttl=10.0)
    token = svc.shorten_url("https://python.org")
    assert token is not None
    
    resolved = svc.resolve_url(token, user_agent="PyTestRunner/1.0")
    assert resolved == "https://python.org"
    assert len(svc.analytics_log) == 1
    assert svc.analytics_log[0]["token"] == token


def test_cache_expiration():
    svc = URLShortenerService(num_shards=2, cache_ttl=0.05)
    token = svc.shorten_url("https://fastapi.tiangolo.com")
    
    time.sleep(0.08)  # Let cache expire
    resolved = svc.resolve_url(token)
    assert resolved == "https://fastapi.tiangolo.com"
