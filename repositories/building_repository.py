from __future__ import annotations

from models.building import Building
from .base_repository import BaseRepository


class BuildingRepository(BaseRepository[Building]):
    def __init__(self) -> None:
        super().__init__(Building)
