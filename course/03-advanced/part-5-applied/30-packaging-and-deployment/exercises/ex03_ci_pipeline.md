# Exercise 30.3 — Continuous Integration with GitHub Actions

**Estimated Time:** 30 minutes

---

## Objective

Design a GitHub Actions CI workflow in `.github/workflows/ci.yml` that validates code quality, typing, and tests across multiple Python versions.

---

## Matrix CI Configuration

```yaml
name: Continuous Integration

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install Linting & Typing Tools
        run: pip install ruff mypy

      - name: Lint Codebase (Ruff)
        run: ruff check .

      - name: Type Check (Mypy)
        run: mypy src/

  test-matrix:
    needs: quality
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ['3.11', '3.12', '3.13']

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'

      - name: Install Package & Test Dependencies
        run: |
          pip install pytest pytest-cov
          pip install -e .

      - name: Run Test Suite with Coverage
        run: pytest --cov=src --cov-report=term-missing tests/
```

---

## Self-Check Questions

1. Why should `quality` (linting/formatting/types) run before the test matrix?
   - *Answer:* Lint checks run in seconds and fail fast, saving CI compute minutes on broken builds before spawning multi-version test matrices.
2. What does `fail-fast: false` achieve in a test matrix?
   - *Answer:* It allows tests to run to completion on all Python versions even if one version fails, providing full visibility across the compatibility matrix.
