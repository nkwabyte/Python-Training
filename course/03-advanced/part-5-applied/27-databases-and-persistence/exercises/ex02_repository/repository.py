"""Repository implementation using SQLite DB-API 2.0 with parameterized queries."""

from __future__ import annotations

import sqlite3
from typing import List, Optional
from models import User


class SQLiteUserRepository:
    """Repository managing User persistence in an SQLite database."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.conn = connection
        self._init_schema()

    def _init_schema(self) -> None:
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL UNIQUE,
                    full_name TEXT NOT NULL,
                    is_active INTEGER NOT NULL DEFAULT 1
                )
            """)

    def add(self, user: User) -> User:
        """Insert a new user and return the user instance with populated ID."""
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO users (email, full_name, is_active) VALUES (?, ?, ?)",
                (user.email, user.full_name, 1 if user.is_active else 0)
            )
            return User(
                id=cursor.lastrowid,
                email=user.email,
                full_name=user.full_name,
                is_active=user.is_active
            )

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Fetch user by primary key ID."""
        cursor = self.conn.execute(
            "SELECT id, email, full_name, is_active FROM users WHERE id = ?",
            (user_id,)
        )
        row = cursor.fetchone()
        if not row:
            return None
        return User(id=row[0], email=row[1], full_name=row[2], is_active=bool(row[3]))

    def get_by_email(self, email: str) -> Optional[User]:
        """Fetch user by unique email."""
        cursor = self.conn.execute(
            "SELECT id, email, full_name, is_active FROM users WHERE email = ?",
            (email,)
        )
        row = cursor.fetchone()
        if not row:
            return None
        return User(id=row[0], email=row[1], full_name=row[2], is_active=bool(row[3]))

    def list_active(self) -> List[User]:
        """Return all active users."""
        cursor = self.conn.execute(
            "SELECT id, email, full_name, is_active FROM users WHERE is_active = 1 ORDER BY id"
        )
        return [
            User(id=row[0], email=row[1], full_name=row[2], is_active=bool(row[3]))
            for row in cursor.fetchall()
        ]
