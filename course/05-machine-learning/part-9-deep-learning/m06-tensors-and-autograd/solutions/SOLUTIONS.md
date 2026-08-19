# Solutions & Commentary — Module M06: Tensors and Autograd

## Key Takeaways
- PyTorch tensors wrap contiguous memory buffers with GPU device placement (`tensor.to('cuda')` / `tensor.to('mps')`).
- Autograd tracks computational graphs dynamically; calling `loss.backward()` populates `.grad` attributes across trainable parameters.
