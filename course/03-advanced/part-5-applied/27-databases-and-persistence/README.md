# Module 27 — Databases and Persistence

**Time budget:** 5 hours lesson, 8 hours exercises
**Prerequisite:** Modules 08-11 (OOP, Dataclasses), 16 (Error Handling), 19 (Files & Serialization)

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

Programs hold state in memory; businesses keep state on disk across crashes, restarts, and concurrent requests.

This module teaches you how Python interacts with relational databases and caching stores: DB-API 2.0 specifications, parameterization against SQL injection, transaction boundaries (ACID), isolation levels, the Repository pattern, modern SQLAlchemy 2.0 (Core and ORM), avoiding the N+1 query problem, and schema migrations with Alembic.

---

## 1. DB-API 2.0 and Raw SQL with `sqlite3`

Python's standard library includes `sqlite3`, which adheres to the PEP 249 (DB-API 2.0) interface implemented by drivers for PostgreSQL (`psycopg`), MySQL (`mysqlclient`), and SQLite.

### Parameterized Queries vs SQL Injection

```python
import sqlite3

conn = sqlite3.connect(":memory:")

# DANGER: String interpolation creates SQL injection vulnerabilities!
# conn.execute(f"SELECT * FROM users WHERE name = '{user_input}'")

# SAFE: Always pass parameters as a tuple/list to let the driver handle escaping:
conn.execute("SELECT id, name, balance FROM users WHERE name = ?", (user_input,))
```

### Transaction Semantics: Context Managers

```python
# The connection object as context manager controls transactions:
try:
    with conn:  # BEGIN TRANSACTION
        conn.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
        conn.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
    # COMMIT automatically called here on normal exit
except sqlite3.DatabaseError as err:
    # ROLLBACK automatically called here on unhandled exception
    print(f"Transaction aborted: {err}")
```

---

## 2. The Repository Pattern

Decoupling your business logic from raw SQL makes applications testable without needing a live database connection for every unit test.

```python
from dataclasses import dataclass
from typing import Protocol, Optional, List

@dataclass
class User:
    id: Optional[int]
    email: str
    is_active: bool = True

class UserRepository(Protocol):
    def get_by_id(self, user_id: int) -> Optional[User]: ...
    def save(self, user: User) -> User: ...
    def list_active(self) -> List[User]: ...
```

---

## 3. Modern SQLAlchemy 2.0 ORM

SQLAlchemy 2.0 uses type annotations (`Mapped[...]`) and explicit `select(...)` statements:

```python
from typing import List, Optional
from sqlalchemy import ForeignKey, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

class Base(DeclarativeBase):
    pass

class Department(Base):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    employees: Mapped[List["Employee"]] = relationship(back_populates="department")

class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    department: Mapped[Department] = relationship(back_populates="employees")
```

### The N+1 Query Trap and Eager Loading

```python
from sqlalchemy.orm import selectinload

# ANTI-PATTERN: N+1 queries
# employees = session.scalars(select(Employee)).all()  # 1 query
# for emp in employees:
#     print(emp.department.name)  # Fires 1 extra query PER EMPLOYEE!

# SOLUTION: Eager load relationships with selectinload:
stmt = select(Employee).options(selectinload(Employee.department))
employees = session.scalars(stmt).all()  # Executes exactly 2 efficient queries
```

---

## Exercises

- `exercises/ex01_sqlite_basics.ipynb`: Parameterized queries, schema migrations, and transactions.
- `exercises/ex02_repository/`: Multi-file implementation of the Repository pattern with SQLite backing and unit tests. (Contains `README.md`, `models.py`, `repository.py`, `test_repository.py`).
- `exercises/ex03_sqlalchemy_orm.ipynb`: SQLAlchemy 2.0 mapped schemas, relationships, and queries.

---

## Solutions

See [`solutions/SOLUTIONS.md`](solutions/SOLUTIONS.md) for full solution commentary and design discussion.
