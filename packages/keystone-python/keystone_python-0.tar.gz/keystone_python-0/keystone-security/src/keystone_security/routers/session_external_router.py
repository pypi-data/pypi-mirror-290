from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Form, Query, Request, status
from starlette.responses import RedirectResponse

from keystone_security.dependencies import (
    UserSessionDepends,
    get_login_redirect_if_invalid_session,
)
from keystone_security.models import UserSession
from keystone_security.services import template_service
from keystone_security.settings import external_settings, session_settings

router = APIRouter()


@router.get("/login")
async def login(
    request: Request,
    user_session: UserSessionDepends,
    error_message: Optional[str] = Query(default=None),
):
    if user_session.xsrf_token is None:
        user_session.xsrf_token = UserSession.generate_id()
    if user_session.redirect_path is None:
        user_session.redirect_path = "/"
    request.session.update(user_session.model_dump())

    return template_service.get_templates().TemplateResponse(
        name="login.html",
        context={
            "request": request,
            "xsrf_token": user_session.xsrf_token,
            "error_message": error_message,
            "title": "Login",
            "login_action": f"/{session_settings.get_settings().auth_router_prefix}/login",
        },
    )


@router.get("/logout")
def logout(request: Request):
    request.session.clear()

    return RedirectResponse(
        url=f"/{session_settings.get_settings().auth_router_prefix}/login",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post("/login")
async def login_for_access_token(
    user_session: UserSessionDepends,
    request: Request,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    verifier: Annotated[str, Form()],
):
    xsrf_result = (
        verifier == user_session.xsrf_token and user_session.xsrf_token is not None
    )

    error_message = ""
    if not xsrf_result:
        error_message = "XSRF detected"

    ex_settings = external_settings.get_settings()
    if ex_settings.user.username != username or ex_settings.user.password != password:
        error_message = "Incorrect username or password"

    if error_message:
        settings = session_settings.get_settings()
        return RedirectResponse(
            url=f"/{settings.auth_router_prefix}/login?error_message={error_message}",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    user_session.username = username
    user_session.roles = [ex_settings.user.role]
    user_session.key = user_session.id
    request.session.update(user_session.model_dump())
    return RedirectResponse(
        url=user_session.redirect_path, status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/me")
def read_me(
    user_session: UserSessionDepends,
    redirect_to: Annotated[
        Optional[RedirectResponse], Depends(get_login_redirect_if_invalid_session)
    ],
):
    if redirect_to:
        return redirect_to
    return {"name": user_session.username, "roles": user_session.roles}
