# Visual Companion Prompt — Module 28: Building APIs with FastAPI

## Video Steering Prompt
> Create a technical diagram and animation of FastAPI's request lifecycle within the ASGI architecture. Illustrate how an incoming HTTP request arrives at Uvicorn, passes through middleware layers, executes dependency injection resolvers (`Depends`), parses and validates payload data via Pydantic v2 rust-core schemas, dispatches to the async route handler, and serializes the outgoing response model.

## Key Concepts
- ASGI Event Loop architecture vs WSGI Thread Pools
- Pydantic v2 Data Validation pipelines & JSON schema extraction
- FastAPI Route Decorators (`@app.get`, `@app.post`)
- Dependency Injection (`Depends`) for Database Sessions & Auth
- Exception Handlers (`HTTPException`) and uniform RFC 7807 error envelopes
- In-memory integration testing using `TestClient`
