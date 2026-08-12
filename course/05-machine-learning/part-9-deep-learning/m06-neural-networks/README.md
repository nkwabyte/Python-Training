# Module M06 — Neural Networks, Derived and Built

**Level:** 05 Machine Learning, Part 9 (Deep Learning with PyTorch)  |  **Time:** L5 E7  |  **Prerequisite:** Module M05

> **Status: curriculum outline.** The full lesson, notebooks, exercises, and
> solutions are written in a later build pass. This file specifies exactly what
> the module must contain, so the build can resume without re-deriving anything.

---

## Why this module

Backpropagation is derived by hand exactly once in this course, here, on a
two-layer network. It is worth the afternoon: everything afterwards, including
why gradients vanish and why residual connections help, is a corollary of that
derivation. The module then builds the same network with nn.Module so the
learner sees the framework as a labour saver rather than as the source of the
result.

## What you will be able to do

- Derive the backward pass of a two-layer network and implement it in NumPy.
- Explain why a non-linearity is required and what each common one does.
- Build the same network with nn.Module and match the from-scratch results.
- Choose an initialisation and say what problem it solves.
- Read a model definition and state its parameter count from the shapes.

## Concept sections

1. **Why a non-linearity** — Stacked linear layers collapse to one. The proof in three lines, and what that means for capacity.
2. **Activations** — Sigmoid, tanh, ReLU, GELU, SiLU. Saturation, dead units, and why the field moved.
3. **Forward and backward by hand** — A two-layer network derived fully, then implemented in NumPy and checked against a numerical gradient.
4. **nn.Module** — Parameters, submodules, forward, and state_dict. The same network in a quarter of the code.
5. **Initialisation** — Why zeros fail, why the scale matters, and what Xavier and He initialisation are protecting.
6. **Optimisers** — SGD, momentum, RMSProp, Adam, AdamW. What each adds and the defaults worth knowing.
7. **Reading an architecture** — Turning a model definition into shapes, parameter counts, and a memory estimate.

## What you build

The same multilayer network three times: NumPy with hand-written gradients, then
PyTorch with autograd but manual updates, then full nn.Module with an optimiser.
Identical loss curves across all three is the acceptance test.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_no_nonlinearity.py` | Demonstrate that stacked linear layers learn nothing extra. |
| `ex02_backprop.py` | Implement the backward pass and pass a numerical gradient check. |
| `ex03_nnmodule.py` | Rebuild with nn.Module and reproduce the curve. |
| `ex04_init.py` | Show training failure from bad initialisation and fix it. |
| `ex05_optimisers.py` | Compare five optimisers on the same problem and explain the ordering. |
| `ex06_param_count.md` | Compute parameter counts for six architectures by hand. |

## Compute budget

CPU is enough for every exercise. Runs are minutes, not hours.

## Common mistakes this module must address

- **Initialising all weights to zero** — Every unit computes the same thing forever. Symmetry is never broken.
- **Applying softmax then cross entropy loss** — Most frameworks expect logits. Doing both silently degrades training.
- **Using a learning rate tuned for SGD with Adam** — Different scales entirely.
- **Trusting a model that trains but never overfits a tiny batch** — If it cannot memorise ten examples, it has a bug, not a capacity problem.

## Self check questions

1. Why is a non-linearity necessary?
2. What problem does He initialisation solve?
3. What does momentum add to plain gradient descent?
4. Why does the loss function usually take logits rather than probabilities?
5. How do you sanity check a new model in under a minute?

## Going deeper

- Nielsen, Neural Networks and Deep Learning, chapters 1 and 2
- Karpathy, A Recipe for Training Neural Networks
