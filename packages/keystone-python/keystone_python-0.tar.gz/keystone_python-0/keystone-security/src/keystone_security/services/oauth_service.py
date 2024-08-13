from typing import Any, Dict, Optional

import httpx
from jose import JWSError, jwt
from loguru import logger

from keystone_security.models import OIDCDiscoveryDocument, OIDCUserPayload


def get_oidc_discovery_doc(issuer: str) -> OIDCDiscoveryDocument:
    url = f"{issuer}/.well-known/openid-configuration"
    response = httpx.get(url)
    response.raise_for_status()

    return OIDCDiscoveryDocument.model_validate(response.json())


def get_jwks(jwks_uri: str) -> dict:
    response = httpx.get(url=jwks_uri)

    return response.json()


def get_user_info(
        access_token: str,
        issuer: str
) -> OIDCUserPayload:
    discovery_doc = get_oidc_discovery_doc(issuer)
    user_info_endpoint = discovery_doc.userinfo_endpoint
    user_info_response: httpx.Response = httpx.get(
            f"{user_info_endpoint}",
            headers={
                    "Authorization": f"Bearer {access_token}"
            },
    )

    user_info_response.raise_for_status()
    user_info = OIDCUserPayload.model_validate(user_info_response.json())
    return user_info


def get_claims(
        client_id: str,
        id_token: str,
        issuer: str,
        access_token: Optional[str] = None,
        jwt_options: Optional[Dict[str, Any]] = None,
) -> dict:
    if jwt_options is None:
        jwt_options = {
                "verify_aud": True,
                "verify_signature": True
        }
    discovery_doc = get_oidc_discovery_doc(issuer)
    jwks = get_jwks(discovery_doc.jwks_uri)
    try:
        claims = jwt.decode(
                id_token,
                jwks,
                algorithms="RS256",
                audience=client_id,
                access_token=access_token,
                options=jwt_options,
        )
        return claims
    except JWSError as e:
        logger.error(e)
        raise e
