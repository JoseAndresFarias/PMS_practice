from __future__ import annotations

from models.resident import Resident
from .base_repository import BaseRepository


class ResidentRepository(BaseRepository[Resident]):
    def __init__(self) -> None:
        super().__init__(Resident)
