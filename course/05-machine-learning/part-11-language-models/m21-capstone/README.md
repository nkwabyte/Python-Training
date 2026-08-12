# Module M21 — Capstone: Build, Fine-tune, Evaluate, and Ship

**Level:** 05 Machine Learning, Part 11 (Language Models and LLMs)  |  **Time:** P24  |  **Prerequisite:** Modules M01 to M19

> **Status: curriculum outline.** The full lesson, notebooks, exercises, and
> solutions are written in a later build pass. This file specifies exactly what
> the module must contain, so the build can resume without re-deriving anything.

---

## Why this module

The capstone is a single project carried the whole distance: a real problem, a
dataset you built, a model you adapted, an evaluation that could reject your own
work, a service that serves it, and a written document that defends every choice
including the ones you got wrong. It is the artefact that demonstrates the level
was completed, and it is deliberately shaped like the work rather than like an
exercise.

## What you will be able to do

- Take a vague problem to a specification with a measurable success criterion.
- Justify the model and method choice against two rejected alternatives.
- Build a dataset and an evaluation before training anything.
- Ship the result as a service with monitoring and a cost model.
- Defend the whole thing against a review checklist.

## Concept sections

1. **Choosing a project** — Three worked briefs at the right scope, plus the criteria for bringing your own. What makes a project too large to finish and too small to prove anything.
2. **The specification** — The decision the model informs, the success metric, the latency and cost budget, and the failure modes you will accept.
3. **Data first** — Sourcing, licensing, cleaning, annotation, and the held-out set built and frozen before any training.
4. **The modelling ladder** — Baseline, prompted, retrieval, fine-tuned. Climb it in order and record what each rung bought.
5. **Evaluation as a gate** — The suite that decides whether the model ships, written before the model exists.
6. **Shipping** — The service, the monitoring, the runbook, and the rollback plan.
7. **The write-up** — A design document in the format of Module 36: problem, constraints, options considered, decision, evidence, risks, and what you would do next with double the budget.

## What you build

One complete project: specification, dataset, evaluation suite, trained or
fine-tuned model, deployed service, monitoring, cost model, and a design
document that would survive a review by someone who disagrees with you.

## Exercises to build

| File | What it drills |
|---|---|
| `stage1_spec.md` | Specification with a measurable success criterion and a budget. |
| `stage2_data.py` | Dataset built, documented, split, and frozen. |
| `stage3_evals.py` | Evaluation suite written before the model. |
| `stage4_model.py` | Climb the modelling ladder, recording what each rung bought. |
| `stage5_serve.py` | Deploy with monitoring and a load test. |
| `stage6_writeup.md` | The design document, defended against the review checklist. |

## Compute budget

Scoped to whatever you have. The briefs come in three sizes: CPU only, single consumer GPU, and hosted GPU, each with a target that is achievable on that hardware.

## Common mistakes this module must address

- **Choosing the model before the metric** — Then no result can be called good or bad.
- **Building the evaluation after the model** — It will be shaped by what the model happens to do well.
- **Skipping the baseline** — Without it there is no claim to make.
- **Writing the document last** — Write it as you go. The decisions are only recoverable while you remember them.

## Self check questions

1. What decision does your model inform, and what does it cost to get it wrong?
2. Which two alternatives did you reject, and on what evidence?
3. What would make you roll this back after deployment?
4. What does your feature cost per thousand requests?
5. What would you build first with twice the budget?

## Going deeper

- Chip Huyen, Designing Machine Learning Systems
- System Design Module 36, whose review checklist this capstone reuses
