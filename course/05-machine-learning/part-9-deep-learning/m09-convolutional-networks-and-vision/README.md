# Module M09 — Convolutional Networks and Vision

**Level:** 05 Machine Learning, Part 9 (Deep Learning with PyTorch)  |  **Time:** L4 E7  |  **Prerequisite:** Module M08

> **Status: curriculum outline.** The full lesson, notebooks, exercises, and
> solutions are written in a later build pass. This file specifies exactly what
> the module must contain, so the build can resume without re-deriving anything.

---

## Why this module

Convolution is the clearest example in the field of an architecture that encodes
a prior: nearby pixels are related, and a feature is worth detecting wherever it
appears. Understanding it that way generalises, which is why this module frames
attention later as a different prior rather than as a newer trick. It is also
the natural place to learn transfer learning, which is the same idea you will
apply to language models in Part 11.

## What you will be able to do

- Explain convolution, stride, padding, and channels in terms of shapes.
- Compute the receptive field and output size of a stack of layers.
- Fine-tune a pretrained vision model on a small dataset.
- Choose augmentations that reflect the invariances your problem actually has.
- Read a modern vision architecture and identify what each block contributes.

## Concept sections

1. **Convolution as a prior** — Locality and translation equivariance. Parameter sharing, and the count compared with a dense layer on the same input.
2. **The mechanics** — Kernels, stride, padding, dilation, channels. Output size arithmetic you can do in your head.
3. **Pooling and downsampling** — What is discarded and why. Strided convolution as the modern alternative.
4. **Receptive field** — How depth buys context. Computing it, and why it explains a model that cannot see the whole object.
5. **Architectures** — LeNet to AlexNet to VGG to ResNet. The residual connection as the single most important idea, connected back to gradient flow in Module M08.
6. **Transfer learning** — Freezing, unfreezing, discriminative learning rates, and why a pretrained backbone beats a bigger dataset most of the time.
7. **Augmentation** — Which transforms encode a true invariance for your problem, and the ones that quietly destroy the label.

## What you build

An image classifier for a small custom dataset: trained from scratch first,
then by fine-tuning a pretrained backbone, with the accuracy gap and the compute
gap both measured and explained.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_conv_by_hand.py` | Implement 2D convolution in NumPy and match PyTorch. |
| `ex02_shapes.md` | Compute output sizes and receptive fields for eight stacks. |
| `ex03_scratch.py` | Train a small CNN from scratch and record the baseline. |
| `ex04_finetune.py` | Fine-tune a pretrained backbone and beat the baseline with less compute. |
| `ex05_augment.py` | Show one augmentation helping and one destroying the label. |
| `ex06_interpret.py` | Visualise filters and activations to see what was learned. |

## Compute budget

A GPU makes this comfortable. Every exercise has a small-image fallback that trains on CPU in under fifteen minutes, and the fine-tuning exercise is the recommended free-notebook candidate.

## Common mistakes this module must address

- **Normalising with the wrong statistics when fine-tuning** — A pretrained model expects the preprocessing it was trained with.
- **Augmenting the validation set** — The metric stops being comparable across runs.
- **Training from scratch on two thousand images** — Fine-tune. Almost always.
- **Forgetting the channel order** — The most common shape bug in vision code.

## Self check questions

1. How many parameters does a 3 by 3 convolution with 64 input and 128 output channels have?
2. What does a residual connection do for the gradient?
3. Why does a pretrained backbone help on a completely different dataset?
4. What is the receptive field after three 3 by 3 convolutions?
5. Which augmentation would be wrong for a digit classifier?

## Going deeper

- CS231n convolutional networks notes
- He et al., Deep Residual Learning for Image Recognition
