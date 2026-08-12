# Module M15 — Build a Mini LLM from Scratch

**Level:** 05 Machine Learning, Part 11 (Language Models and LLMs)  |  **Time:** P16  |  **Prerequisite:** Modules M10 and M14

> **Status: curriculum outline.** The full lesson, notebooks, exercises, and
> solutions are written in a later build pass. This file specifies exactly what
> the module must contain, so the build can resume without re-deriving anything.

---

## Why this module

This is the centre of the level. Everything built so far assembles into a small
GPT that you pretrain yourself, on data you prepared, with a training loop you
wrote, producing text you can read. The model will be modest, and that is the
point: a ten million parameter model you understand completely teaches more than
a frontier model you can only prompt, and every scaling question afterwards
becomes a quantitative question rather than a mystery.

## What you will be able to do

- Assemble a GPT-style decoder from your Module M10 components.
- Prepare a pretraining corpus: cleaning, deduplication, tokenising, packing.
- Run a stable pretraining job with checkpointing, resumption, and logging.
- Reason about the parameter, data, and compute trade using scaling laws.
- Generate text, evaluate it honestly, and explain what the model cannot do.

## Concept sections

1. **The architecture** — A decoder-only transformer specified in full: dimensions, heads, layers, context, vocabulary, and the parameter count derived from them.
2. **The data pipeline** — Sourcing, cleaning, deduplicating, tokenising, and packing into fixed-length sequences. Why deduplication matters more than people expect.
3. **The training run** — Batch size and accumulation, AdamW settings, warmup and cosine decay, weight tying, gradient clipping, and mixed precision.
4. **Watching a pretraining run** — Loss curves, gradient norms, learning rate, throughput in tokens per second, and the samples you generate at every checkpoint.
5. **Scaling laws** — Parameters, tokens, and compute, and the compute-optimal ratio. Using it to choose the size that fits the budget you actually have.
6. **Generation** — Wiring up the sampling from Module M14, adding a KV cache, and measuring the speedup.
7. **Honest evaluation** — Held-out loss, a small benchmark, and reading outputs. What a model this size can and cannot do, stated plainly.

## What you build

A GPT of roughly ten to thirty million parameters, pretrained by you on a corpus
of a few hundred million tokens, with checkpoints, a training report, generated
samples, and a written analysis of where the compute went.

## Exercises to build

| File | What it drills |
|---|---|
| `stage1_data.py` | Build the data pipeline: clean, dedupe, tokenise, pack. |
| `stage2_model.py` | Assemble the model from your M10 components and check the parameter count. |
| `stage3_train.py` | Pretrain with checkpointing, resumption, and logging. |
| `stage4_generate.py` | Add a KV cache and measure the generation speedup. |
| `stage5_scale.md` | Apply scaling laws to justify your size and token budget. |
| `stage6_report.md` | Write the training report: curves, samples, cost, and limitations. |

## Compute budget

This is the heaviest module in the course. A single consumer GPU trains the reference configuration in a few hours. The module also ships a tiny character-level configuration that trains on CPU in about twenty minutes, so the whole pipeline can be completed without a GPU, and a hosted-notebook path for the full run.

## Common mistakes this module must address

- **Not deduplicating the corpus** — The model memorises repeats and the held-out loss lies to you.
- **Skipping warmup** — Early instability that poisons the whole run.
- **Checkpointing too rarely** — A crash at hour four costs hour four.
- **Judging the model by one lucky sample** — Generate many, at fixed settings, and keep them all.
- **Choosing size before budget** — Scaling laws let you pick both together. Use them.

## Self check questions

1. How do you compute the parameter count of your model from its dimensions?
2. Why does deduplication change held-out loss?
3. What does the KV cache store and what does it save?
4. What ratio of tokens to parameters does compute-optimal training suggest?
5. What can your model demonstrably not do, and why?

## Going deeper

- Karpathy, nanoGPT and Let's build GPT from scratch
- Hoffmann et al., Training Compute-Optimal Large Language Models
