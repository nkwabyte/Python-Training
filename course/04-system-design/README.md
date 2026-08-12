# Level 04 — System Design

**Start here if you write production Python and now need to reason about scale,
cost, and failure.**

This level has two parts and they are in this order on purpose. You cannot
estimate a system whose primitives you cannot cost, so Part 6 rebuilds the data
structures and algorithms from first principles, in Python, with every
complexity claim measured. Part 7 then designs systems out of them.

| | |
|---|---|
| Modules | D01 to D10, then 31 to 36 |
| Duration | 10 weeks |
| Weekly load | 10 to 15 hours |
| Prerequisite | Level 03, or production Python experience |
| Ends with | A designed, built, instrumented, and load-tested service |

---

## Part 6 — Data Structures and Algorithms

| Module | Title |
|---|---|
| [D01](part-6-data-structures-and-algorithms/d01-complexity-and-measurement/README.md) | Complexity and Measuring Cost |
| [D02](part-6-data-structures-and-algorithms/d02-arrays-and-dynamic-arrays/README.md) | Arrays and Dynamic Arrays |
| [D03](part-6-data-structures-and-algorithms/d03-hash-tables/README.md) | Hash Tables |
| [D04](part-6-data-structures-and-algorithms/d04-linked-structures/README.md) | Linked Lists, Stacks, and Queues |
| [D05](part-6-data-structures-and-algorithms/d05-trees-and-heaps/README.md) | Trees and Heaps |
| [D06](part-6-data-structures-and-algorithms/d06-graphs/README.md) | Graphs |
| [D07](part-6-data-structures-and-algorithms/d07-sorting-and-searching/README.md) | Sorting and Searching |
| [D08](part-6-data-structures-and-algorithms/d08-recursion-and-divide-and-conquer/README.md) | Recursion, Backtracking, and Divide and Conquer |
| [D09](part-6-data-structures-and-algorithms/d09-dynamic-programming-and-greedy/README.md) | Dynamic Programming and Greedy Algorithms |
| [D10](part-6-data-structures-and-algorithms/d10-patterns-and-design-bridge/README.md) | Patterns, Drills, and the Bridge to System Design |

## Part 7 — System Design with Python

| Module | Title |
|---|---|
| [31](part-7-system-design/31-design-fundamentals/README.md) | Design Fundamentals |
| [32](part-7-system-design/32-service-architecture/README.md) | Service Architecture and Concurrency Models |
| [33](part-7-system-design/33-caching-queues-jobs/README.md) | Caching, Queues, and Background Jobs |
| [34](part-7-system-design/34-data-at-scale/README.md) | Data at Scale |
| [35](part-7-system-design/35-reliability-observability-security/README.md) | Reliability, Observability, and Security |
| [36](part-7-system-design/36-capstone/README.md) | Capstone |

---

## How the two parts connect

Part 6 is not interview preparation that happens to sit next to system design.
Each structure reappears in Part 7 at a different scale:

| Part 6 idea | Part 7 consequence |
|---|---|
| Complexity and measurement (D01) | Capacity estimation and latency budgets (31) |
| Hash tables (D03) | Consistent hashing and sharding (34) |
| Linked structures and LRU (D04) | Cache eviction policy (33) |
| Trees and B-trees (D05) | Database index behaviour (34) |
| Graphs (D06) | Dependency ordering, tracing, service call graphs (32, 35) |
| Sorting and external merge (D07) | Batch pipelines and shuffles (34) |
| Probabilistic structures (D10) | Memory-bounded counting and dedup at scale (33, 34) |

If you already know your algorithms cold, you may run Part 6 as drills only and
move to Module 31 sooner. Do not skip D01 or D10 in that case; the first
supplies the vocabulary Part 7 uses for estimation and the second is the bridge.
