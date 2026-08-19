# Solutions & Capstone Defense Guide — Module 36: Capstone

## System Architecture Review

The reference implementation in `ex03_service_implementation` successfully meets the target scale:
- **Write Path:** Base62 ID encoding + Hash sharding provides collision-free token generation and scalable multi-shard writes.
- **Read Path:** Cache-Aside memory layer ensures p99 response times of under 5ms for hot keys, insulating database shards from traffic surges.
- **Analytics Path:** Click recording is decoupled from the user redirect response, avoiding latency overhead on the redirect path.

---

## Defense Questions & Model Answers

### Question 1: How do you prevent URL token collisions across multiple web nodes without distributed locks?
- **Model Answer:** Use a distributed ID generator (such as Twitter Snowflake or range allocation in Redis/Zookeeper) where each worker node is allocated a non-overlapping ID range (e.g. Node 1 gets IDs 1..1M, Node 2 gets 1M..2M). Encoding this monotonically increasing unique 64-bit integer directly into Base62 mathematically guarantees collision-free tokens without distributed coordination on every write.

### Question 2: What happens if a database shard fails?
- **Model Answer:** Each shard operates with an active primary and standby replica with automated failover. The service implements Circuit Breakers to fail-fast on queries destined for the degraded shard while all other shards continue serving requests unimpeded.
