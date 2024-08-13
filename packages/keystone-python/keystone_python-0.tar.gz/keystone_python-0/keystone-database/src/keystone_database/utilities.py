from typing import Any, Dict, List, Optional, Type, TypeVar

import jsondiff
from beanie import Document
from beanie.odm.operators.find.array import ElemMatch
from pydantic import BaseModel

from keystone_database.models import EntityChange, PropertyChange


# TODO: create tests for this method
def get_changes(
        old_model: BaseModel, current_model: BaseModel, exclude_keys: Optional[List[str]] = None
) -> List[PropertyChange]:
    if exclude_keys is None:
        exclude_keys = ["comment"]
    diff = jsondiff.diff(old_model.dict(), current_model.dict())

    def get_prop_changes(diff_dict: Dict[str, Any]) -> List[PropertyChange]:
        property_changes = []
        if len(diff_dict.keys()) == 0:
            return []
        for k, v in diff_dict.items():
            if isinstance(v, dict):
                changes = get_prop_changes(v)
                property_changes = property_changes + changes
            else:
                if k in exclude_keys or isinstance(k, jsondiff.symbols.Symbol):
                    continue
                old_value = existing_obj.get(k)
                if old_value is None and v is None:
                    continue
                prop_change = PropertyChange(name=k, old_value=existing_obj.get(k), new_value=v)
                property_changes.append(prop_change)

        return property_changes

    if len(diff.keys()) > 0:
        existing_obj = old_model.dict()

        return get_prop_changes(diff)


T = TypeVar("T", Document, EntityChange)
K = TypeVar("K", bound=Document)


class NoStateManagementError(Exception):
    def __init__(self, entity_class: Type[K]) -> None:
        self.message = f"Must set {entity_class.__name__} Settings.use_state_management = True"
        super().__init__(self.message)


async def track_entity_change(cls: Type[T], entity: K, entity_id: int, user_claims: Dict, comment: str) -> T | None:
    if not entity.use_state_management():
        raise NoStateManagementError(type(entity))
    if entity.get_saved_state() is None or not entity.is_changed:
        return None

    changes: dict = entity.get_changes()
    property_changes = []
    for key, value in changes.items():
        old_change = (
                await cls.find(
                        cls.entity == entity.get_collection_name(),
                        cls.entity_id == entity_id,
                        ElemMatch(
                                cls.properties, {
                                        "name": key
                                }
                        ),
                )
                .sort(-cls.modified_date)
                .first_or_none()
        )
        if old_change is not None:
            old_value = next(p for p in old_change.properties if p.name == key).new_value
        else:
            old_value = None
        property_changes.append(PropertyChange(name=key, old_value=old_value, new_value=value))

    change = cls(
            entity_id=entity_id,
            properties=property_changes,
            modified_by=user_claims.get("name"),
            modified_by_id=user_claims.get("oid", user_claims.get("id")),
            comment=comment,
            entity=entity.get_collection_name(),
    )
    await change.save()

    return change


def get_string_contains_filter(property_name: str, search: str) -> Dict[str, Dict[str, Any]]:
    return {
            property_name: {
                    "$regex": search,
                    "$options": "i"
            }
    }
