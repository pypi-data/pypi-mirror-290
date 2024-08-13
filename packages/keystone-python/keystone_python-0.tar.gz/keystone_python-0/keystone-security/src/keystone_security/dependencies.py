from typing import Annotated, Optional, Type

from fastapi import (
    Depends,
    HTTPException,
    Request,
    status,
)
from fastapi.responses import RedirectResponse
from fastapi_azure_auth.auth import AzureAuthorizationCodeBearerBase
from fastapi_azure_auth.user import User
from loguru import logger

from keystone_security.exceptions import Forbid
from keystone_security.models import UserSession
from keystone_security.settings import session_settings


def get_user_session(request: Request) -> UserSession:
    try:
        session = UserSession(**request.session)
        if session.id is None:
            session.id = UserSession.generate_id()
        request.session.update(**session.model_dump())
        return session
    except Exception as e:
        logger.warning(f"{e}")
        return UserSession()


UserSessionDepends = Annotated[UserSession, Depends(get_user_session)]


def is_user_logged_in(session: UserSessionDepends) -> bool:
    return session.is_logged_in()


UserLoggedInDepends = Annotated[bool, Depends(is_user_logged_in)]


def get_login_redirect_if_invalid_session(
    logged_in: UserLoggedInDepends,
) -> Optional[RedirectResponse]:
    settings = session_settings.get_settings()
    if not settings.ignore_challenge and not logged_in:
        return RedirectResponse(
            f"/{settings.auth_router_prefix}/login",
            status_code=status.HTTP_303_SEE_OTHER,
        )


def check_user_session(
    redirect_to: Annotated[Optional[RedirectResponse], Depends(get_login_redirect_if_invalid_session)],
) -> None:
    if redirect_to:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Login at {redirect_to.headers['location']}",
        )


def ensure_user_has_role(role: str, user: User) -> None:
    if role not in user.roles:
        msg = f"User does not have {role} Role"
        raise Forbid(msg)


def create_user_type_dependency(
    code_bearer: AzureAuthorizationCodeBearerBase,
) -> Type[User]:
    return Annotated[User, Depends(code_bearer)]
