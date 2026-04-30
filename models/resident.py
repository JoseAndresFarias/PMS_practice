from __future__ import annotations

from dataclasses import dataclass

from .base_model import BaseModel


@dataclass(kw_only=True)
class Resident(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
