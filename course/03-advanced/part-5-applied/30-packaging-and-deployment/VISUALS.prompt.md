# Visual Companion Prompt — Module 30: Packaging, Deployment, and Ops

## Video Steering Prompt
> Create a step-by-step visual animation demonstrating the Python packaging and deployment pipeline. Illustrate the source tree transformation into wheel (`.whl`) and sdist (`.tar.gz`) archives under PEP 517/621 specifications. Diagram a multi-stage Docker build separating the compilation/wheel-building toolchain stage from the slim runtime container running as a non-root user. Visualize the GitHub Actions CI matrix executing parallel linting, type-checking, and pytest runs.

## Key Concepts
- `pyproject.toml` configuration under PEP 621
- Wheels vs Source Distributions (sdists)
- Multi-stage Docker container architecture
- Non-root user privileges and container security
- Signal forwarding (`SIGTERM`) and graceful process shutdown
- Continuous Integration workflows with GitHub Actions
