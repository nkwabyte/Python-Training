# Solutions & Commentary — Module M10: Sequences and Attention

## Key Takeaways
- Recurrent Neural Networks (RNNs/LSTMs) pass hidden states sequentially, suffering from vanishing gradients over long horizons.
- Scaled Dot-Product Attention $\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$ enables direct $O(1)$ path lengths across all sequence tokens.
