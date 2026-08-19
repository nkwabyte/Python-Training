# Solutions & Commentary — Module M17: Pretrained Models & Hugging Face

## Key Takeaways
- VRAM budgeting: Model weights in 16-bit float require $2 \times \text{Params}$ bytes; optimizer states (AdamW) require $8 \times \text{Params}$ bytes.
- Post-Training Quantization (8-bit / 4-bit NF4) cuts VRAM consumption by 50-75% with minimal perplexity degradation.
