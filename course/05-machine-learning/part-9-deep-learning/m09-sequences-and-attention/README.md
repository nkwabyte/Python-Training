# Module M09 — Sequences, Recurrence, and the Road to Attention

**Level:** 05 Machine Learning, Part 9 (Deep Learning with PyTorch)  |  **Time:** L4 E6  |  **Prerequisite:** Module M08

> **Status: curriculum outline.** The full lesson, notebooks, exercises, and
> solutions are written in a later build pass. This file specifies exactly what
> the module must contain, so the build can resume without re-deriving anything.

---

## Why this module

Attention is usually taught as a formula to accept. Taught after recurrence, it
is instead an answer to a specific failure: a fixed-size state cannot carry a
long sequence, and sequential computation cannot be parallelised. This module
builds the RNN, finds both walls honestly, and then derives attention as the
thing that removes them, which makes the next module feel inevitable rather
than arbitrary.

## What you will be able to do

- Implement an RNN cell and unroll it over a sequence.
- Explain vanishing gradients through time and what an LSTM gate actually gates.
- Describe the two limits of recurrence that attention removes.
- Implement scaled dot-product attention and interpret its weight matrix.
- Represent text as embeddings and explain what an embedding space encodes.

## Concept sections

1. **Sequence problems** — Classification, tagging, and generation. Why order carries meaning and a bag of features loses it.
2. **The RNN** — The recurrence, unrolling, and backpropagation through time. Implemented from scratch on a small task.
3. **Where it breaks** — Vanishing and exploding gradients over long sequences, and the sequential dependency that prevents parallel training.
4. **LSTM and GRU** — Gates as learned read, write, and forget. Why they extend the usable context without removing the wall.
5. **Embeddings** — Discrete tokens to dense vectors. What the geometry encodes, and how embeddings are learned rather than designed.
6. **Attention derived** — Query, key, value from a retrieval analogy. The dot product from Module M02 returns as a similarity score. Scaling, softmax, and the weighted sum.
7. **Reading attention** — Visualising the weight matrix on a real example, and being honest about what it does and does not explain.

## What you build

A character-level sequence model built twice: as an LSTM, and as a single
attention layer. Same data, same budget, with the training-time and quality
difference measured rather than asserted.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_rnn.py` | Implement an RNN cell and unroll it. |
| `ex02_vanishing.py` | Measure gradient magnitude by timestep and see it disappear. |
| `ex03_lstm.py` | Add gates and show the longer usable context. |
| `ex04_embeddings.py` | Train embeddings and explore the resulting geometry. |
| `ex05_attention.py` | Implement scaled dot-product attention and verify against PyTorch. |
| `ex06_compare.md` | Report the recurrence versus attention trade with your own numbers. |

## Compute budget

CPU is workable at the sizes used here. A GPU shortens the comparison exercise.

## Common mistakes this module must address

- **Forgetting to scale by the square root of the key dimension** — Softmax saturates and gradients vanish.
- **Confusing hidden size with sequence length** — Two different axes, one common bug.
- **Reading attention weights as explanation** — They show what was attended to, not why the output was produced.
- **Padding without masking** — The model attends to padding and learns from noise.

## Self check questions

1. What are the two limits of recurrence that attention removes?
2. What does the forget gate of an LSTM control?
3. Why divide the attention scores by the square root of the key dimension?
4. What does an embedding space encode that one-hot vectors cannot?
5. Why is a padding mask required?

## Going deeper

- Olah, Understanding LSTM Networks
- Bahdanau et al., Neural Machine Translation by Jointly Learning to Align and Translate
