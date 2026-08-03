"""Exercise 17.2 — Ten narrowing puzzles.

For each: predict whether `mypy --strict` accepts it, and whether it can fail at
runtime. Those are two separate questions and both need an answer.

Run:  mypy --strict ex02_narrowing.py
      python ex02_narrowing.py
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, TypeGuard


@dataclass
class User:
    name: str
    email: str | None = None


# q01 -- PREDICTION: mypy? runtime?
def q01(user: User | None) -> str:
    return user.name


# q02 -- PREDICTION:
def q02(user: User | None) -> str:
    if user is None:
        return "anonymous"
    return user.name


# q03 -- PREDICTION: what does `if user:` narrow, and is it the same as is None?
def q03(user: User | None) -> str:
    if user:
        return user.name
    return "anonymous"


# q04 -- PREDICTION: the narrowing is LOST. Where, and why?
def q04(user: User | None, refresh: bool) -> str:
    if user is None:
        return "anonymous"
    if refresh:
        user = lookup(user.name)          # returns User | None
    return user.name


def lookup(name: str) -> User | None:
    return User(name)


# q05 -- PREDICTION: does mypy follow a check inside a HELPER function?
def has_email(user: User) -> bool:
    return user.email is not None


def q05(user: User) -> str:
    if has_email(user):
        return user.email.upper()
    return ""


# q06 -- the fix for q05. PREDICTION: what does TypeGuard change?
def has_email_guard(user: User) -> TypeGuard[User]:
    return user.email is not None


# q07 -- PREDICTION: is `assert` enough for mypy? Is it enough at runtime?
def q07(value: object) -> int:
    assert isinstance(value, int)
    return value + 1


# q08 -- PREDICTION: exhaustiveness. What happens when a Literal gains a member?
Mode = Literal["read", "write"]


def q08(mode: Mode) -> str:
    if mode == "read":
        return "r"
    elif mode == "write":
        return "w"
    else:
        assert_never(mode)          # type: ignore[name-defined]


# q09 -- PREDICTION: does Any propagate through this?
def q09(raw: Any) -> int:
    parsed = raw["count"]           # Any
    doubled = parsed * 2            # still Any
    return doubled                  # returning Any from an int function


# q10 -- PREDICTION: which of these does mypy accept, and which is UNSAFE?
def q10() -> None:
    dogs: list[str] = ["rex"]
    animals: list[object] = dogs        # accepted?
    animals.append(42)                   # and then?
    print(dogs[1].upper())               # ...


# --- questions to answer -------------------------------------------------------
ANSWERS = """
q01  mypy:            runtime:
q02  mypy:            runtime:
q03  What does `if user:` actually narrow? Give a User subclass where `if user:`
     and `if user is not None:` differ. (Hint: Module 09.)
q04  Exactly which line loses the narrowing, and what is the fix that does NOT
     involve an assert?
q05  Why can mypy not follow has_email()?
q06  What does TypeGuard promise, and what happens if you LIE in one?
q07  Two separate questions: does mypy accept it, and what happens under
     python -O? (Module 01.)
q08  Add "append" to Mode. What error appears, and where? Now delete the
     assert_never line and re-check. What changed?
q09  Trace the Any. How many expressions became unchecked?
q10  Does mypy accept it? Should it? What is the general rule this
     demonstrates?
"""

if __name__ == "__main__":
    print(ANSWERS)
