from datetime import datetime
from typing import Any, List, Optional

from beanie import Document
from pydantic import BaseModel
from pydantic.fields import Field


class PropertyChange(BaseModel):
    name: str
    old_value: Any
    new_value: Any


class Change(BaseModel):
    modified_by: str
    modified_by_id: str
    modified_date: datetime = Field(default_factory=datetime.utcnow)
    comment: Optional[str] = None
    properties: List[PropertyChange]


class EntityChange(Change, Document):
    entity_id: int
    entity: str

    class Settings:
        indexes = [
                "entity_id",
                "modified_date"
        ]


class DbConnectionOptions(BaseModel):
    tls: bool = False
