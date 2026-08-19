# Module 28 — Building APIs with FastAPI

**Time budget:** 5 hours lesson, 9 hours exercises
**Prerequisite:** Modules 17 (Typing), 22 (Asyncio), 26 (HTTP), 27 (Databases)

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

Python web APIs have evolved from WSGI (Flask/Django) to ASGI (FastAPI/Starlette).
FastAPI has become the standard framework for production Python services because it combines:
1. **Type-driven validation** via Pydantic v2.
2. **Asynchronous performance** on ASGI event loops.
3. **Dependency injection** for testable, modular resource lifecycles.
4. **Auto-generated OpenAPI / Swagger documentation**.

This module teaches you how to structure, build, authenticate, and test production-ready APIs with FastAPI.

---

## 1. ASGI vs WSGI Architecture

```
WSGI (Synchronous, Thread-per-request):
[Client] -> [Nginx] -> [Gunicorn (Sync Worker)] -> [Python Thread blocked on I/O]

ASGI (Asynchronous, Event-Loop multiplexing):
[Client] -> [Nginx] -> [Uvicorn (Async Event Loop)] -> [Task awaiting async DB/HTTP]
```

---

## 2. Pydantic v2 Data Contracts

In FastAPI, function signatures *are* the validation schemas and documentation:

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

app = FastAPI(title="User API", version="1.0.0")

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=30)
    full_name: Optional[str] = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool

@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate) -> UserOut:
    # payload is already validated here: email syntax checked, lengths verified
    return UserOut(id=1, email=payload.email, username=payload.username, is_active=True)
```

---

## 3. Dependency Injection with `Depends`

FastAPI's dependency injection system manages database sessions, authentication, and configuration cleanly:

```python
from fastapi import Depends, Header, HTTPException

async def verify_api_key(x_api_key: str = Header(...)) -> str:
    if x_api_key != "secret-production-key":
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

@app.get("/protected-data")
async def get_protected_data(api_key: str = Depends(verify_api_key)):
    return {"message": "Access granted to secure dataset"}
```

---

## 4. Testing FastAPI Services with `TestClient`

FastAPI provides a synchronous `TestClient` (wrapping `httpx`) that requires no running server:

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_create_user():
    response = client.post("/users", json={"email": "alice@example.com", "username": "alice99"})
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "alice@example.com"
    assert data["id"] == 1
```

---

## Exercises

- `exercises/ex01_endpoints.ipynb`: Pydantic request models, query parameters, status codes, and error handlers.
- `exercises/ex02_api_service/`: Multi-module FastAPI service with database dependency injection, authentication middleware, and pytest suite. (Contains `README.md`, `models.py`, `main.py`, `test_api.py`).

---

## Solutions

See [`solutions/SOLUTIONS.md`](solutions/SOLUTIONS.md) for full solution architecture and discussion.
