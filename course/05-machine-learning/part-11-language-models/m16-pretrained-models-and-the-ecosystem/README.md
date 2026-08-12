# Module M16 — Pretrained Models and the Open Ecosystem

**Level:** 05 Machine Learning, Part 11 (Language Models and LLMs)  |  **Time:** L4 E6  |  **Prerequisite:** Module M15

> **Status: curriculum outline.** The full lesson, notebooks, exercises, and
> solutions are written in a later build pass. This file specifies exactly what
> the module must contain, so the build can resume without re-deriving anything.

---

## Why this module

Having built one from scratch, you can now use other people's without mystique.
This module is about the working practice around open models: finding one that
fits, loading it without exhausting memory, running it efficiently, and reading
a model card critically enough to know what you are deploying. It is deliberately
placed after the from-scratch build so that every abstraction maps onto something
you have already implemented.

## What you will be able to do

- Choose a model by size, licence, context length, and benchmark evidence.
- Load and run a model within a known memory budget, including quantised.
- Map the library's abstractions onto the components you built yourself.
- Batch and stream inference efficiently.
- Read a model card and state the risks of using it in a product.

## Concept sections

1. **The landscape** — Base versus instruction-tuned versus reasoning models. Parameter counts, context windows, licences, and what open weights does and does not mean.
2. **Loading a model** — Weights, dtypes, device maps, and the memory arithmetic that tells you in advance whether it will fit.
3. **The library, demystified** — Tokenizer, config, model, and generation utilities, each matched to the thing you wrote in Modules M10, M14, and M15.
4. **Running inference well** — Batching, padding side, streaming, stopping criteria, and the settings that silently change output quality.
5. **Quantisation, first pass** — 8-bit and 4-bit weights, what is lost, and the memory-versus-quality curve measured on your own task.
6. **Datasets and the hub** — Loading, streaming, and preparing datasets. Versioning and licensing hygiene.
7. **Reading a model card critically** — Training data, evaluations, known failure modes, and the questions the card does not answer.

## What you build

A small local inference service that loads an open model, batches requests,
streams tokens, and reports latency and memory, with a quality-versus-memory
table for full, 8-bit, and 4-bit precision on your own task.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_choose.md` | Select a model for five stated constraints and defend each choice. |
| `ex02_memory.py` | Predict memory use before loading, then measure the error. |
| `ex03_map.md` | Map each library abstraction onto your own implementation. |
| `ex04_batching.py` | Measure throughput against batch size and find the knee. |
| `ex05_quantise.py` | Compare full, 8-bit, and 4-bit on quality, memory, and speed. |

## Compute budget

A GPU with 8GB or more is comfortable. Everything is doable on CPU with a model of about one billion parameters, more slowly; the quantisation exercise is where CPU is actually convenient.

## Common mistakes this module must address

- **Left padding versus right padding** — Wrong for generation, and the outputs degrade without an error.
- **Ignoring the chat template** — An instruction-tuned model given raw text underperforms badly.
- **Assuming the licence permits your use** — Open weights is not one licence, and several forbid commercial use.
- **Trusting benchmark numbers on a card** — Contamination is common. Evaluate on your own task.

## Self check questions

1. How do you estimate the memory needed to load a model of a given size?
2. What is the difference between a base and an instruction-tuned model?
3. Why does padding side matter for generation?
4. What does 4-bit quantisation cost you, measurably?
5. Which questions should a model card answer that most do not?

## Going deeper

- The Hugging Face Transformers documentation, quicktour and generation guides
- Mitchell et al., Model Cards for Model Reporting
