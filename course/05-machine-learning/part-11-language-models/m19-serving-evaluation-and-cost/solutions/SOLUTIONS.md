# Solutions & Commentary — Module M19: Serving, Evaluation, and Cost

## Key Takeaways
- KV-Caching stores past Key and Value attention tensors, reducing token generation complexity from $O(N^2)$ to $O(N)$ per step.
- Continuous batching (vLLM) dynamically groups incoming generation requests to maximize GPU utilization.
