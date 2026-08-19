# Solutions & Commentary — Module M18: Fine-Tuning and Alignment

## Key Takeaways
- LoRA (Low-Rank Adaptation) decomposes weight updates into low-rank matrices $\Delta W = B \cdot A$ with rank $r \ll d$, tuning <1% of parameters.
- Direct Preference Optimization (DPO) aligns LLMs directly on preferred vs rejected completions without training an unstable reward model.
