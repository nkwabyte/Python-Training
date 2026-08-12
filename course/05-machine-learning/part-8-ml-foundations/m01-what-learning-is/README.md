# Module M01 — What Learning Is

**Level:** 05 Machine Learning, Part 8 (Foundations of Learning)  |  **Time:** L4 E5  |  **Prerequisite:** Advanced Module 29 (Data and ML Foundations)

> **Status: curriculum outline.** The full lesson, notebooks, exercises, and
> solutions are written in a later build pass. This file specifies exactly what
> the module must contain, so the build can resume without re-deriving anything.

---

## Why this module

Most people arrive at machine learning through libraries, which means they can
fit a model months before they can say what fitting one means. This module
installs the frame that every later module hangs on: a hypothesis space, a loss
that says what wrong means, an optimiser that searches, and a held-out set that
tells you whether any of it generalised. It also front-loads the failure that
ruins more projects than any modelling mistake, which is leakage between the
data you trained on and the data you judged yourself with.

## What you will be able to do

- State any supervised problem as a hypothesis space, a loss, and an optimisation procedure.
- Explain generalisation, and why training error is not evidence of it.
- Split data correctly, including for time series and grouped records.
- Name the leakage in a described pipeline before it is trained.
- Decide whether a problem needs machine learning at all.

## Concept sections

1. **The learning frame** — Inputs, targets, a function family, a loss, and a search. Supervised, unsupervised, and reinforcement learning placed on one map.
2. **What a loss encodes** — Squared error, absolute error, cross entropy. Each loss is a statement about what kind of mistake you mind, made mathematical.
3. **Generalisation** — Training, validation, and test as three different questions. Why the test set is spent the moment you look at it twice.
4. **Underfitting and overfitting** — Capacity, the bias and variance decomposition, and learning curves as the diagnostic that tells you which one you have.
5. **Splitting data honestly** — Random, stratified, grouped, and temporal splits. Which one your problem requires and what breaks if you choose wrong.
6. **Leakage** — Target leakage, train-test contamination, and preprocessing fitted on the whole dataset. Five real examples, each of which looked like a great result first.
7. **When not to use machine learning** — A rule, a lookup table, or a better sensor. The cost of a model that must be maintained forever.

## What you build

A single notebook that takes one tabular dataset and produces an honest baseline:
correct split, a trivial predictor, a linear model, learning curves, and a
written statement of what performance would have to beat to be worth deploying.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_frame_it.md` | Express six real problems as hypothesis space, loss, and optimiser. |
| `ex02_splits.py` | Build random, stratified, grouped, and temporal splits and compare their estimates. |
| `ex03_find_the_leak.md` | Eight pipelines, each with one leak. Name it and predict the effect. |
| `ex04_learning_curves.py` | Diagnose underfitting versus overfitting from curves alone. |
| `ex05_baseline.py` | Beat a trivial baseline, or report honestly that you did not. |

## Compute budget

CPU only. Every exercise in this module runs on a laptop in under a minute.

## Common mistakes this module must address

- **Scaling before splitting** — The scaler saw the test set. The score is optimistic and the deployment is worse.
- **Random splitting time series** — The model predicts the past from the future. It will never do that again in production.
- **Tuning on the test set** — Your test estimate becomes a training estimate. Keep a set you have looked at exactly once.
- **Reporting accuracy on imbalanced data** — Ninety-nine percent accuracy on a one percent positive rate is a constant predictor.

## Self check questions

1. What are the three components of a learning problem?
2. What does a validation set answer that a training set cannot?
3. Give an example of target leakage that would look like an excellent result.
4. When is a grouped split required?
5. How do learning curves distinguish high bias from high variance?

## Going deeper

- Hastie, Tibshirani, Friedman, The Elements of Statistical Learning, chapter 7
- Google's Rules of Machine Learning
