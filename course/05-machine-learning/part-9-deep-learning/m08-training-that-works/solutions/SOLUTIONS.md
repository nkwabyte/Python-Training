# Solutions & Commentary — Module M08: Training That Actually Works

## Key Takeaways
- Sanity check: verify that your model can overfit a tiny batch of 10 samples to zero loss before training on full datasets.
- Normalization layers (BatchNorm, LayerNorm) stabilize activations and prevent vanishing/exploding gradients.
- Learning rate schedulers: Cosine Annealing with Warmup.
