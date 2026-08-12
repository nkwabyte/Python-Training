# Module M18 — Serving, Evaluation, and Cost

**Level:** 05 Machine Learning, Part 11 (Language Models and LLMs)  |  **Time:** L4 E7  |  **Prerequisite:** Module M17

> **Status: curriculum outline.** The full lesson, notebooks, exercises, and
> solutions are written in a later build pass. This file specifies exactly what
> the module must contain, so the build can resume without re-deriving anything.

---

## Why this module

A model that is not served is a notebook. This module closes the loop with the
system design level: an inference service has a latency budget, a throughput
ceiling, a memory constraint, and a bill, and those are architecture problems
before they are model problems. It also covers evaluation and monitoring, since
a language feature that nobody measures degrades silently and nobody finds out
from the logs.

## What you will be able to do

- Serve a model behind an API with batching and streaming.
- Explain the KV cache, continuous batching, and where the latency actually goes.
- Build an evaluation suite that can gate a deployment.
- Design a retrieval-augmented pipeline and say what it fixes and what it does not.
- Estimate and control the cost of a feature per thousand requests.

## Concept sections

1. **The inference workload** — Prefill and decode as two different problems: one compute-bound, one memory-bandwidth-bound. Why that split explains most latency behaviour.
2. **Serving efficiently** — KV cache memory, continuous batching, paged attention, speculative decoding. What each buys, in the vocabulary of Module 32.
3. **Building the service** — A FastAPI front end from Advanced Module 28, streaming responses, timeouts, backpressure, and graceful degradation.
4. **Retrieval augmentation** — Chunking, embeddings, vector search, reranking, and context assembly. Which failures it fixes and which it cannot touch.
5. **Evaluation that gates a release** — Golden sets, rubric grading, model-as-judge and its biases, regression suites, and offline versus online evaluation.
6. **Monitoring in production** — Latency percentiles, token throughput, refusal and error rates, drift, and user feedback loops. Tied to the observability practice of Module 35.
7. **Cost** — Tokens as the unit. Cost per request, caching, routing between model sizes, and the build-versus-buy calculation done with real numbers.

## What you build

A production-shaped service for your fine-tuned model: streaming API, batching,
a retrieval path, an evaluation suite wired into CI, a load test, and a cost
model per thousand requests.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_serve.py` | Serve the model with streaming and measure latency percentiles. |
| `ex02_kv_cache.py` | Measure prefill and decode separately and explain the difference. |
| `ex03_batching.py` | Compare static and continuous batching under load. |
| `ex04_rag.py` | Build a retrieval pipeline and measure what it fixes. |
| `ex05_evals.py` | Build an evaluation suite that fails the build on regression. |
| `ex06_cost.md` | Model the cost per thousand requests and find the two biggest levers. |

## Compute budget

A GPU makes the load tests realistic. A small model on CPU is sufficient to build and test every component; the numbers will differ but the shapes will not.

## Common mistakes this module must address

- **Measuring only average latency** — Users experience the tail. Report p50, p95, and p99.
- **Ignoring KV cache memory in capacity planning** — It grows with batch size and context, and it is what actually limits concurrency.
- **Using a model as judge without checking it** — It has biases, including toward its own style and toward longer answers.
- **Shipping without an evaluation gate** — Every later change is then a guess about whether quality moved.

## Self check questions

1. Why are prefill and decode bound by different resources?
2. What determines how many concurrent requests a GPU can hold?
3. What class of failure does retrieval augmentation not fix?
4. Why is p99 latency the number that matters?
5. What are the two largest levers on cost per request?

## Going deeper

- Kwon et al., Efficient Memory Management for LLM Serving with PagedAttention
- Chip Huyen, Designing Machine Learning Systems, chapters 7 to 9
