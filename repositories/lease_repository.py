from __future__ import annotations

from models.lease import Lease
from .base_repository import BaseRepository


class LeaseRepository(BaseRepository[Lease]):
    def __init__(self) -> None:
        super().__init__(Lease)
