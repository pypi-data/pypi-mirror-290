from typing import Dict, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request, status
from fastapi.security import utils
from httpx import HTTPStatusError
from keystone_msgraph.services import graph_service
from loguru import logger
from starlette.responses import RedirectResponse, StreamingResponse

from keystone_security.dependencies import UserSessionDepends, check_user_session
from keystone_security.models import OIDCLoginForm, OIDCUserPayload, UserSession
from keystone_security.services import oauth_service, oidc_router_helper
from keystone_security.settings import idp_settings

router = APIRouter()


@router.get("/login")
async def login(
    request: Request,
    user_session: UserSessionDepends,
    state: Optional[str] = Query(
        None, description="uri of where to be redirected after login"
    ),
    authorization: Optional[str] = Header(None, name="Authorization"),
):
    if authorization:
        try:
            schema, payload = utils.get_authorization_scheme_param(authorization)
            idp_config = idp_settings.get_settings()
            claims = oauth_service.get_claims(
                client_id=idp_config.client_id,
                id_token=payload,
                access_token=None,
                issuer=idp_config.issuer,
            )
            __update_session_with_claims(request, payload, claims)

            if state is None:
                redirect_uri = "/"
            else:
                redirect_uri = state
            url = redirect_uri
        except Exception as e:
            logger.exception(e)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=str(f"{e}")
            ) from e
    else:
        if user_session.is_logged_in():
            return RedirectResponse(status_code=status.HTTP_303_SEE_OTHER, url="/")
        if state is None:
            redirect_uri = (
                user_session.redirect_path if user_session.redirect_path else "/"
            )
        else:
            redirect_uri = state
        url = oidc_router_helper.get_redirect_for_login(redirect_uri)

    return RedirectResponse(status_code=status.HTTP_303_SEE_OTHER, url=url)


@router.get("/logout")
async def logout(
    request: Request,
    state: Optional[str] = Query(
        None, description="uri of where to be redirected after logout"
    ),
):
    request.session.clear()
    redirect_uri = state if state is not None else "/"
    return RedirectResponse(status_code=status.HTTP_303_SEE_OTHER, url=redirect_uri)


def __update_session_with_claims(
    request: Request,
    token: str,
    claims: Dict,
    user_info: Optional[OIDCUserPayload] = None,
) -> None:
    request.session.update(
        UserSession(
            key=token,
            roles=claims.get("roles", []),
            oidc_user_payload=user_info,
            user_oid=claims.get("oid", claims.get("email", None)),
        ).model_dump()
    )


@router.post("/login")
async def complete_login(request: Request):
    form_data = await request.form()
    payload = OIDCLoginForm.model_validate(form_data)
    response, claims, user_info = oidc_router_helper.handle_form_post_from_idp(payload)

    if claims is not None:
        __update_session_with_claims(request, payload.access_token, claims, user_info)

    return response


@router.get("/me", dependencies=[Depends(check_user_session)])
def read_me(user_session: UserSessionDepends):
    return user_session.oidc_user_payload


@router.get("/me/photo/$value", dependencies=[Depends(check_user_session)])
async def get_photo(user_session: UserSessionDepends):
    access_token = user_session.key
    try:
        image = await graph_service.get_user_photo(access_token)
        return StreamingResponse(image, media_type="image/jpeg")
    except HTTPStatusError as e:
        # If the user gets one of these responses, then that means one of the following:
        #   1. the user's access token from the session has expired
        #   2. the user's access token from the session was from a previous version of the api which didn't request
        #   the proper scopes
        if e.response.status_code in [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        ]:
            logger.error(e)
            raise HTTPException(  # noqa: B904
                status_code=status.HTTP_401_UNAUTHORIZED, detail=e.response.text
            )
