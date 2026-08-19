# Exercise 30.2 — Writing a Production Multi-Stage Dockerfile

**Estimated Time:** 35 minutes

---

## Objective

Author a production Dockerfile for a FastAPI / Python application that meets five strict production criteria:
1. **Multi-stage build:** Separates compilation/build dependencies from runtime.
2. **Minimal attack surface:** Uses a slim base image (`python:3.12-slim`).
3. **Non-root execution:** Runs as a dedicated non-root user (`appuser` with UID 10001).
4. **Clean environment variables:** `PYTHONUNBUFFERED=1` and `PYTHONDONTWRITEBYTECODE=1`.
5. **Layer caching:** Copies dependency specifications (`pyproject.toml`) before copying full application source code.

---

## Worksheet Tasks

### Task 1: Complete the Multi-Stage Dockerfile Template

Fill in the blanks below to create a production Dockerfile:

```dockerfile
# Stage 1: Build virtual environment
FROM python:3.12-slim AS builder

WORKDIR /app
RUN pip install --no-cache-dir uv

# Copy dependency definition only for optimal caching
COPY pyproject.toml .
RUN uv venv /opt/venv && \
    uv pip install --python /opt/venv/bin/python .

# Stage 2: Minimal runtime image
FROM python:3.12-slim AS runtime

# Create dedicated non-root user
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/false appuser

WORKDIR /app

# Copy built virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application source code
COPY src/ /app/src/

# Set production environment variables
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER appuser

EXPOSE 8000

# Use exec form to allow SIGTERM signal forwarding
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Self-Check Questions

1. Why is `uvicorn src.main:app` in shell form (`CMD uvicorn ...`) problematic compared to JSON list exec form (`CMD ["uvicorn", ...]`)?
   - *Answer:* Shell form starts `/bin/sh` as PID 1, which does not forward `SIGTERM` signals to Uvicorn, preventing graceful shutdown on container termination.
2. Why is running containers as `root` a critical security vulnerability?
   - *Answer:* If an attacker exploits a remote code execution vulnerability in a root container, they gain root privileges over container namespaces and potentially the host kernel.
