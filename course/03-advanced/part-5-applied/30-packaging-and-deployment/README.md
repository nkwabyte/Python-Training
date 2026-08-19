# Module 30 — Packaging, Deployment, and Ops

**Time budget:** 5 hours lesson, 7 hours exercises
**Prerequisite:** Modules 06 (Modules & Packages), 18 (Testing), 20 (CLI Project)

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

Code on your laptop is a prototype; software running reliably in containers, passing CI checks on every commit, and installable via standard package managers is production engineering.

This module teaches modern Python distribution and operational standards:
1. **PEP 621 / PEP 517 packaging** with `pyproject.toml` and standard build backends (`hatchling`, `flit`).
2. **Production Dockerization**: Multi-stage builds, non-root user execution, layer caching, and signal forwarding (`exec`).
3. **Twelve-Factor App Configuration**: Environment variables, secrets hygiene, and graceful shutdowns.
4. **CI/CD Automation**: GitHub Actions workflows for linting, testing, and artifact publishing.

---

## 1. Modern Packaging with `pyproject.toml`

The legacy `setup.py` / `setup.cfg` format has been replaced by the unified `pyproject.toml` standard:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "logparser-pro"
version = "0.1.0"
description = "High-throughput log analysis engine"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "httpx>=0.25.0",
    "pydantic>=2.0.0",
]

[project.scripts]
logparser = "logparser.cli:main"

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "ruff>=0.3.0",
    "mypy>=1.9.0",
]
```

---

## 2. Multi-Stage Production Dockerfile

```dockerfile
# Stage 1: Build virtualenv
FROM python:3.12-slim AS builder

WORKDIR /app
RUN pip install --no-cache-dir uv

COPY pyproject.toml .
RUN uv venv /opt/venv && \
    uv pip install --python /opt/venv/bin/python .

# Stage 2: Final minimal runtime image
FROM python:3.12-slim AS runtime

# Create non-root system user
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/false appuser

WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY src/ /app/src/

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER appuser

EXPOSE 8000
CMD ["python", "-m", "src.main"]
```

---

## 3. GitHub Actions CI Pipeline

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install ruff mypy pytest
          pip install -e .
      
      - name: Lint with Ruff
        run: ruff check .
      
      - name: Type check with Mypy
        run: mypy src/
      
      - name: Run Test Suite
        run: pytest tests/ --cov=src
```

---

## Exercises

- `exercises/ex01_package_build/`: Standard PEP 621 package with `src/` layout, entrypoints, and build validation. (Contains `README.md`, `pyproject.toml`, source and test files).
- `exercises/ex02_docker_container.md`: Multi-stage Dockerfile authoring and security audit worksheet.
- `exercises/ex03_ci_pipeline.md`: GitHub Actions workflow authoring worksheet.

---

## Solutions

See [`solutions/SOLUTIONS.md`](solutions/SOLUTIONS.md) for full solution commentary.
