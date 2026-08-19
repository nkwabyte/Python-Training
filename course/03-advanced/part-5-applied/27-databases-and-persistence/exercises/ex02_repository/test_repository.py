"""Unit tests for the SQLiteUserRepository."""

import sqlite3
import pytest
from models import User
from repository import SQLiteUserRepository


@pytest.fixture
def repo():
    conn = sqlite3.connect(":memory:")
    return SQLiteUserRepository(conn)


def test_add_and_get_user(repo):
    new_user = User(id=None, email="alice@example.com", full_name="Alice Smith")
    saved = repo.add(new_user)
    
    assert saved.id is not None
    assert saved.email == "alice@example.com"
    
    fetched = repo.get_by_id(saved.id)
    assert fetched is not None
    assert fetched.id == saved.id
    assert fetched.email == "alice@example.com"
    assert fetched.full_name == "Alice Smith"
    assert fetched.is_active is True


def test_unique_email_constraint(repo):
    repo.add(User(id=None, email="bob@example.com", full_name="Bob Jones"))
    with pytest.raises(sqlite3.IntegrityError):
        repo.add(User(id=None, email="bob@example.com", full_name="Bob Duplicate"))


def test_list_active_users(repo):
    repo.add(User(id=None, email="u1@example.com", full_name="User 1", is_active=True))
    repo.add(User(id=None, email="u2@example.com", full_name="User 2", is_active=False))
    repo.add(User(id=None, email="u3@example.com", full_name="User 3", is_active=True))
    
    active_users = repo.list_active()
    assert len(active_users) == 2
    emails = {u.email for u in active_users}
    assert emails == {"u1@example.com", "u3@example.com"}
