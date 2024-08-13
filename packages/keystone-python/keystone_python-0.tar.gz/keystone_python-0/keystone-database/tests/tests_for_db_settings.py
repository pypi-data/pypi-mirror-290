from typing import Optional

import pytest
from utilities import create_env_file

from keystone_database import db_settings

db_use_tls_settings_data = [
        ("true", True),
        ("false", False),
        ("yes", True),
        ("no", False),
        ("1", True),
        ("0", False),
        (None, False),
]


@pytest.mark.parametrize("use_tls,expected_result", db_use_tls_settings_data)
def test_for_db_use_tls(use_tls: Optional[str], expected_result: bool):
    create_env_file(use_tls=use_tls)

    db_config = db_settings.get_settings()

    assert db_config.connection_options.tls == expected_result
