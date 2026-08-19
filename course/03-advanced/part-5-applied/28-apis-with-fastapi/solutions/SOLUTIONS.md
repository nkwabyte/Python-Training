# Solutions & Commentary — Module 28: Building APIs with FastAPI

## Overview of Exercises

This module drilled ASGI architecture, Pydantic v2 schemas, REST CRUD design, status codes, and test automation with `TestClient`.

---

## Exercise 28.1: Request Validation & Endpoints

### Key Takeaways
- Pydantic v2 validates requests before route handler functions are invoked. Invalid types or missing fields immediately generate RFC-compliant 422 error envelopes.
- `response_model` ensures sensitive or internal fields (like password hashes or internal foreign keys) are never inadvertently serialized to API consumers.

---

## Exercise 28.2: Task Service & TestClient

### Key Takeaways
- `PATCH` endpoints use `exclude_unset=True` when dumping partial update models so omitted fields are not overwritten with `None`.
- `TestClient` uses `httpx` under the hood to invoke ASGI applications directly in-memory, providing fast, deterministic testing without port binding or network latency.
