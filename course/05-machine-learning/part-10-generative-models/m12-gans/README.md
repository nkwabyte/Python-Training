# Module M12 — Generative Adversarial Networks

**Level:** 05 Machine Learning, Part 10 (Generative Models)  |  **Time:** L5 E7  |  **Prerequisite:** Module M11

> **Status: curriculum outline.** The full lesson, notebooks, exercises, and
> solutions are written in a later build pass. This file specifies exactly what
> the module must contain, so the build can resume without re-deriving anything.

---

## Why this module

A GAN replaces a hand-written loss with a second network that learns what wrong
looks like, which is an idea worth understanding whether or not you ever ship
one. It is also the best available lesson in training instability: two networks
optimising against each other produce failure modes that no single-objective
model can, and diagnosing them teaches a level of attention to training dynamics
that transfers directly to fine-tuning large models later.

## What you will be able to do

- Explain the minimax objective and what equilibrium would mean.
- Implement and train a DCGAN on an image dataset.
- Recognise mode collapse, discriminator dominance, and oscillation from their signatures.
- Apply the stabilising techniques and say which failure each one addresses.
- Evaluate a generative model with something better than looking at it.

## Concept sections

1. **The adversarial idea** — Generator and discriminator, the minimax game, and the learned loss. Why this is different from every objective so far.
2. **Why it is unstable** — Non-stationary objectives, no single loss to monitor, and the equilibrium you are aiming at rather than a minimum.
3. **DCGAN** — The architectural choices that first made GANs trainable: strided convolutions, batch norm placement, and activation choices.
4. **Failure modes** — Mode collapse, discriminator dominance, vanishing generator gradients, and oscillation. Each shown, with the plot that reveals it.
5. **Stabilising** — Wasserstein loss, gradient penalty, spectral normalisation, two time-scale updates, and label smoothing. Which failure each targets.
6. **Conditional and controllable generation** — Class-conditional GANs, image-to-image translation, and the idea of steering a generator.
7. **Evaluation** — Inception Score, FID, precision and recall for generative models, and the honest limits of all of them.

## What you build

A DCGAN trained to convergence on a small image dataset, then upgraded to
WGAN-GP, with FID measured for both and a written account of every failure mode
you hit and what fixed it.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_dcgan.py` | Implement and train a DCGAN end to end. |
| `ex02_collapse.py` | Induce mode collapse deliberately and identify its signature. |
| `ex03_wgan_gp.py` | Add the Wasserstein loss and gradient penalty and compare stability. |
| `ex04_conditional.py` | Condition generation on a class label. |
| `ex05_fid.py` | Implement FID and rank your own checkpoints with it. |
| `ex06_diary.md` | A training diary: every failure, its symptom, and the fix that worked. |

## Compute budget

A GPU is strongly recommended here. On CPU, use the 32 by 32 configuration and expect an hour per experiment; this is the module where a free hosted GPU notebook is worth the setup.

## Common mistakes this module must address

- **Reading the losses as progress** — Both losses can look fine while the samples are garbage. Look at samples and FID.
- **Unbalanced training** — One network overwhelms the other. Watch the discriminator accuracy.
- **Batch norm in the discriminator with a gradient penalty** — They interact badly. Use layer or instance norm.
- **Judging by cherry-picked samples** — Report a random grid and a metric, always.

## Self check questions

1. What is the generator actually optimising?
2. What does mode collapse look like in the samples and in the metrics?
3. What does the gradient penalty enforce, and why does that help?
4. Why is FID preferred to Inception Score?
5. Why can you not use the loss curve to decide when a GAN has finished training?

## Going deeper

- Goodfellow et al., Generative Adversarial Networks
- Gulrajani et al., Improved Training of Wasserstein GANs
