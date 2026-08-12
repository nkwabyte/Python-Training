# Module M11 — Autoencoders and Variational Autoencoders

**Level:** 05 Machine Learning, Part 10 (Generative Models)  |  **Time:** L4 E6  |  **Prerequisite:** Module M10

> **Status: curriculum outline.** The full lesson, notebooks, exercises, and
> solutions are written in a later build pass. This file specifies exactly what
> the module must contain, so the build can resume without re-deriving anything.

---

## Why this module

Generative modelling begins with a question that is different in kind from
prediction: not what is the label, but what does the data look like. The
autoencoder introduces the idea of a compressed latent space you can inspect,
and the variational autoencoder turns that space into a distribution you can
sample from. The reparameterisation trick taught here is the technique that makes
the whole family trainable, and it recurs in diffusion and in reinforcement
learning.

## What you will be able to do

- Train an autoencoder and interpret its latent space.
- Explain why a plain autoencoder cannot generate reliably.
- Derive the VAE objective as reconstruction plus a KL term.
- Implement the reparameterisation trick and say what it makes possible.
- Diagnose posterior collapse and blurry reconstructions.

## Concept sections

1. **Generative versus discriminative** — Modelling the data distribution rather than a decision boundary. What each buys you.
2. **The autoencoder** — Encoder, bottleneck, decoder. Reconstruction loss. Denoising and sparse variants.
3. **Why sampling fails** — Holes in an unregularised latent space. Shown by decoding random points and looking at the result.
4. **The variational view** — A distribution over latents, the evidence lower bound, and the KL term as a pull toward the prior. Derived, not asserted.
5. **The reparameterisation trick** — Moving the randomness out of the path the gradient must travel. Three lines of code, one important idea.
6. **Latent space in practice** — Interpolation, arithmetic, disentanglement, and the beta weighting that trades reconstruction against structure.
7. **Honest limitations** — Blurriness and its cause, posterior collapse and its remedies, and where VAEs still win over GANs and diffusion.

## What you build

An autoencoder and a VAE on the same image dataset, with a latent space you can
walk through: interpolations between two inputs, samples from the prior, and a
side-by-side comparison of reconstruction quality.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_autoencoder.py` | Train an autoencoder and visualise the bottleneck. |
| `ex02_holes.py` | Decode random latents from a plain autoencoder and explain the failure. |
| `ex03_elbo.md` | Derive the ELBO and identify each term's job. |
| `ex04_vae.py` | Implement a VAE with the reparameterisation trick. |
| `ex05_beta.py` | Sweep the KL weight and chart the reconstruction-versus-structure trade. |
| `ex06_collapse.py` | Induce posterior collapse deliberately, then fix it. |

## Compute budget

A GPU is helpful but small images train on CPU in minutes. Every exercise is sized for a free hosted notebook at worst.

## Common mistakes this module must address

- **Summing the KL term over the wrong axis** — Silently rescales the objective and the samples degrade.
- **Using a reconstruction loss that contradicts the data** — Squared error on binary pixels, for instance.
- **Reading a blurry sample as a bug** — It follows from the objective. Know why before trying to fix it.
- **Weighting KL too heavily at the start** — The decoder ignores the latent entirely. Anneal it.

## Self check questions

1. Why can a plain autoencoder not be sampled from reliably?
2. What are the two terms of the ELBO and what does each encourage?
3. What problem does the reparameterisation trick solve?
4. What is posterior collapse and how would you notice it?
5. Why are VAE samples characteristically blurry?

## Going deeper

- Kingma and Welling, Auto-Encoding Variational Bayes
- Doersch, Tutorial on Variational Autoencoders
