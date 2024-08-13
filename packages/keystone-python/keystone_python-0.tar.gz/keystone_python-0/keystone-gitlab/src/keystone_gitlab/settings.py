from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class GitlabSettings(BaseSettings):
    token: str
    url: str = "https://gitlab.purplejay.net"
    project_id: str

    model_config = SettingsConfigDict(case_sensitive=False, extra="ignore", env_prefix="gl_")


class Context:
    settings: Optional[GitlabSettings] = None


__ctx = Context()


def init_settings(root: Path) -> None:
    __ctx.settings = GitlabSettings(_env_file=root / ".env")


def get_settings() -> GitlabSettings:
    if __ctx.settings is None:
        msg = "Settings are not initialized -- call init_settings()"
        raise Exception(msg)
    return __ctx.settings
