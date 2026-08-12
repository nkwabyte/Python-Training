# Module M05 — Tensors and Autograd

**Level:** 05 Machine Learning, Part 9 (Deep Learning with PyTorch)  |  **Time:** L4 E6  |  **Prerequisite:** Module M04

> **Status: curriculum outline.** The full lesson, notebooks, exercises, and
> solutions are written in a later build pass. This file specifies exactly what
> the module must contain, so the build can resume without re-deriving anything.

---

## Why this module

PyTorch is two ideas: a tensor library that runs on accelerators, and a system
that records what you did to tensors so it can differentiate it. Once those two
are clear, the rest of the framework is an ergonomics layer you can read from
the documentation. This module makes both concrete by rebuilding, in PyTorch,
the model you already wrote in NumPy, so nothing new is learned twice.

## What you will be able to do

- Create, reshape, index, and broadcast tensors without guessing.
- Explain what requires_grad, backward, and grad accumulation actually do.
- Move a model and its data between CPU and accelerator correctly.
- Use no_grad and detach in the right places and say why.
- Rewrite a NumPy training loop in PyTorch and get the same numbers.

## Concept sections

1. **Tensors** — Creation, dtype, device, shape, views versus copies. The NumPy correspondence and where it stops.
2. **Broadcasting** — The rules, stated precisely, with the four cases people get wrong.
3. **Autograd** — The dynamic graph, leaf tensors, backward, and .grad. Why gradients accumulate by default and what zero_grad is for.
4. **Devices** — CPU, CUDA, MPS. The two most common device errors and the habit that prevents both.
5. **no_grad and detach** — Inference mode, stopping gradient flow, and the memory difference. Where each belongs in a training script.
6. **The training loop, explicitly** — Forward, loss, backward, step, zero. Written once by hand with every line explained, because every later module abbreviates it.
7. **From NumPy to PyTorch** — Porting Module M03's logistic regression and reproducing its numbers exactly.

## What you build

The Module M03 models, reimplemented in PyTorch, plus a reusable training loop
with device handling, seeding, and metric logging that the rest of the level
imports.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_tensors.py` | Twenty tensor manipulations including views, copies, and stride surprises. |
| `ex02_broadcasting.py` | Predict the output shape of fifteen broadcast expressions. |
| `ex03_autograd.py` | Verify autograd against your hand-computed gradients from M02. |
| `ex04_port.py` | Port the NumPy logistic regression and match its loss curve. |
| `ex05_devices.py` | Fix six device and dtype errors. |

## Compute budget

CPU is sufficient. If you have a GPU or Apple silicon, this module is where you confirm it works.

## Common mistakes this module must address

- **Forgetting zero_grad** — Gradients accumulate across steps and training silently misbehaves.
- **Calling .item() inside the loop on a GPU tensor** — Forces a synchronisation every step and destroys throughput.
- **Keeping the loss tensor in a list** — Holds the whole graph in memory. Store .item() or .detach().
- **Mixing devices** — A cryptic error that is always the same mistake.

## Self check questions

1. What does requires_grad do to a tensor?
2. Why do gradients accumulate rather than replace?
3. What is the difference between detach and no_grad?
4. When is a reshape a view and when is it a copy?
5. Write the five lines of a minimal training step in order.

## Going deeper

- The PyTorch tutorials, tensors and autograd sections
- PyTorch internals, by Edward Yang
