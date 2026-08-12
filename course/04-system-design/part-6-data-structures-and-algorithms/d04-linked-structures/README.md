# Module D04 — Linked Lists, Stacks, and Queues

**Track:** System Design, Part 6 (Data Structures and Algorithms)  |  **Time:** L3 E5  |  **Prerequisite:** Module D03

> **Status: curriculum outline.** The full lesson, exercises, and solutions are
> written in a later build pass. This file specifies exactly what the module
> must contain, so the build can resume without re-deriving anything.

---

## Why this module

Linked lists are rarely the right answer in Python, and that is precisely why
they are worth building once: they make pointers, invariants, and node surgery
concrete, and they are the substrate for the LRU cache that appears in the
system design track. Stacks and queues are the opposite case, structures you
will use constantly, usually without naming them.

## What you will be able to do

- Implement singly and doubly linked lists with correct edge case handling.
- Explain what a linked list buys and what it costs relative to an array.
- Use a list as a stack and a deque as a queue, correctly.
- Implement an LRU cache from a hash map plus a doubly linked list.
- Recognise stack-shaped and queue-shaped problems on sight.

## Concept sections

1. **Nodes and references** — A node holds a value and a link. Building, traversing, and the sentinel trick that removes half the edge cases.
2. **Singly linked operations** — Insert, delete, reverse, find the middle, detect a cycle with the fast and slow pointer.
3. **Doubly linked lists** — Two way links, constant time removal given a node, and the bookkeeping that makes it correct.
4. **Array versus linked, honestly** — Why the textbook advantage rarely materialises in Python, with a benchmark.
5. **Stacks** — Last in first out. Using a list. Undo, balanced brackets, expression evaluation, and depth first traversal without recursion.
6. **Queues** — First in first out. deque, and why a list is the wrong choice. Breadth first traversal and simple work buffers.
7. **LRU cache** — The classic composition of a hash map and a doubly linked list, then a comparison with functools.lru_cache.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_singly.py` | Build a singly linked list with insert, delete, and reverse. |
| `ex02_cycle.py` | Detect and locate a cycle with two pointers. |
| `ex03_doubly.py` | Doubly linked list with constant time removal. |
| `ex04_stack_problems.py` | Balanced brackets, postfix evaluation, and an undo buffer. |
| `ex05_lru.py` | Implement an LRU cache and verify eviction order under load. |

## The Python angle

Connect to advanced Module 15, where functools.lru_cache appeared as a
decorator, and to the caching module in the system design part, where eviction
policy becomes an architectural decision rather than a data structure one.

## Common mistakes this module must address

- **Losing the head reference** — One reassignment in the wrong order and the list is gone. Sentinels and diagrams prevent this.
- **Forgetting the empty and single element cases** — Where nearly every linked list bug lives.
- **Using a list as a queue** — pop(0) again. It comes back in every module for a reason.
- **Building a linked list in production Python** — Almost always slower than a list or deque. Build it to learn, then use the built-in.

## Self check questions

1. What does a linked list make cheap that an array makes expensive?
2. How does the fast and slow pointer detect a cycle?
3. Why is deque the right queue and list the wrong one?
4. Which two structures combine to make an LRU cache, and why each?
5. When is a stack the natural fit for a problem?

## Going deeper

- The collections.deque documentation and its implementation notes
- CLRS, chapter 10
