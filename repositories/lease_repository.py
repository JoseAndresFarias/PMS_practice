from __future__ import annotations

from models.lease import Lease
from .base_repository import BaseRepository


class LeaseRepository(BaseRepository[Lease]):
    def __init__(self) -> None:
        super().__init__(Lease)

    def get_active(self) -> list[T]:
        non_archived_leases = super().get_active()
        return [lease for lease in non_archived_leases if lease.status == "active"]

    def get_by_unit_id(self, unit_id: UUID) -> list[Lease]:
        return [lease for lease in self.get_active() if lease.unit_id == unit_id]