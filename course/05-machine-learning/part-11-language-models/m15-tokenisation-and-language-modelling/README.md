# Module M15 — Tokenisation and Language Modelling

**Level:** 05 Machine Learning, Part 11 (Language Models and LLMs)  |  **Time:** L4 E6  |  **Prerequisite:** Module M11 (Module M14 optional)

> **Status: curriculum outline.** The full lesson, notebooks, exercises, and
> solutions are written in a later build pass. This file specifies exactly what
> the module must contain, so the build can resume without re-deriving anything.

---

## Why this module

Nearly every confusing behaviour of a language model traces back to two things
taught here: what a token is, and what next-token prediction does and does not
optimise. Counting characters, arithmetic failures, non-English cost, prompt
length limits, and the shape of sampling artefacts all become obvious once
tokenisation is concrete. This module is short, unglamorous, and prevents more
confusion per page than any other in the level.

## What you will be able to do

- Explain byte pair encoding and train a tokeniser on your own corpus.
- Predict how a given string will tokenise and why the count matters for cost.
- State the language modelling objective and compute perplexity correctly.
- Choose sampling parameters deliberately and describe their effect on output.
- Explain several well-known model failures as tokenisation artefacts.

## Concept sections

1. **From characters to tokens** — Character, word, and subword tokenisation. The vocabulary size trade, and why subword won.
2. **Byte pair encoding** — The merge algorithm, implemented from scratch on a small corpus. Byte-level BPE and why it never fails on unseen input.
3. **Tokenisation in practice** — Special tokens, chat templates, and the padding and truncation decisions that quietly change results.
4. **Why tokens explain the weirdness** — Character counting, arithmetic, rhyming, and why some languages cost several times more per sentence.
5. **The language modelling objective** — Next-token prediction, teacher forcing, and cross entropy over the vocabulary. What this objective rewards and what it never mentions.
6. **Perplexity** — The metric, its interpretation as an effective branching factor, and why it is not comparable across tokenisers.
7. **Sampling** — Greedy, beam, temperature, top-k, top-p, and repetition penalties. The determinism and diversity trade, demonstrated on one prompt.

## What you build

A byte pair encoding tokeniser of your own, trained on a corpus you choose,
compared against a production tokeniser on vocabulary size, compression ratio,
and how it fragments unusual text.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_bpe.py` | Implement BPE training and encoding from scratch. |
| `ex02_explore.py` | Tokenise fifteen tricky strings and explain each result. |
| `ex03_perplexity.py` | Compute perplexity and show why cross-tokeniser comparison is invalid. |
| `ex04_sampling.py` | Sweep temperature, top-k, and top-p on one prompt and characterise the output. |
| `ex05_artefacts.md` | Explain six known model failures in terms of tokenisation. |

## Compute budget

CPU only. Tokeniser training on a modest corpus takes minutes.

## Common mistakes this module must address

- **Assuming a token is a word** — It is roughly three quarters of one in English and much less elsewhere.
- **Comparing perplexity across tokenisers** — The denominator is different. The comparison is meaningless.
- **Forgetting the chat template** — An instruction-tuned model given raw text behaves like a different model.
- **Setting temperature to zero and expecting determinism** — Batching, hardware, and kernel choice still introduce variation.

## Self check questions

1. Why did subword tokenisation win over word-level?
2. Why can a model struggle to count the letters in a word?
3. What does perplexity measure, in plain words?
4. What is the difference between top-k and top-p sampling?
5. Why does the same text cost more in some languages?

## Going deeper

- Karpathy, Let's build the GPT Tokenizer
- Sennrich et al., Neural Machine Translation of Rare Words with Subword Units
