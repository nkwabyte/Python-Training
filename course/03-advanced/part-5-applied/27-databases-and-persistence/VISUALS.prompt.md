# Visual Companion Prompt — Module 27: Databases and Persistence

## Video Steering Prompt
> Create an architectural animation contrasting direct database coupling against the Repository Pattern and ORM layer in Python. Illustrate SQL injection vulnerabilities via string concatenation alongside driver-level parameterized query compilation. Visualize ACID transaction boundaries showing WAL (Write-Ahead Logging) and atomic rollback. Diagram the classic N+1 query problem with SQL query timeline waterfalls, contrasting naive lazy loading against batched JOINs and `selectinload` eager loading in SQLAlchemy 2.0.

## Key Concepts
- Parameterized Queries vs String Formatting (SQL Injection protection)
- DB-API 2.0 connection & cursor lifecycles
- ACID transactions: `BEGIN`, `COMMIT`, `ROLLBACK`
- Repository Pattern and abstraction of persistence
- SQLAlchemy 2.0 Declarative Mapping with `Mapped[...]`
- Eager Loading (`joinedload`, `selectinload`) to eliminate N+1 queries
- Schema migrations with Alembic
