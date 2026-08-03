"""Exercise 18.2 — The same service, two test suites.

The point of this exercise is the experiment at the bottom, not the tests
themselves. Run it before reading further.

Run:  pytest ex02_doubles.py -v
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol
from unittest.mock import Mock

import pytest


@dataclass(frozen=True)
class User:
    id: int
    email: str
    created: datetime


class UserRepository(Protocol):
    def save(self, user: User) -> None: ...
    def get(self, uid: int) -> User | None: ...
    def next_id(self) -> int: ...


class Mailer(Protocol):
    def send(self, to: str, subject: str, body: str) -> None: ...


class RegistrationService:
    def __init__(self, repo: UserRepository, mailer: Mailer,
                 now=datetime.now) -> None:  # type: ignore[no-untyped-def]
        self._repo = repo
        self._mailer = mailer
        self._now = now

    def register(self, email: str) -> User:
        if "@" not in email:
            raise ValueError(f"not an email address: {email!r}")
        user = User(id=self._repo.next_id(), email=email, created=self._now())
        self._repo.save(user)
        self._mailer.send(email, "Welcome", f"Hello {email}")
        return user


# TODO 1: the FAKE ------------------------------------------------------------
class InMemoryUserRepo:
    """A working implementation. Implement save, get, next_id."""


class RecordingMailer:
    """A spy: record (to, subject, body) tuples in .sent."""


# TODO 2: suite A, using mocks -------------------------------------------------
class TestWithMocks:
    def test_saves_the_user(self) -> None:
        repo = Mock()
        repo.next_id.return_value = 1
        service = RegistrationService(repo, Mock())
        service.register("ada@example.com")
        repo.save.assert_called_once()

    def test_sends_an_email(self) -> None:
        mailer = Mock()
        repo = Mock()
        repo.next_id.return_value = 1
        RegistrationService(repo, mailer).register("ada@example.com")
        mailer.send.assert_called_once()


# TODO 3: suite B, using fakes -------------------------------------------------
class TestWithFakes:
    def test_saves_the_user(self) -> None:
        """Assert the OUTCOME: the user is retrievable afterwards, with the
        right email and the injected timestamp."""

    def test_sends_an_email(self) -> None:
        """Assert the outcome: an email was recorded, addressed to the right
        person, with the right content."""


# TODO 4: THE EXPERIMENT -------------------------------------------------------
#
# Make each of these four changes to RegistrationService, one at a time, and
# record which suite goes red. Predict before running.
#
#   CHANGE 1 (a pure refactor): rename save() to persist() everywhere,
#            including the Protocol and both doubles.
#   CHANGE 2 (a pure refactor): make register() call repo.save() twice --
#            once before the email and once after, to record the send.
#   CHANGE 3 (A REAL BUG): save a User with the email lowercased and the id
#            hardcoded to 0.
#   CHANGE 4 (A REAL BUG): send the welcome email to a hardcoded address
#            instead of `email`.
#
# Fill in this table:
#
#            | suite A (mocks) | suite B (fakes) | is it a real bug?
#   change 1 |                 |                 |
#   change 2 |                 |                 |
#   change 3 |                 |                 |
#   change 4 |                 |                 |
#
# Then answer:
#   - which suite has FALSE POSITIVES (red on a harmless change)?
#   - which suite has FALSE NEGATIVES (green on a real bug)?
#   - which failure mode costs more, and why?
#   - when IS a mock the right tool? Write a test where suite B cannot express
#     the requirement and a mock can.


# TODO 5: the clock ------------------------------------------------------------
def test_created_timestamp_is_exact() -> None:
    """`now` is injected. Write a test asserting the EXACT timestamp, and note
    that this test cannot become flaky at midnight or across a DST change --
    which a test using the real clock can."""


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
