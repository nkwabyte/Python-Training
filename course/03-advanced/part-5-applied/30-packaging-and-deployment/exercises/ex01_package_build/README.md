# Exercise 30.1 — Packaging a Python Project with pyproject.toml

**Directory:** `ex01_package_build/`
**Files:** `pyproject.toml`, `src/pkgdemo/`, `tests/test_core.py`
**Estimated Time:** 35 minutes

---

## Background & Objective

Under modern PEP 621 / PEP 517 specifications, Python projects define their build metadata, dependencies, and command-line scripts in `pyproject.toml`.

In this exercise, you will explore the standard `src/` layout, install the package in editable mode, run tests, and verify CLI entrypoint registration.

---

## Instructions

1. Inspect `pyproject.toml` and observe:
   - `[build-system]` declaring `hatchling`.
   - `[project]` containing project metadata, authors, and Python version constraints.
   - `[project.scripts]` defining the `pkgdemo` executable pointing to `pkgdemo.core:main`.
2. Install the package in editable mode into your virtual environment:
   ```bash
   pip install -e .
   ```
3. Run the pytest test suite:
   ```bash
   pytest
   ```
4. Test running the CLI script directly:
   ```bash
   pkgdemo Ada
   ```
