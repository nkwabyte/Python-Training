# Solutions & Commentary — Module 30: Packaging, Deployment, and Ops

## Overview of Exercises

This module covered modern Python packaging standards with `pyproject.toml`, multi-stage Docker builds with non-root security, and GitHub Actions CI pipelines.

---

## Exercise 30.1: Package Layout with pyproject.toml

### Key Takeaways
- The `src/` layout prevents accidental imports of uninstalled local package folders during testing, ensuring that tests run against the installed wheel / editable build.
- `[project.scripts]` generates cross-platform executable wrappers in virtual environment `bin/` or `Scripts/` paths.

---

## Exercise 30.2: Production Dockerfile

### Key Takeaways
- Building in a dedicated `builder` stage and copying only `/opt/venv` to the runtime image keeps compilers, build tools, and cache files out of the deployment image, reducing image size by up to 80%.
- Running as non-root (`USER appuser`) mitigates container escape vulnerabilities.

---

## Exercise 30.3: CI Matrix Workflows

### Key Takeaways
- Splitting fast lint/type stages from testing matrices saves cloud compute credits.
- Matrix testing across supported Python minor versions prevents regression when utilizing newer standard library or syntax features.
