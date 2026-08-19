"""Domain entity models for the User Repository exercise."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class User:
    id: Optional[int]
    email: str
    full_name: str
    is_active: bool = True
