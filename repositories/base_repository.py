from __future__ import annotations

import csv
import dataclasses
import types
import typing
from datetime import datetime
from pathlib import Path
from typing import Generic, Type, TypeVar
from uuid import UUID

from models.base_model import BaseModel

T = TypeVar("T", bound=BaseModel)

DATA_DIR = Path(__file__).parent.parent / "data"


def _serialize_value(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)


def _deserialize_value(value: str, hint: type) -> object:
    if value == "":
        return None

    origin = typing.get_origin(hint)

    # Handle Optional[X] and X | None
    if origin is typing.Union or isinstance(hint, types.UnionType):
        non_none = [a for a in typing.get_args(hint) if a is not type(None)]
        if non_none:
            return _deserialize_value(value, non_none[0])

    if hint is UUID:
        return UUID(value)
    if hint is datetime:
        return datetime.fromisoformat(value)
    if hint is int:
        return int(value)
    if hint is float:
        return float(value)

    return value


class BaseRepository(Generic[T]):
    def __init__(self, model_cls: Type[T], data_dir: Path = DATA_DIR) -> None:
        self._model_cls = model_cls
        self._file = data_dir / f"{model_cls.__name__.lower()}s.csv"
        self._fieldnames = [f.name for f in dataclasses.fields(model_cls)]
        data_dir.mkdir(parents=True, exist_ok=True)
        self._ensure_file()
        self._records: dict[UUID, T] = self._load_from_disk()

    def _ensure_file(self) -> None:
        if not self._file.exists():
            with self._file.open("w", newline="") as f:
                csv.DictWriter(f, fieldnames=self._fieldnames).writeheader()

    def _to_dict(self, obj: T) -> dict[str, str]:
        return {k: _serialize_value(v) for k, v in dataclasses.asdict(obj).items()}

    def _from_dict(self, data: dict[str, str], row_number: int) -> T:
        hints = typing.get_type_hints(self._model_cls)
        missing = [field for field in hints if field not in data]
        if missing:
            raise ValueError(
                f"[{self._model_cls.__name__}] Row {row_number} is missing fields: {missing}"
            )
        return self._model_cls(**{
            key: _deserialize_value(data[key], hint)
            for key, hint in hints.items()
        })

    def _load_from_disk(self) -> dict[UUID, T]:
        with self._file.open(newline="") as f:
            return {
                obj.id: obj
                for row_number, row in enumerate(csv.DictReader(f), start=1)
                if (obj := self._from_dict(row, row_number))
            }

    def _persist(self) -> None:
        records = [self._to_dict(obj) for obj in self._records.values()]
        with self._file.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self._fieldnames)
            writer.writeheader()
            writer.writerows(records)

    def save(self, obj: T) -> None:
        self._records[obj.id] = obj
        self._persist()

    def get_by_id(self, id: UUID) -> T | None:
        return self._records.get(id)

    def get_all(self) -> list[T]:
        return list(self._records.values())

    def get_active(self) -> list[T]:
        return [obj for obj in self._records.values() if not obj.is_archived]
