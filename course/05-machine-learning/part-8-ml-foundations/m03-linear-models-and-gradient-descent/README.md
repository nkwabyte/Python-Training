# Module M03 — Linear Models and Gradient Descent from Scratch

**Level:** 05 Machine Learning, Part 8 (Foundations of Learning)  |  **Time:** L4 E6  |  **Prerequisite:** Module M02

> **Status: curriculum outline.** The full lesson, notebooks, exercises, and
> solutions are written in a later build pass. This file specifies exactly what
> the module must contain, so the build can resume without re-deriving anything.

---

## Why this module

Every deep network is a stack of the thing you build in this module. Writing
linear and logistic regression from scratch, with your own gradient descent
loop, gives you a model whose every part you can inspect, so that when a
transformer refuses to converge later you already know what a learning rate that
is too high looks like. Regularisation is taught here too, because the trade it
makes is easier to see in two parameters than in two hundred million.

## What you will be able to do

- Implement linear and logistic regression and their gradients in NumPy.
- Write a gradient descent loop and diagnose it from the loss curve alone.
- Explain the difference between batch, stochastic, and mini-batch descent.
- Choose a learning rate deliberately and recognise the three failure shapes.
- Say what L1 and L2 regularisation do to the parameters and why.

## Concept sections

1. **Linear regression** — The model, the loss, the closed form, and why iterative methods are used anyway once the data is large.
2. **Gradient descent** — The update rule, the learning rate, and convergence. The three loss curves: too high, too low, and about right.
3. **Batch, stochastic, and mini-batch** — Noise as a feature. Why mini-batches dominate in practice and how batch size interacts with learning rate.
4. **Logistic regression** — From a linear score to a probability. The sigmoid, the decision boundary, and cross entropy in code.
5. **Feature scaling** — Why unscaled features make descent crawl, shown as an elongated loss surface.
6. **Regularisation** — L2 shrinking, L1 selecting, and the geometric reason for the difference. Weight decay as the same idea in a different vocabulary.
7. **Beyond one linear layer** — Polynomial features, the limits of a linear boundary, and the precise reason the next module needs a non-linearity.

## What you build

A small library of your own: fit and predict for linear and logistic regression,
mini-batch descent, L1 and L2 penalties, and a training report. Its results are
checked against scikit-learn to the third decimal.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_linreg.py` | Implement linear regression with gradients and verify numerically. |
| `ex02_learning_rate.py` | Produce all three loss-curve failure shapes on purpose. |
| `ex03_logreg.py` | Logistic regression from scratch, checked against scikit-learn. |
| `ex04_regularise.py` | Show L1 zeroing coefficients where L2 only shrinks them. |
| `ex05_scaling.py` | Measure how many more steps unscaled features cost. |

## Compute budget

CPU only. Datasets stay small enough that a full run takes seconds.

## Common mistakes this module must address

- **Forgetting to average the gradient over the batch** — The effective learning rate then scales with batch size and nothing is comparable.
- **Not scaling features** — Slow convergence blamed on the algorithm rather than the data.
- **Regularising the bias term** — Shrinking the intercept toward zero is rarely what you meant.
- **Judging convergence by the training loss alone** — It will keep falling long after the model has stopped generalising.

## Self check questions

1. What does the learning rate control, and what does too high look like?
2. Why does mini-batch descent often generalise better than full batch?
3. What is the geometric reason L1 produces sparse solutions?
4. Why does logistic regression use cross entropy rather than squared error?
5. What does feature scaling do to the loss surface?

## Going deeper

- Murphy, Probabilistic Machine Learning: An Introduction, chapters 11 and 10
- Sebastian Ruder, An overview of gradient descent optimisation algorithms
