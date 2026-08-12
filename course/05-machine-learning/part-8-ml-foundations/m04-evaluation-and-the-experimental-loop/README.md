# Module M04 — Evaluation, Data, and the Experimental Loop

**Level:** 05 Machine Learning, Part 8 (Foundations of Learning)  |  **Time:** L4 E6  |  **Prerequisite:** Module M03

> **Status: curriculum outline.** The full lesson, notebooks, exercises, and
> solutions are written in a later build pass. This file specifies exactly what
> the module must contain, so the build can resume without re-deriving anything.

---

## Why this module

The difference between a practitioner and a hobbyist is not the model, it is the
loop: whether the next experiment is chosen by evidence or by mood. This module
builds that discipline while the models are still simple enough to run in
seconds, so it is already a habit by the time a training run costs a day. It
also settles metrics properly, because a project optimising the wrong number
will do so very efficiently.

## What you will be able to do

- Choose a metric that matches the decision the model will inform.
- Read a confusion matrix and a precision-recall curve and act on them.
- Run cross validation correctly, including in grouped and temporal settings.
- Perform error analysis and turn it into the next experiment.
- Make an experiment reproducible by another person on another machine.

## Concept sections

1. **Metrics as decisions** — Accuracy, precision, recall, F1, ROC AUC, PR AUC, log loss, MAE, RMSE, MAPE. For each: the decision it serves and the situation where it lies.
2. **Imbalanced problems** — Why accuracy is useless, what resampling really does, threshold selection, and cost-sensitive evaluation.
3. **Calibration** — A probability that means what it says. Reliability diagrams, Platt scaling, and why calibration matters more than ranking when the number is shown to a human.
4. **Cross validation** — k-fold, stratified, grouped, and time series splits. Nested cross validation when hyperparameters are tuned.
5. **Error analysis** — Reading your worst predictions. Slicing performance by subgroup. Turning a pattern in the errors into a hypothesis and a next step.
6. **Baselines and ablations** — The trivial predictor, the previous model, and the one-change-at-a-time discipline that makes a result attributable.
7. **Reproducibility** — Seeds, environment pinning, data versioning, and experiment tracking. A run you cannot reproduce is an anecdote.

## What you build

An experiment harness you reuse for the rest of the level: a config, a seeded
run, logged metrics, saved artefacts, and a comparison report across runs.
Built on the packaging and CLI habits from Advanced Modules 20 and 30.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_choose_a_metric.md` | Pick and defend a metric for ten described products. |
| `ex02_imbalance.py` | Show accuracy, F1, and PR AUC disagreeing on the same model. |
| `ex03_calibration.py` | Diagnose an uncalibrated model and fix it. |
| `ex04_cv.py` | Implement grouped and temporal cross validation and compare estimates. |
| `ex05_harness.py` | Build the reusable experiment harness with tracking and seeds. |
| `ex06_error_analysis.md` | Analyse a hundred errors and propose the next three experiments. |

## Compute budget

CPU only.

## Common mistakes this module must address

- **Optimising a metric nobody asked for** — The model improves and the product does not.
- **Tuning inside the cross validation loop without nesting** — The estimate is optimistic by more than most improvements are worth.
- **Not fixing seeds** — Two runs differ and you cannot tell whether your change did anything.
- **Ignoring subgroup performance** — An average can hide a group the model fails completely.

## Self check questions

1. When is PR AUC more informative than ROC AUC?
2. What is model calibration and when does it matter more than accuracy?
3. Why must hyperparameter tuning be nested inside cross validation?
4. What does an ablation establish that a comparison does not?
5. What would another person need to reproduce your last experiment exactly?

## Going deeper

- Google's Machine Learning Crash Course, classification section
- Andrew Ng, Machine Learning Yearning
