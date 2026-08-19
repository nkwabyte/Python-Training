# Solutions & Commentary — Module 27: Databases and Persistence

## Overview of Exercises

This module drilled parameterized SQL execution, atomic transaction boundaries, Repository abstraction, and modern SQLAlchemy 2.0 ORM schemas.

---

## Exercise 27.1: SQLite Fundamentals & Transactions

### Key Takeaways
- Using `with conn:` guarantees that if any exception occurs during multi-statement operations (such as transferring balances or deducting inventory), the entire transaction is rolled back cleanly.
- Parameterized placeholders (`?` for SQLite, `%s` or `%(name)s` for PostgreSQL) ensure query plans are cached and prevent SQL injection.

---

## Exercise 27.2: Repository Pattern

### Key Takeaways
- The `SQLiteUserRepository` keeps all SQL statements localized to data access layer code.
- Higher level services can be unit-tested against an in-memory repository mock without requiring database setup/teardown overhead.

---

## Exercise 27.3: SQLAlchemy 2.0 ORM

### Key Takeaways
- Modern SQLAlchemy 2.0 uses `Mapped[T]` and `mapped_column()` with typing integration for static type checkers (`mypy`, `pyright`).
- Relationship queries should always specify eager loading strategies (`selectinload` for 1-to-many, `joinedload` for 1-to-1) to avoid firing N additional database queries in loops.
