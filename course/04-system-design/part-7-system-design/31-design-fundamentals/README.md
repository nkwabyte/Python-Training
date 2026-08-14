# Module 31 — Design Fundamentals

**Level:** 04 System Design, Part 7  |  **Time:** L4 E5  |  **Prerequisite:** Module D10, and Level 03

> The teaching for this module is in the notebooks under [`exercises/`](exercises/).
> This README is the map: why the module exists, what you should be able to do,
> the mistakes it exists to prevent, and the quiz. Read it first and last.

---

## Why this module

Every system design conversation you will ever have is decided in its first ten
minutes, and not by the box diagram. It is decided by whether you established
what the system must do, how much of it, how fast, and what happens when part of
it is broken. Engineers who skip that arrive at an architecture that answers no
stated question, and cannot defend it when challenged, because there is nothing
to defend it against.

This module gives you the four tools that make the rest of the level possible:
requirements you can hold someone to, numbers you can produce in ninety seconds
on a whiteboard, a law that ties throughput to latency, and honest availability
arithmetic. None of them are difficult. All of them are routinely skipped.

The order matters. Estimation without requirements is arithmetic about nothing.
Architecture without estimation is decoration.

---

## What you will be able to do

- Turn a one-sentence brief into functional and non-functional requirements, and
  name the three questions whose answers would change the design most.
- Produce a capacity estimate in under two minutes: queries per second, storage
  per year, bandwidth, and the size of the working set.
- Recite the latency numbers that matter, and say which two orders of magnitude
  separate the ones you will actually trade between.
- Apply Little's Law to size a pool, a queue, or a thread count, and explain why
  adding concurrency past a point raises latency without raising throughput.
- Compute the availability of a dependency chain and say where the nines went.
- State what CAP actually says, and what it does not, without repeating the
  slogan version.
- Run a design conversation through a framework rather than improvising.

---

## The notebooks

Work through them in order. Each teaches before it asks.

| Notebook | What it covers |
|---|---|
| [`ex01_requirements.ipynb`](exercises/ex01_requirements.ipynb) | Functional against non-functional. The questions to ask a stakeholder. Turning a vague brief into a spec you could be held to. Scope that can be defended. |
| [`ex02_estimation.ipynb`](exercises/ex02_estimation.ipynb) | Back of envelope: users to QPS, QPS to storage, storage to cost. Latency numbers, measured on your own machine rather than memorised. Rounding rules that keep you fast and honest. |
| [`ex03_littles_law.ipynb`](exercises/ex03_littles_law.ipynb) | Throughput, latency, and concurrency as three views of one thing. Simulating a queue and watching the law hold. Why the fourth worker helps and the fortieth does not. |
| [`ex04_availability.ipynb`](exercises/ex04_availability.ipynb) | Nines as minutes. Serial and parallel composition. Why a chain of five reliable services is not reliable, and what to do about it. |
| [`ex05_cap_and_consistency.ipynb`](exercises/ex05_cap_and_consistency.ipynb) | CAP stated precisely, then PACELC. Consistency models with a replication-lag simulation you can break read-your-writes in. |
| [`ex06_the_framework.ipynb`](exercises/ex06_the_framework.ipynb) | The whole conversation, step by step, applied end to end to one brief. Produces a design document you keep. |

---

## Common mistakes this module exists to prevent

| Mistake | What it looks like | The fix |
|---|---|---|
| Designing before scoping | A diagram appears in minute three | Nothing is drawn until the requirements are written down |
| Estimating with false precision | "About 47,000 QPS" | One significant figure. The exponent is the answer; the mantissa is noise |
| Quoting latency numbers you have never measured | "Disk is 10ms" on an NVMe machine | Measure your own. The ratios matter more than the values |
| Adding workers to fix latency | A pool of 200 threads and worse p99 | Little's Law. Past saturation, concurrency becomes queueing |
| Multiplying nines wrongly | "All my services are 99.9, so the system is 99.9" | Serial dependencies multiply. Five of them give you 99.5 |
| Repeating CAP as a slogan | "We chose AP" | CAP is about behaviour during a partition only. PACELC covers the other 99.9 percent of the time |
| Treating an estimate as a commitment | The number becomes a target | An estimate exists to eliminate options, not to predict the future |

---

## Self-check quiz

Answer each in one or two sentences without looking.

1. What separates a functional from a non-functional requirement, and which one usually decides the architecture?
2. A service has 10 million daily active users, each making 20 requests a day. What is the average QPS, and what peak would you plan for?
3. Roughly how much slower is a memory read than an L1 cache reference? A disk seek than a memory read?
4. State Little's Law, and use it to size a connection pool for 500 requests per second at 40ms each.
5. Why does p99 latency rise sharply as utilisation approaches 100 percent?
6. Five services each at 99.9 percent availability, called in sequence. What is the availability of the chain, in minutes of downtime per month?
7. What exactly does CAP force you to choose between, and when does that choice apply?
8. What does PACELC add that CAP leaves out?
9. Read-your-writes fails on a replicated database. Name two fixes and the cost of each.
10. What are the first three things you do when given a design brief, in order?

---

## Going deeper

- Jeff Dean, Numbers Everyone Should Know, and the latency tables derived from it
- Martin Kleppmann, Designing Data-Intensive Applications, chapters 1 and 9
- Daniel Abadi, Consistency Tradeoffs in Modern Distributed Database System Design, the PACELC paper
- Google SRE Book, chapters on service level objectives and on handling overload
- Brendan Gregg, Systems Performance, on utilisation, saturation, and queueing
