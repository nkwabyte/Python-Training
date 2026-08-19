# Solutions & Commentary — Module M12: Autoencoders and VAEs

## Key Takeaways
- Autoencoders compress inputs into a latent bottleneck $z$ and reconstruct via a decoder.
- Variational Autoencoders (VAEs) enforce a Gaussian prior $\mathcal{N}(0, I)$ on latents using KL Divergence loss.
- The Reparameterization Trick ($z = \mu + \sigma \odot \epsilon$) allows backpropagation through stochastic sampling.
