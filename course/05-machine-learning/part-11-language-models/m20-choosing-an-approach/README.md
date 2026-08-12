# Module M20 — Choosing an Approach: Matching Model to Problem

**Level:** 05 Machine Learning, Part 11 (Language Models and LLMs)  |  **Time:** L3 E8  |  **Prerequisite:** Modules M01 to M19

> **Status: curriculum outline.** The full lesson, notebooks, exercises, and
> solutions are written in a later build pass. This file specifies exactly what
> the module must contain, so the build can resume without re-deriving anything.

---

## Why this module

By this point you can train a dozen kinds of model, which is exactly when the
real failure mode appears: reaching for whichever one you most recently enjoyed.
Selection is a separate skill from execution and it has to be drilled, not
mentioned. This module gives you a decision procedure driven by constraints
rather than by fashion, then makes you commit to a choice on thirty short briefs
and defend it. It is placed here because the choice is only teachable once you
know what each option actually does, and immediately before the capstone so that
the capstone opens by applying it.

## What you will be able to do

- Extract a constraint sheet from a vague brief before naming any model.
- Decide whether the problem needs a learned model at all.
- Match a problem shape to a family of approaches, and justify the match.
- Climb the escalation ladder deliberately, stopping at the first rung that clears the bar.
- Write a model choice record that names the rejected alternatives and the evidence that would reverse the decision.

## Concept sections

1. **The prior question** — Does this need a model at all? Rules, heuristics, better instrumentation, a lookup, or a human in the loop. The permanent cost of a model that must be retrained, monitored, and explained.
2. **The constraint sheet** — Data volume, label availability and cost, latency budget, interpretability and regulatory requirements, cost of a wrong answer, cost of ownership, team skill, and iteration speed. Constraints first, always, because they eliminate more options than any benchmark.
3. **Problem shape to family** — Tabular, text, image, audio, time series, graph, recommendation, ranking, and anomaly detection. For each: the honest first choice, the signal that you should escalate, and the approach people wrongly reach for first.
4. **The escalation ladder** — Trivial baseline, classical model, deep model, pretrained model, fine-tuned model, custom pretraining. Each rung costs roughly an order of magnitude more than the last in effort and in maintenance, so each needs evidence, not enthusiasm.
5. **The language model ladder in particular** — Prompt, few-shot, retrieval, fine-tune, continued pretraining. The specific symptom that tells you the current rung has stopped working, drawn from Modules M17 and M18.
6. **Data volume and the rules of thumb** — What tends to be true at a hundred, a thousand, a hundred thousand, and ten million labelled examples, stated as tendencies with their exceptions named.
7. **Cost, latency, and build against buy** — Total cost of ownership over a year, not the cost of the experiment. API, hosted, and self-hosted compared with real arithmetic, including the engineer-hours that never appear on the invoice.
8. **The model choice record** — One page: the decision, the constraints that drove it, two alternatives rejected with reasons, the evidence that would reverse it, and the review date. Reuses the design document discipline of System Design Module 36.
9. **What ages and what does not** — Model names and benchmark rankings date within a year. Constraints, ladders, and the discipline of writing the decision down do not. The one section of this module that is expected to be rewritten is marked as such and dated.

## What you build

Your own decision procedure, applied: a completed constraint sheet and model
choice record for the capstone in Module M21, plus written answers to the case
drills with the reasoning preserved rather than only the conclusions.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_constraints.md` | Extract a constraint sheet from ten deliberately vague briefs. |
| `ex02_cases.md` | Thirty short cases: commit to an approach and state what would change your mind. |
| `ex03_no_model.md` | Six problems where the right answer is not machine learning. Identify them and say what is. |
| `ex04_escalate.py` | Climb the ladder on one dataset and record what each rung actually bought. |
| `ex05_postmortems.md` | Five projects that chose wrong. Diagnose the decision, not the model. |
| `ex06_record.md` | Write the model choice record for your capstone. |
| `ex07_defend.md` | Defend one choice against a reviewer arguing the opposite position. |
| `ex08_revisit.md` | Re-examine your own choices from Modules M06 to M19 with the procedure in hand. |

## Compute budget

CPU only, apart from ex04, which reuses checkpoints you already trained earlier in the level.

## Common mistakes this module must address

- **Choosing the model before the metric** — Nothing can then be called better or worse, only newer.
- **Escalating because the higher rung is more interesting** — The most expensive form of curiosity in the field.
- **Costing the experiment rather than the year** — Retraining, monitoring, on-call, and explanation are the actual bill.
- **Assuming more data always beats a better prior** — At small data volumes the prior wins, which is the whole argument of Module M05.
- **Treating a hosted API as free of ownership** — Prompt drift, version deprecation, rate limits, and vendor risk are ownership.
- **Using a public leaderboard as evidence for your problem** — Different data, different distribution, and often contaminated.

## Self check questions

1. What are the first three questions to ask about a new problem, before any model is named?
2. What evidence justifies moving one rung up the escalation ladder?
3. For a tabular problem with eight thousand rows, what do you try first and why?
4. When does retrieval solve a problem that fine-tuning cannot, and when is it the reverse?
5. What belongs in a model choice record, and when should it be revisited?
6. Name a problem where the correct decision is not to build a model.

## Going deeper

- Chip Huyen, Designing Machine Learning Systems, chapter 6
- Google's Rules of Machine Learning, rules 1 to 15
- Grinsztajn, Oyallon, Varoquaux, Why do tree-based models still outperform deep learning on typical tabular data?
