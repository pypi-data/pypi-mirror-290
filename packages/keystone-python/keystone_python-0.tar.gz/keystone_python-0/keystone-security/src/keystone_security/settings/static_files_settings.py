from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class StaticFilesSettings(BaseSettings):
    dir: str

    model_config = SettingsConfigDict(case_sensitive=False, extra="ignore", env_prefix="static_files_")


class Context:
    settings: Optional[StaticFilesSettings] = None


__ctx = Context()


def init_settings(root: Path) -> None:
    __ctx.settings = StaticFilesSettings(_env_file=root / ".env")


def get_settings() -> StaticFilesSettings:
    if __ctx.settings is None:
        msg = "Settings are not initialized -- call init_settings()"
        raise Exception(msg)
    return __ctx.settings
