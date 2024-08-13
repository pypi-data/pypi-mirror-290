from typing import Dict, List, Optional

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from keystone_security.routers import static_files_router
from keystone_security.settings.session_settings import SessionSettings
from keystone_security.settings.session_settings import get_settings as session_get_settings


def add_oidc_router(app: FastAPI) -> None:
    from keystone_security.routers.session_oidc_router import router
    settings = session_get_settings()
    __add_session_middleware(app, settings)
    app.include_router(router, prefix=f"/{settings.auth_router_prefix}", tags=["Authentication"])


def __add_session_middleware(app: FastAPI, settings: SessionSettings) -> None:

    app.add_middleware(
            SessionMiddleware,
            secret_key=settings.secret,
            same_site=settings.same_site,
            session_cookie=settings.session_cookie,
            https_only=settings.https_only,
            max_age=settings.max_age,
            domain=settings.domain
    )


def add_external_router(app: FastAPI) -> None:
    from keystone_security.routers.session_external_router import router
    settings = session_get_settings()

    __add_session_middleware(app, settings)
    app.include_router(router, prefix=f"/{settings.auth_router_prefix}", tags=["Authentication"])


def add_static_files_middleware(
        app: FastAPI,
        auth_router_flags: Optional[Dict[str, bool]] = None,
        required_role: Optional[str] = None,
        open_routes: Optional[List[str]] = None
) -> None:
    from keystone_security.middleware.static_files_middleware import StaticFilesAuthMiddleware
    if auth_router_flags is None:
        auth_router_flags = {
                "oidc": True
        }
    app.add_middleware(
            StaticFilesAuthMiddleware,
            open_routes=open_routes,
            required_role=required_role
    )
    if auth_router_flags.get("external", False):
        add_external_router(app)
    elif auth_router_flags.get("oidc", False):
        add_oidc_router(app)

    app.include_router(static_files_router.router)
