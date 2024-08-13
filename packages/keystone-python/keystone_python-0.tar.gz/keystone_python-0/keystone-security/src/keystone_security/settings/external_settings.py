from pathlib import Path
from typing import Optional

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)

from keystone_security.models import ExternalUser


class ExternalSettings(BaseSettings):
    http_secure: bool = True
    user: Optional[ExternalUser] = None

    model_config = SettingsConfigDict(
            case_sensitive=False, extra="ignore", env_prefix="external_", env_nested_delimiter="__"
    )


class Context:
    settings: Optional[ExternalSettings] = None


__ctx = Context()


def init_settings(root: Path):
    __ctx.settings = ExternalSettings(_env_file=root / ".env")


def get_settings() -> ExternalSettings:
    if __ctx.settings is None:
        msg = "Settings are not initialized -- call init_settings()"
        raise Exception(msg)
    return __ctx.settings


if __name__ == "__main__":
    __root_path = Path(__file__).parent

    init_settings(__root_path)
    settings = get_settings()
    print(settings.user)
