from __future__ import annotations

from dataclasses import dataclass
from typing import Literal
from uuid import UUID

from .base_model import BaseModel

UnitStatus = Literal["vacant", "occupied", "maintenance"]


@dataclass(kw_only=True)
class Unit(BaseModel):
    building_id: UUID
    unit_number: str
    bedrooms: int
    bathrooms: float
    rent_amount: float
    status: UnitStatus = "vacant"
