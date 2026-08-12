# Module M08 — Training That Actually Works

**Level:** 05 Machine Learning, Part 9 (Deep Learning with PyTorch)  |  **Time:** L5 E7  |  **Prerequisite:** Module M07

> **Status: curriculum outline.** The full lesson, notebooks, exercises, and
> solutions are written in a later build pass. This file specifies exactly what
> the module must contain, so the build can resume without re-deriving anything.

---

## Why this module

A model that will not train is the most common experience in deep learning and
the least documented. This module is the diagnostic manual: the ordered
checklist for a loss that will not fall, the regularisation toolkit for a model
that fits the training set and nothing else, and the engineering that makes runs
fast enough to iterate on. It is the module people wish they had read first.

## What you will be able to do

- Diagnose a stuck training run with an ordered procedure rather than by guessing.
- Apply dropout, weight decay, augmentation, and early stopping deliberately.
- Explain what batch norm and layer norm do and where each belongs.
- Use a learning rate schedule, including warmup, and justify the shape.
- Make a run faster with mixed precision and a correct data pipeline.

## Concept sections

1. **The overfitting toolkit** — More data, augmentation, weight decay, dropout, early stopping, and smaller models. What each costs and the order to try them.
2. **Normalisation** — Batch norm, layer norm, RMS norm. What is normalised over what, the train and eval difference, and why transformers use layer norm.
3. **Learning rate schedules** — Step, cosine, one-cycle, and warmup. Why the largest single hyperparameter effect is here.
4. **The stuck-run checklist** — Overfit ten samples first. Then check the data, the labels, the loss, the learning rate, the initialisation, the gradients, and the shapes, in that order.
5. **Gradient pathologies** — Vanishing and exploding gradients, gradient clipping, residual connections, and how to see the problem in a gradient norm plot.
6. **The input pipeline** — Dataset and DataLoader, workers, pinned memory, and the moment the GPU is starved by the CPU.
7. **Speed** — Mixed precision, batch size, accumulation, and compilation. Measure before and after, per the rule from Advanced Module 23.

## What you build

A training script with the full apparatus: config, seeding, schedules, early
stopping, checkpointing, gradient logging, mixed precision, and resume. This is
the script every remaining module in the level starts from.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_overfit_ten.py` | Prove a model can memorise ten samples, then find the bug when it cannot. |
| `ex02_regularise.py` | Apply four regularisers to an overfitting model and compare. |
| `ex03_norm.py` | Show batch norm failing at batch size one and layer norm not. |
| `ex04_schedules.py` | Compare three schedules and warmup on the same run. |
| `ex05_debug_five.md` | Five broken runs, one root cause each, diagnosed with the checklist. |
| `ex06_speed.py` | Halve the epoch time and prove it with measurements. |

## Compute budget

A GPU helps but is not required. Exercises are sized so the CPU path finishes in under ten minutes; a free hosted notebook is an acceptable substitute.

## Common mistakes this module must address

- **Changing five things at once** — Nothing is attributable. One change per run.
- **Leaving the model in train mode at evaluation** — Dropout and batch norm behave differently and the metric is wrong.
- **Shuffling a validation set with a temporal meaning** — Quietly reintroduces leakage.
- **Blaming the model before checking the labels** — Data problems outnumber architecture problems by a wide margin.

## Self check questions

1. What is the first thing to try when the loss will not move?
2. Why does batch norm behave differently at evaluation time?
3. What does warmup protect against?
4. What symptom does gradient clipping treat?
5. How would you tell that the GPU is being starved by the data pipeline?

## Going deeper

- Karpathy, A Recipe for Training Neural Networks
- The PyTorch performance tuning guide
