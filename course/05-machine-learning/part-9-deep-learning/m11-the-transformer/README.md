# Module M11 — The Transformer, Built from Parts

**Level:** 05 Machine Learning, Part 9 (Deep Learning with PyTorch)  |  **Time:** L5 E8  |  **Prerequisite:** Module M10

> **Status: curriculum outline.** The full lesson, notebooks, exercises, and
> solutions are written in a later build pass. This file specifies exactly what
> the module must contain, so the build can resume without re-deriving anything.

---

## Why this module

Every model in Part 11 is this architecture with different data and different
scale, so it is built here once, completely, from tensors up, and checked
against the reference implementation. Learners who skip this step spend the rest
of their careers treating language models as opaque; learners who do it can read
any paper in the field, because almost all of them describe a modification to
one of the blocks assembled in this module.

## What you will be able to do

- Implement multi-head self-attention, including masking, from scratch.
- Explain what each component of a transformer block contributes.
- Compare positional encoding schemes and say what rotary embeddings fix.
- Distinguish encoder, decoder, and encoder-decoder models by what they can see.
- State the memory and compute cost of attention as sequence length grows.

## Concept sections

1. **From one head to many** — Splitting the representation, attending in parallel subspaces, and recombining. The shape choreography written out in full.
2. **Masking** — Causal masks for generation, padding masks for batches. The single most common transformer bug lives here.
3. **The block** — Attention, feed-forward, residual connections, and layer norm. Pre-norm versus post-norm and why the field moved.
4. **Positional information** — Why attention is permutation invariant without it. Sinusoidal, learned, and rotary embeddings, and what each buys.
5. **Encoder, decoder, and both** — BERT-style, GPT-style, and T5-style, distinguished by what each token is allowed to see.
6. **The cost of attention** — Quadratic in sequence length in both time and memory. What that implies for context windows, and the direction of the efficient-attention literature.
7. **Verifying your build** — Testing your implementation against nn.MultiheadAttention numerically, then loading real pretrained weights into your own module as the final proof.

## What you build

A complete transformer implementation of your own: multi-head attention, block,
stack, and generation. Verified numerically against PyTorch, then made to run
with real pretrained weights loaded into it.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_multihead.py` | Implement multi-head attention and match PyTorch to floating point tolerance. |
| `ex02_masks.py` | Build causal and padding masks and show the failure without each. |
| `ex03_block.py` | Assemble the block and compare pre-norm with post-norm stability. |
| `ex04_positions.py` | Compare three positional schemes on a length-sensitive task. |
| `ex05_cost.py` | Measure attention time and memory against sequence length and fit the curve. |
| `ex06_load_weights.py` | Load pretrained weights into your own implementation and reproduce its outputs. |

## Compute budget

CPU for correctness work, GPU preferred for the cost measurements at longer sequences.

## Common mistakes this module must address

- **Getting the causal mask off by one** — The model sees the token it is predicting. Loss looks wonderful and generation is nonsense.
- **Applying softmax over the wrong axis** — Attention over the batch instead of over positions.
- **Forgetting to scale, again** — It matters more at larger head dimensions.
- **Assuming more heads is better** — Head dimension shrinks as heads grow. There is a trade, not a free win.

## Self check questions

1. What does the causal mask prevent, and what happens without it?
2. Why does a transformer need positional information at all?
3. What does the feed-forward layer contribute that attention does not?
4. How does attention memory scale with sequence length?
5. What distinguishes a BERT-style model from a GPT-style one?

## Going deeper

- Vaswani et al., Attention Is All You Need
- The Annotated Transformer, Harvard NLP
