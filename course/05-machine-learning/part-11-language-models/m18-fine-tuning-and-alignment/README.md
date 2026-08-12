# Module M18 — Fine-tuning and Alignment

**Level:** 05 Machine Learning, Part 11 (Language Models and LLMs)  |  **Time:** L5 E9  |  **Prerequisite:** Module M17

> **Status: curriculum outline.** The full lesson, notebooks, exercises, and
> solutions are written in a later build pass. This file specifies exactly what
> the module must contain, so the build can resume without re-deriving anything.

---

## Why this module

Fine-tuning is the highest-leverage skill in applied language modelling and the
one most often done badly. This module treats it as an engineering discipline:
decide first whether you need it at all, build the dataset carefully because it
dominates the result, choose the method that fits your hardware, and evaluate
against a baseline you established beforehand. Alignment methods are included
because instruction following and preference tuning are what turn a base model
into something usable.

## What you will be able to do

- Decide between prompting, retrieval, and fine-tuning for a stated problem.
- Build and validate an instruction dataset, including the held-out split.
- Apply LoRA and QLoRA and explain the memory arithmetic that makes them work.
- Run supervised fine-tuning and a preference method such as DPO.
- Evaluate a fine-tune against a baseline and detect capability regression.

## Concept sections

1. **Do you need it** — Prompting, few-shot, retrieval, and fine-tuning as an ordered ladder of cost. The questions that decide which rung, and the honest answer that it is usually not the top one.
2. **The dataset is the model** — Instruction formats, quality over quantity, deduplication, contamination checks, and a held-out set built before any training.
3. **Full fine-tuning** — What it costs in memory: weights, gradients, optimiser states, activations, computed explicitly so the number stops being a surprise.
4. **LoRA** — Low-rank adapters, the rank and alpha choices, which modules to target, and why a fraction of a percent of trainable parameters can be enough.
5. **QLoRA** — 4-bit base weights with adapters on top. What is quantised, what is not, and the quality cost measured rather than assumed.
6. **Supervised fine-tuning in practice** — Masking the prompt tokens, packing, epochs, learning rates that are far smaller than pretraining, and the overfitting that appears within one epoch.
7. **Preference tuning** — RLHF in outline, then DPO in detail as the practical method. Preference data, the objective, and what alignment does and does not fix.
8. **Evaluating a fine-tune** — Task metrics, a capability regression suite, and human review. Catastrophic forgetting, detected rather than hoped against.

## What you build

A fine-tuned model for a task of your own: dataset built and documented, a
LoRA or QLoRA run, a merged and exported adapter, and an evaluation report
comparing it against the base model on both your task and a regression suite.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_ladder.md` | For eight problems, choose prompting, retrieval, or fine-tuning and justify it. |
| `ex02_dataset.py` | Build, clean, and split an instruction dataset with contamination checks. |
| `ex03_memory.md` | Compute the memory for full, LoRA, and QLoRA fine-tuning of three model sizes. |
| `ex04_lora.py` | Run a LoRA fine-tune and sweep rank against quality. |
| `ex05_qlora.py` | Repeat under a strict memory budget and measure the quality difference. |
| `ex06_dpo.py` | Apply preference tuning to a small preference set. |
| `ex07_evaluate.md` | Report task gains and any capability regression, with numbers. |

## Compute budget

QLoRA on a model of up to about seven billion parameters fits in 12 to 16GB of GPU memory, which is the intended path. A smaller model of around half a billion parameters makes the full exercise set feasible on CPU or a free hosted GPU.

## Common mistakes this module must address

- **Fine-tuning when a better prompt would do** — Weeks of work for something a paragraph achieved.
- **Not masking the prompt tokens in the loss** — The model learns to generate the instruction as well as the answer.
- **No held-out set from before training** — There is then no way to claim an improvement honestly.
- **Reusing pretraining learning rates** — Orders of magnitude too high. The model forgets.
- **Declaring success on the target task alone** — Check what the model lost, not only what it gained.

## Self check questions

1. When is retrieval the right answer instead of fine-tuning?
2. Why does LoRA reduce memory so much when the base model is unchanged?
3. What exactly does QLoRA quantise?
4. Why must prompt tokens be masked out of the loss?
5. How would you detect catastrophic forgetting?

## Going deeper

- Hu et al., LoRA: Low-Rank Adaptation of Large Language Models
- Rafailov et al., Direct Preference Optimization
