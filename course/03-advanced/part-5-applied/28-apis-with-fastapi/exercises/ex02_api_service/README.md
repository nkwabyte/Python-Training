# Exercise 28.2 — Building and Testing a FastAPI Service

**Directory:** `ex02_api_service/`
**Files:** `models.py`, `main.py`, `test_api.py`
**Estimated Time:** 45 minutes

---

## Background & Objective

FastAPI uses Pydantic models for request validation, documentation, and response serialization. In this exercise, you will explore a production-patterned Task Management API with CRUD routes, path parameters, optional query filtering, PATCH partial updates, and status codes.

---

## File Overview

- `models.py`: Defines request models (`TaskCreate`, `TaskUpdate`) and the response model (`TaskResponse`).
- `main.py`: Declares FastAPI application routes (`POST /tasks`, `GET /tasks`, `GET /tasks/{id}`, `PATCH /tasks/{id}`, `DELETE /tasks/{id}`).
- `test_api.py`: Pytest suite using `fastapi.testclient.TestClient` to verify status codes, payload validations, partial updates, and 404 handling.

---

## Running the Tests

Execute pytest in this directory:
```bash
pytest test_api.py
```
Observe how invalid payloads automatically return `422 Unprocessable Entity` with detailed field-level error diagnostics without manual validation logic.
