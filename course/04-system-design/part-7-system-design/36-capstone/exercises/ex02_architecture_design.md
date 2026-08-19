# Capstone Stage 2 — Architecture Specification Document

---

## 1. System Topology Diagram

```
                        [ Cloudflare Anycast / Global CDN ]
                                        |
                          [ Load Balancer (Round Robin) ]
                                        |
             +--------------------------+--------------------------+
             |                                                     |
    [ Web API Service (Pod 1) ]                           [ Web API Service (Pod 2) ]
    (FastAPI + Uvicorn Async)                             (FastAPI + Uvicorn Async)
             |                                                     |
             +--------------------------+--------------------------+
                                        |
                 +----------------------+----------------------+
                 |                                             |
          (Cache-Aside Reads)                         (Write Mutations)
                 |                                             |
                 v                                             v
        [ Redis Cluster ]                           [ Sharded Database Cluster ]
        (Hot URLs, TTL=24h)                         (PostgreSQL Shards 0..3)
                 |
                 | (Asynchronous Click Stream)
                 v
        [ Task Queue / Stream ]
                 |
                 v
        [ Analytics Ingestion Worker ] -> [ ClickHouse / Data Warehouse ]
```

---

## 2. Token Generation Strategy: Base62 Encoding
- Alphabet: `[a-z, A-Z, 0-9]` (62 characters).
- With 7 characters: $62^7 \approx 3.52 \text{ Trillion}$ unique URLs, far exceeding our 5-year requirement of 6 Billion URLs.
- Using a distributed counter / Snowflake ID generator + Base62 ensures zero collisions without expensive DB uniqueness queries.
