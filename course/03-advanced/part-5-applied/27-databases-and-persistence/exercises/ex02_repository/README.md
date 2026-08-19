# Exercise 27.2 — Implementing the Repository Pattern with SQLite

**Directory:** `ex02_repository/`
**Files:** `models.py`, `repository.py`, `test_repository.py`
**Estimated Time:** 45 minutes

---

## Background & Objective

The Repository pattern creates an abstraction layer between domain models and data mapping code. Instead of executing ad-hoc SQL strings across business controllers or service modules, callers interact with a clean domain interface (`add`, `get_by_id`, `list_active`).

In this exercise, you will explore and test the `SQLiteUserRepository` implementation.

---

## Structure

- `models.py`: Defines the immutable domain entity `User(id, email, full_name, is_active)`.
- `repository.py`: Implements CRUD operations against SQLite using parameterized SQL queries and context managers.
- `test_repository.py`: Pytest suite verifying persistence, retrieval, constraints, and filtering.

---

## Running the Tests

Execute pytest directly in this directory:
```bash
pytest test_repository.py
```
Ensure all tests pass and investigate how transaction rollbacks behave when integrity constraints fail.
