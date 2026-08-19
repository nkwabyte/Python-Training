# Exercise 34.3 — Event Streaming, Partitioning, and Consumer Groups

**Estimated Time:** 35 minutes

---

## Scenario: Order Fulfillment Event Pipeline

An event stream topic `orders.events` receives order lifecycle events:
- `OrderPlaced`
- `PaymentCaptured`
- `OrderShipped`
- `OrderDelivered`

The topic has 8 partitions and must process 20,000 events/second across a cluster of consumers.

---

## Analysis Questions

### Question 1: Partition Key Selection
Which field should be chosen as the partition key for `orders.events`?
- (A) `event_type`
- (B) `order_id`
- (C) `timestamp`

**Evaluation:**
- Selecting `(B) order_id` ensures that all events for a given order are routed to the exact same partition in deterministic chronological order. Partitioning by `event_type` would interleave events from different orders and lose the per-order causal ordering guarantee.

### Question 2: Consumer Group Scaling
If a topic has 8 partitions, what is the maximum number of active parallel consumers in a single consumer group?
- **Answer:** Exactly 8. A partition can only be assigned to a single consumer within a consumer group at any one time. If you deploy 12 consumer instances, 4 will sit idle as hot standbys.
