import base64
import uuid
from typing import Optional, Tuple

from fastapi import status
from fastapi.responses import RedirectResponse, Response
from loguru import logger

from keystone_security.models import OIDCLoginForm, OIDCUserPayload
from keystone_security.services import oauth_service
from keystone_security.settings import idp_settings, session_settings


def get_redirect_for_login(state: str) -> str:
    idp_config = idp_settings.get_settings()
    session_config = session_settings.get_settings()
    authorize_url = oauth_service.get_oidc_discovery_doc(idp_config.issuer).authorization_endpoint
    encoded_state_bytes = state.encode("utf-8")
    encoded_state = base64.b64encode(encoded_state_bytes).decode("utf-8")
    scopes = "openid+profile+email"
    if idp_config.extra_scopes is not None:
        scopes += f"+{idp_config.extra_scopes}"
    params = {
            "client_id": idp_config.client_id,
            "response_type": "id_token%20token",
            "redirect_uri": f"{session_config.client_host}/{session_config.auth_router_prefix}/login",
            "response_mode": "form_post",
            "scope": scopes,
            "state": encoded_state,
            "nonce": str(uuid.uuid4())
    }
    return f"{authorize_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"


def handle_form_post_from_idp(payload: OIDCLoginForm) -> Tuple[Response, Optional[dict], Optional[OIDCUserPayload]]:
    if payload.error is not None:
        logger.error(payload.error)
        logger.error(payload.error_description)

        return Response(status_code=status.HTTP_400_BAD_REQUEST), None, None

    idp_config = idp_settings.get_settings()

    claims = oauth_service.get_claims(
            client_id=idp_config.client_id,
            id_token=payload.id_token,
            access_token=payload.access_token,
            issuer=idp_config.issuer,
    )

    user_info = oauth_service.get_user_info(
            access_token=payload.access_token,
            issuer=idp_config.issuer,
    )

    if payload.state is None:
        redirect_uri = "/"
    else:
        decoded_bytes = base64.b64decode(payload.state)
        redirect_uri = decoded_bytes.decode("utf-8")

    return RedirectResponse(status_code=status.HTTP_303_SEE_OTHER, url=redirect_uri), claims, user_info
