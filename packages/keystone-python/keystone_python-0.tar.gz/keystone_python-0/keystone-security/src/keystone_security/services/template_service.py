from pathlib import Path
from typing import Any, Optional

from fastapi import Request
from fastapi.templating import Jinja2Templates

from keystone_security.settings import external_settings


class Context:
    templates: Optional[Jinja2Templates] = None


__ctx = Context()


def init(templates_directory: str | Path) -> None:
    __ctx.templates = Jinja2Templates(directory=templates_directory)
    __ctx.templates.env.globals["https_url_for"] = https_url_for


def https_url_for(request: Request, name: str, **path_params: Any) -> str:
    settings = external_settings.get_settings()
    http_url = f"{request.url_for(name, **path_params)}"
    if settings.http_secure:
        return http_url.replace("http", "https", 1)

    return http_url


def get_templates() -> Jinja2Templates:
    if __ctx.templates is None:
        msg = "Templates were not initialized"
        raise RuntimeError(msg)
    return __ctx.templates
