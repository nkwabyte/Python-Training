# Solutions & Commentary — Module M15: Tokenisation and Language Modelling

## Key Takeaways
- Byte Pair Encoding (BPE) merges frequent byte pairs iteratively to construct subword vocabularies.
- Perplexity $\text{PPL} = \exp\left(-\frac{1}{N}\sum \log P(w_t)\right)$ measures next-token prediction certainty.
- Generation sampling: Temperature scaling, Top-$k$, and Top-$p$ (Nucleus) sampling.
