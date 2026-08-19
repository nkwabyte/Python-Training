# Capstone Stage 1 — Requirements & Capacity Estimation

**Estimated Time:** 45 minutes

---

## 1. Traffic Estimations
- **Monthly writes:** 100 Million URLs
- **Write QPS (Queries Per Second):**
  $$\text{Write QPS} = \frac{100,000,000}{30 \times 24 \times 3600} \approx 38.6 \approx 40 \text{ writes/sec}$$
- **Peak Write QPS (5x):** $40 \times 5 = 200 \text{ writes/sec}$
- **Monthly reads (10:1 ratio):** 1 Billion redirects
- **Read QPS:**
  $$\text{Read QPS} = \frac{1,000,000,000}{30 \times 24 \times 3600} \approx 386 \approx 400 \text{ reads/sec}$$
- **Peak Read QPS (5x):** $400 \times 5 = 2,000 \text{ reads/sec}$

---

## 2. Storage Capacity (5-Year Horizon)
- **Record Size:**
  - `id`: 8 bytes (int64)
  - `short_token`: 7 bytes (Base62)
  - `long_url`: 500 bytes (varchar)
  - `created_at`: 8 bytes (timestamp)
  - `user_id`: 8 bytes
  - *Total per row with indexing overhead:* ~600 bytes
- **5-Year URL Storage:**
  $$100,000,000 \times 12 \times 5 \times 600 \text{ bytes} = 6 \text{ Billion} \times 600 \text{ B} = 3.6 \text{ TB}$$
- *Conclusion:* 3.6 TB comfortably fits on a modern SSD cluster with read replication and horizontal sharding.

---

## 3. Cache Estimation (80/20 Rule)
- 20% of the daily hot URLs generate 80% of daily read traffic.
- Daily read requests: $\approx 33.3 \text{ Million}$
- 20% hot URLs per day: $0.20 \times 33.3 \text{ M} = 6.66 \text{ Million URLs}$
- Cache Memory Required:
  $$6.66 \text{ Million} \times 600 \text{ bytes} \approx 4 \text{ GB of RAM}$$
- *Conclusion:* A single Redis master-replica pair with 8 GB to 16 GB of RAM easily caches all hot URL redirects in memory!
