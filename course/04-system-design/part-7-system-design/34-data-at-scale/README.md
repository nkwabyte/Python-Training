# Module 34 — Data at Scale: Sharding, Hashing, and Streams

**Level:** System Design  |  **Time:** L4 E7  |  **Prerequisite:** Modules 27 (Databases), 31 (Design Fundamentals), D03 (Hash Tables)

---

## Why this module

When a database exceeds the capacity of a single physical server (RAM, disk I/O, storage), you must scale horizontally. Scaling data horizontally introduces distributed system challenges: partitioning strategies, consistent hashing, replication lag, distributed transactions, and event streaming (Kafka/Pulsar).

This module teaches you how to design data layers at scale, route queries across shards, maintain consistency under replication delay, and stream events reliably.

---

## 1. Database Scaling Ladder

```
Level 1: Vertical Scaling (Bigger hardware, NVMe SSDs, more RAM)
   |
Level 2: Read Replicas (Primary handles writes, Read Replicas handle reads)
   |
Level 3: Table Partitioning (Range/List partitioning on single DB engine)
   |
Level 4: Horizontal Sharding (Splitting rows across distinct database instances)
```

---

## 2. Sharding Strategies & Consistent Hashing

| Strategy | Mechanism | Pros & Cons |
|---|---|---|
| **Range-based** | Shard by ID range (e.g. 1-1M, 1M-2M) | Simple range queries; creates write hotspots on latest range |
| **Hash-based (`key % N`)** | Shard by modulo of key hash | Uniform write distribution; adding a shard requires moving $N-1/N$ keys |
| **Consistent Hashing** | Keys and servers mapped onto a virtual circular hash ring | Adding/removing a node relocates only $K/N$ keys on average |

---

## 3. Event Streaming with Log Semantics (Kafka)

An event stream is an append-only, ordered log of immutable records.
- **Partitions:** Unit of parallelism in Kafka. Ordering is guaranteed strictly *within* a partition, not across partitions.
- **Consumer Groups:** Multiple worker instances consuming from assigned partitions in parallel.

---

## Exercises

- `exercises/ex01_consistent_hash_ring.ipynb`: Consistent hashing ring with virtual nodes.
- `exercises/ex02_sharding_router.ipynb`: Range vs hash-based database sharding router.
- `exercises/ex03_event_sourcing_log.md`: Event log semantics, replay, and schema evolution worksheet.

---

## Solutions

See [`solutions/SOLUTIONS.md`](solutions/SOLUTIONS.md) for full design analysis.
