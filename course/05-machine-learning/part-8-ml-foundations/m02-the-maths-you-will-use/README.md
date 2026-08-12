# Module M02 — The Maths You Will Actually Use

**Level:** 05 Machine Learning, Part 8 (Foundations of Learning)  |  **Time:** L5 E6  |  **Prerequisite:** Module M01

> **Status: curriculum outline.** The full lesson, notebooks, exercises, and
> solutions are written in a later build pass. This file specifies exactly what
> the module must contain, so the build can resume without re-deriving anything.

---

## Why this module

This is not a maths course, and treating it as one loses most learners before
the first model. It is the specific, small set of ideas that you cannot skip
without later copying code you do not understand: what a matrix multiply is
doing to your data, what a gradient tells the optimiser, and why cross entropy
rather than something else. Every idea here is introduced because a later module
needs it, and each is implemented in NumPy so it stays concrete.

## What you will be able to do

- Read a model architecture as a sequence of shapes and say what each layer does to them.
- Compute a gradient by hand for a small composed function using the chain rule.
- Explain what a dot product measures and why attention is built from one.
- Derive cross entropy from maximum likelihood for a classification problem.
- Debug a shape error by reasoning rather than by permuting arguments.

## Concept sections

1. **Vectors, matrices, and shapes** — Data as a matrix. The matmul as the fundamental operation. Shape discipline as the single most useful debugging habit in deep learning.
2. **What a dot product means** — Similarity, projection, and why this one operation underlies embeddings, similarity search, and attention.
3. **Derivatives and the chain rule** — Slope, gradient, and composition. Deriving the gradient of a two-layer function by hand, once, carefully.
4. **Gradients of the operations you use** — Linear, sigmoid, ReLU, softmax, and the losses. A table you will refer back to for the rest of the level.
5. **Probability for modelling** — Distributions, expectation, conditional probability, and independence. Enough to read a paper's notation.
6. **Maximum likelihood** — Deriving squared error from a Gaussian assumption and cross entropy from a categorical one. Why the loss was never arbitrary.
7. **Optimisation geometry** — Convex versus non-convex, local minima, saddle points, and why high-dimensional loss surfaces are kinder than the two-dimensional pictures suggest.

## What you build

A small NumPy autodiff engine: scalar values with recorded operations and a
backward pass. Roughly two hundred lines, and it makes every later mention of
autograd concrete rather than magical.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_shapes.py` | Fix twelve shape errors by reasoning about dimensions. |
| `ex02_by_hand.md` | Differentiate five composed functions on paper, then verify numerically. |
| `ex03_micrograd.py` | Build the scalar autodiff engine and train a tiny network with it. |
| `ex04_likelihood.md` | Derive squared error and cross entropy from their distributional assumptions. |
| `ex05_softmax.py` | Implement a numerically stable softmax and show why the naive version fails. |

## Compute budget

CPU only. The autodiff engine is deliberately small enough to run and read.

## Common mistakes this module must address

- **Treating shape errors as syntax errors** — They are modelling errors. The shape is the meaning.
- **Implementing softmax without the max subtraction** — Overflow to nan on real logits.
- **Confusing the gradient with the update** — The gradient points uphill. The step is its negative, scaled.
- **Memorising derivative formulas** — Derive the two you use most once, and the rest become recognisable.

## Self check questions

1. What does the shape (batch, sequence, features) tell you about a tensor?
2. Why is cross entropy the natural loss for classification?
3. What does the chain rule let you do that direct differentiation does not?
4. Why subtract the maximum before exponentiating in softmax?
5. What is the gradient of ReLU at zero, and why does the choice not matter much?

## Going deeper

- Andrej Karpathy, The spelled-out intro to neural networks and backpropagation
- Deisenroth, Faisal, Ong, Mathematics for Machine Learning, chapters 2 to 5
