from pathlib import Path
from typing import List, Optional, Type
from unittest.mock import patch

import mocks
from beanie import Document

from keystone_database import db_settings
from keystone_database.service import (
    init_connection,
    ConnectionOptions
)


def create_env_file(
        use_tls: Optional[str] = None,
        db_name: Optional[str] = "fake",
) -> None:
    root = Path(f"{Path(__file__).parent}")

    with open(f"{root}/.env", "w") as f:
        if use_tls is not None:
            f.write(f"DB_CONNECTION_OPTIONS__TLS={use_tls}\n")

        f.write(f"DB_NAME={db_name}\n")

    db_settings.init_settings(root)


async def setup_mock_db(entities: List[Type[Document]]):
    with patch("keystone_database.db_settings.get_settings", return_value=mocks.settings_mock):
        await init_connection(ConnectionOptions(document_models=entities))
