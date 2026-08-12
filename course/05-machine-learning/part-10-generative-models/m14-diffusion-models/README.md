# Module M14 — Diffusion Models

**Level:** 05 Machine Learning, Part 10 (Generative Models)  |  **Time:** L5 E9  |  **Prerequisite:** Module M13

> **Status: curriculum outline.** The full lesson, notebooks, exercises, and
> solutions are written in a later build pass. This file specifies exactly what
> the module must contain, so the build can resume without re-deriving anything.

---

## Why this module

Diffusion displaced GANs for image generation by replacing one hard problem with
many easy ones: instead of learning to produce an image in a single step, learn
to remove a little noise, repeatedly. That reframing is the whole idea, and it is
simple enough to implement from scratch. Doing so also demystifies the image
tools the learner already uses, and sets up the guidance and conditioning ideas
that reappear in multimodal work.

## What you will be able to do

- Explain the forward noising process and why it has a closed form.
- Implement a DDPM training loop and sample from it.
- Describe what the network is actually predicting and why that target was chosen.
- Apply classifier-free guidance and explain the quality-versus-diversity trade.
- Compare diffusion with GANs and VAEs on the axes that matter in practice.
- Adapt a pretrained diffusion model to a new subject or style on consumer
  hardware, and evaluate the result against the base model.

## Concept sections

1. **The reframing** — Many small denoising steps instead of one generative leap. Why that is easier to train and slower to sample.
2. **The forward process** — Adding Gaussian noise on a schedule, and the closed form that lets you jump to any timestep in one operation.
3. **The reverse process** — Learning to predict the noise. The training objective in its final, surprisingly simple form.
4. **The network** — A U-Net with timestep conditioning. Why this architecture, and what the skip connections carry.
5. **Sampling** — DDPM and DDIM, step count against quality, and the schedule choices that control it.
6. **Conditioning and guidance** — Text conditioning, classifier-free guidance, and the guidance scale as a diversity dial.
7. **Latent diffusion** — Running the process in a compressed latent space instead of pixel space. The idea that made these models affordable.
8. **Adapting a pretrained diffusion model** — LoRA adapters on the attention layers, DreamBooth-style subject fine-tuning with a prior-preservation term, and textual inversion as the cheapest option of the three. What each one actually changes, how many images each needs, and the overfitting signature of each.
9. **Controlling generation** — Conditioning on structure rather than text, image-to-image strength, inpainting, and where the control comes from in each case.

## What you build

A DDPM implemented from scratch and trained on a small image dataset, with a
sampling loop you wrote, a guidance scale you can turn, and a comparison against
your GAN from Module M13 on sample quality, diversity, and wall-clock cost. Then an adapted model: a pretrained diffusion checkpoint
fine-tuned with LoRA on a subject of your own, with the adapter file, a
before-and-after grid at fixed seeds, and an honest note on what it broke.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_forward.py` | Implement the noising schedule and verify the closed form. |
| `ex02_train.py` | Train a small DDPM to convergence. |
| `ex03_sample.py` | Implement DDPM and DDIM sampling and compare step counts. |
| `ex04_guidance.py` | Add classifier-free guidance and chart the quality-diversity trade. |
| `ex05_compare.md` | Compare diffusion, GAN, and VAE with your own numbers. |
| `ex06_lora.py` | Fine-tune a pretrained diffusion model with LoRA and ship the adapter. |
| `ex07_dreambooth.py` | Subject fine-tuning with prior preservation, and the same run without it. |
| `ex08_control.py` | Condition on structure and on an input image, and measure how much control each gives. |

## Compute budget

A GPU is effectively required for the full training exercise. The module ships a reduced 16 by 16 configuration that completes on CPU, and a pretrained checkpoint so the sampling and guidance exercises can be done without training. The adaptation exercises need a GPU with about 8GB, or a free hosted notebook: LoRA fine-tuning of a pretrained model on a dozen images is a matter of minutes, which is exactly why it is the technique people actually use.

## Common mistakes this module must address

- **Mismatching the training and sampling schedules** — Samples come out as noise and the bug is in the bookkeeping, not the model.
- **Forgetting timestep conditioning** — One network cannot serve every noise level without knowing which one it is at.
- **Turning guidance up too far** — Sharper, more uniform, and less diverse. The trade is real.
- **Expecting fast sampling** — It is many forward passes. That is the cost of the reframing.
- **Training a subject fine-tune without prior preservation** — The model forgets the class and every prompt returns your subject.
- **Comparing before and after at different seeds** — Fix the seed and the sampler, or the comparison shows nothing.

## Self check questions

1. What does the network predict at each timestep?
2. Why does the forward process have a closed form, and why does that matter?
3. What does classifier-free guidance trade away for quality?
4. Why is DDIM sampling faster than DDPM?
5. What does latent diffusion change about the cost?
6. What does a LoRA adapter modify in a diffusion model, and how large is it?
7. What is prior preservation protecting against?
8. When is textual inversion enough, and when do you need DreamBooth?

## Going deeper

- Ho et al., Denoising Diffusion Probabilistic Models
- Lilian Weng, What are Diffusion Models?
- Ruiz et al., DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation
- The Hugging Face Diffusers training documentation
