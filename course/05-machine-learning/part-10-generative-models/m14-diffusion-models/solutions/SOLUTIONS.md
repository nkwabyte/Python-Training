# Solutions & Commentary — Module M14: Diffusion Models

## Key Takeaways
- Forward diffusion adds Gaussian noise gradually according to a variance schedule $\beta_t$.
- Reverse diffusion trains a U-Net to predict added noise $\epsilon_\theta(x_t, t)$ at timestep $t$.
- Classifier-Free Guidance (CFG) balances generation diversity vs prompt fidelity.
