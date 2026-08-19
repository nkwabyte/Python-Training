# Solutions & Commentary — Module 34: Data at Scale

## Overview of Exercises

This module covered horizontal database sharding, consistent hashing with virtual nodes, and partitioned event stream processing.

---

## Exercise 34.1: Consistent Hashing Ring

### Key Takeaways
- Virtual nodes (multiple tokens mapped per physical server) smooth out hash distribution irregularities and prevent uneven hotspot allocation across physical nodes.
- When nodes are added or removed, `bisect` finds the immediate successor key with $O(\log M)$ binary search complexity on the token ring.

---

## Exercise 34.2: Shard Routing & Scatter-Gather

### Key Takeaways
- Direct point lookups by shard key (e.g. `user_id`) route with $O(1)$ efficiency directly to the target shard.
- Non-shard-key queries (such as counting all users or searching by email when partitioned by user ID) require scatter-gather execution across all shards, which degrades performance and scalability.
