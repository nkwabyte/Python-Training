"""Load testing benchmark for URL Shortener Service."""

import time
from service import URLShortenerService


def run_load_test(num_urls: int = 1000, num_redirects: int = 10000) -> None:
    print(f"=== URL Shortener Load Test ===")
    print(f"Generating {num_urls} URLs and executing {num_redirects} redirect resolutions...")
    
    svc = URLShortenerService(num_shards=4, cache_ttl=60.0)
    
    # 1. Benchmark Writes (Shorten)
    t0 = time.perf_counter()
    tokens = [svc.shorten_url(f"https://example.com/article/{i}") for i in range(num_urls)]
    write_duration = time.perf_counter() - t0
    write_qps = num_urls / write_duration
    print(f"Writes: {num_urls} URLs created in {write_duration:.4f}s ({write_qps:,.1f} ops/sec)")
    
    # 2. Benchmark Reads (Resolve with Cache-Aside)
    t1 = time.perf_counter()
    for i in range(num_redirects):
        target_token = tokens[i % num_urls]
        url = svc.resolve_url(target_token)
        assert url is not None
    read_duration = time.perf_counter() - t1
    read_qps = num_redirects / read_duration
    print(f"Reads: {num_redirects} redirects resolved in {read_duration:.4f}s ({read_qps:,.1f} ops/sec)")
    
    print(f"Analytics captured: {len(svc.analytics_log)} click events")
    print(f"Database shard item counts: {[len(s) for s in svc.db_shards]}")
    print("=== Load Test Passed Successfully ===")


if __name__ == "__main__":
    run_load_test()
