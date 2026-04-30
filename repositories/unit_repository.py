from __future__ import annotations

from models.unit import Unit
from .base_repository import BaseRepository


class UnitRepository(BaseRepository[Unit]):
    def __init__(self) -> None:
        super().__init__(Unit)
