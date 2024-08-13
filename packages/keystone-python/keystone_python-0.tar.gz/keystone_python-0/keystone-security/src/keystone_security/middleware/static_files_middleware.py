from typing import List, Optional

from fastapi import Request, status
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from keystone_security.dependencies import get_user_session
from keystone_security.settings import session_settings


class StaticFilesAuthMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            open_routes: Optional[List[str]] = None,
            required_role: Optional[str] = None,
            **kwargs
    ):
        settings = session_settings.get_settings()
        self.open_routes = open_routes if open_routes else []
        self.open_routes += [f"/{settings.auth_router_prefix}", f"/{settings.unauthorized_redirect_url}"]
        self.required_role = required_role
        super().__init__(**kwargs)

    def allow_route_through(self, path: str) -> bool:
        if len(self.open_routes) == 0:
            return True

        return any(path.startswith(open_route_pattern) for open_route_pattern in self.open_routes)

    async def dispatch(self, request: Request, call_next):
        if self.allow_route_through(request.url.path):
            return await call_next(request)

        settings = session_settings.get_settings()
        user_session = get_user_session(request)

        if not user_session.is_logged_in():
            user_session.redirect_path = request.url.path
            request.session.update(user_session.model_dump())
            return RedirectResponse(
                    f"/{settings.auth_router_prefix}/login", status_code=status.HTTP_303_SEE_OTHER
            )

        if (
                user_session.roles is not None
                and self.required_role is not None
                and self.required_role not in user_session.roles
        ):
            return RedirectResponse(
                    settings.unauthorized_redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        return await call_next(request)
