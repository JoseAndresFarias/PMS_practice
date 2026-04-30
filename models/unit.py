from __future__ import annotations

from dataclasses import dataclass
from typing import Literal
from uuid import UUID

from .base_model import BaseModel
from repositories.lease_repository import LeaseRepository
UnitStatus = Literal["vacant", "occupied", "maintenance"]


@dataclass(kw_only=True)
class Unit(BaseModel):
    building_id: UUID
    unit_number: str
    bedrooms: int
    bathrooms: float
    rent_amount: float
    status: UnitStatus = "vacant"

def archive(self) -> None:
    if self.status == "occupied":
        lease = LeaseRepository().get_by_unit_id(self.id)
        if lease:
            lease.archive()
    super().archive()