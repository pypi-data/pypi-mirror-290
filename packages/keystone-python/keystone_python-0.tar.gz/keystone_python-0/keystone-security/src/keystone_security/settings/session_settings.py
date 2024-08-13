from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class SessionSettings(BaseSettings):
    client_host: str
    max_age: int = 60 * 60 * 24  # 1 day
    https_only: bool = True
    session_cookie: str = "pj_session"
    same_site: str = "Lax"
    domain: Optional[str] = None
    secret: str
    auth_router_prefix: str
    ignore_challenge: bool = False
    unauthorized_redirect_url: Optional[str] = "unauthorized"

    model_config = SettingsConfigDict(case_sensitive=False, extra="ignore", env_prefix="session_")


class Context:
    settings: Optional[SessionSettings] = None


__ctx = Context()


def init_settings(root: Path) -> None:
    __ctx.settings = SessionSettings(_env_file=root / ".env")


def get_settings() -> SessionSettings:
    if __ctx.settings is None:
        msg = "Settings are not initialized -- call init_settings()"
        raise Exception(msg)
    return __ctx.settings
