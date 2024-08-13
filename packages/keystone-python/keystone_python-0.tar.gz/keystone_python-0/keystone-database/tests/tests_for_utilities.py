from typing import Dict, Optional

import pytest
from beanie import Document
from loguru import logger
from utilities import setup_mock_db

from keystone_database.models import EntityChange
from keystone_database.utilities import NoStateManagementError, track_entity_change

pytest_plugins = ("pytest_asyncio",)

logger.enable("keystone_database")


class Dummy(Document):
    value: str
    value_2: Optional[str] = None
    tracking_id: int

    class Settings:
        use_state_management = True


async def setup_db() -> None:
    await setup_mock_db(
            [
                    EntityChange,
                    Dummy
            ]
    )


def get_mock_user_claims() -> Dict:
    return {
            "name": "fake",
            "oid": "fake"
    }


@pytest.mark.asyncio
async def test_track_entity_change_creates_change_object_with_single_property_change():
    await setup_db()

    dummy = Dummy(value="value", tracking_id=1)
    await dummy.save()

    dummy.value = "new_value"

    await track_entity_change(
            EntityChange, dummy, dummy.tracking_id, get_mock_user_claims(),
            "testing"
    )

    await dummy.save()

    changes = await EntityChange.find().to_list()
    assert len(changes) == 1
    assert len(changes[0].properties) == 1
    assert changes[0].entity_id == dummy.tracking_id
    assert changes[0].properties[0].name == "value"
    assert changes[0].properties[0].old_value is None
    assert changes[0].properties[0].new_value == "new_value"


@pytest.mark.asyncio
async def test_track_entity_change_creates_change_object_with_multiple_property_changes():
    await setup_db()

    dummy = Dummy(value="value", value_2="value_2", tracking_id=1)
    await dummy.save()

    dummy.value = "new_value"
    dummy.value_2 = "new_value2"

    await track_entity_change(
            EntityChange, dummy, dummy.tracking_id, get_mock_user_claims(),
            "testing"
    )

    await dummy.save()

    changes = await EntityChange.find().to_list()
    assert len(changes) == 1
    assert len(changes[0].properties) == 2
    assert changes[0].entity_id == dummy.tracking_id


@pytest.mark.asyncio
async def test_track_entity_change_does_not_create_change_for_new_object():
    await setup_db()

    dummy = Dummy(value="value", tracking_id=1)
    await track_entity_change(
            EntityChange, dummy, dummy.tracking_id, get_mock_user_claims(),
            "testing"
    )

    await dummy.save()

    changes = await EntityChange.find().to_list()
    assert len(changes) == 0


@pytest.mark.asyncio
async def test_track_entity_change_raises_no_state_management_error():
    class TestClass(Document):
        value: Optional[str] = None

    await setup_mock_db(
            [
                    EntityChange,
                    TestClass
            ]
    )

    with pytest.raises(NoStateManagementError):
        await track_entity_change(EntityChange, TestClass(), 1, get_mock_user_claims(), "")
