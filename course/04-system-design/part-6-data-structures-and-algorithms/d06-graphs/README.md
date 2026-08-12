# Module D06 — Graphs

**Track:** System Design, Part 6 (Data Structures and Algorithms)  |  **Time:** L5 E7  |  **Prerequisite:** Module D05

> **Status: curriculum outline.** The full lesson, exercises, and solutions are
> written in a later build pass. This file specifies exactly what the module
> must contain, so the build can resume without re-deriving anything.

---

## Why this module

Graphs are the most general model in this track, and once a learner can see
them, they appear everywhere: dependencies, routing, social connections,
scheduling, deadlocks, and service call chains. This module is deliberately
practical about representation, because choosing an adjacency list versus a
matrix is exactly the kind of decision that has consequences at scale.

## What you will be able to do

- Represent a graph three ways and choose the right one for a density and access pattern.
- Implement breadth first and depth first search iteratively.
- Produce a topological order and detect a cycle in a dependency graph.
- Apply Dijkstra with a heap, and say when it does not apply.
- Recognise a graph problem when it is disguised as something else.

## Concept sections

1. **Modelling with graphs** — Vertices, edges, directed, weighted, cyclic. Turning three real problems into graphs in front of the learner.
2. **Representations** — Adjacency list, adjacency matrix, and edge list. Memory and access cost for each, tied to Module D01.
3. **Breadth first search** — Level order over a graph. Shortest path on unweighted edges. Why a queue and a visited set are both required.
4. **Depth first search** — Recursive and explicit stack forms. Connected components, cycle detection, and path finding.
5. **Topological sort** — Kahn's algorithm and the DFS variant. Build order, task scheduling, and detecting the cycle that makes it impossible.
6. **Weighted shortest paths** — Dijkstra with heapq. Where negative edges break it and what Bellman-Ford is for. A word on A star.
7. **Graphs in system design** — Dependency graphs in deployment, service call graphs in tracing, and consistent hashing rings as a structure. The bridge to Modules 32 and 35.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_representations.py` | Build all three representations and compare memory and lookup cost. |
| `ex02_bfs.py` | Shortest hop count and level grouping on an unweighted graph. |
| `ex03_dfs.py` | Components, cycle detection, and path reconstruction. |
| `ex04_toposort.py` | Order a real build dependency file and report a cycle clearly. |
| `ex05_dijkstra.py` | Weighted shortest path with a heap, on a road-like network. |
| `ex06_disguised.md` | Recognise six problems as graph problems and state the model. |

## The Python angle

Use dicts of lists as the default representation, deque for BFS, and heapq for
Dijkstra, so that every earlier module pays off here. Mention networkx as the
right production answer and explain why the course still builds it by hand once.

## Common mistakes this module must address

- **Forgetting the visited set** — Infinite loop on any cyclic graph.
- **Marking visited at pop instead of push in BFS** — Duplicate work and, sometimes, wrong results.
- **Recursive DFS on a large graph** — Stack overflow. Show the iterative version.
- **Using Dijkstra with negative weights** — It returns confidently wrong answers, which is worse than failing.

## Self check questions

1. When is an adjacency matrix the better representation?
2. Why does BFS find the shortest path only on unweighted graphs?
3. How do you detect a cycle in a directed graph?
4. What does a topological sort tell you about a build?
5. Why does Dijkstra fail on negative edges?

## Going deeper

- CLRS, chapters 22 to 24
- The networkx documentation, tutorial section
