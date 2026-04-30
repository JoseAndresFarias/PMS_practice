from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from uuid import UUID

from .base_model import BaseModel

LeaseStatus = Literal["active", "expired", "terminated"]


@dataclass(kw_only=True)
class Lease(BaseModel):
    unit_id: UUID
    resident_id: UUID
    start_date: datetime
    end_date: datetime
    monthly_rent: float
    status: LeaseStatus = "active"
