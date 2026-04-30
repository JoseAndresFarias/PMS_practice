from __future__ import annotations

from dataclasses import dataclass

from .base_model import BaseModel


@dataclass(kw_only=True)
class Building(BaseModel):
    name: str
    address: str
    city: str
    state: str
    zip_code: str
