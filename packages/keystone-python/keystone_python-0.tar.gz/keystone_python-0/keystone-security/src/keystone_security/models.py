import uuid
from typing import List, Optional

from pydantic import BaseModel


class ExternalUser(BaseModel):
    username: str
    password: str
    role: str


class OIDCUserPayload(BaseModel):
    name: str
    family_name: str
    given_name: str
    picture: str
    email: str


class UserSession(BaseModel):
    id: Optional[str] = None
    key: Optional[str] = None
    redirect_path: Optional[str] = None
    user_oid: Optional[str] = None
    username: Optional[str] = None
    roles: Optional[List[str]] = None
    oidc_user_payload: Optional[OIDCUserPayload] = None
    xsrf_token: Optional[str] = None

    def is_logged_in(self) -> bool:
        return self.id is not None and (self.username is not None or self.oidc_user_payload is not None)

    @staticmethod
    def generate_id() -> str:
        return uuid.uuid4().hex


class OIDCDiscoveryDocument(BaseModel):
    issuer: str
    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str
    jwks_uri: str
    scopes_supported: List[str]
    response_types_supported: List[str]
    response_modes_supported: List[str]
    claims_supported: List[str]


class OIDCLoginForm(BaseModel):
    id_token: Optional[str] = None
    access_token: Optional[str] = None
    state: Optional[str] = None
    error: Optional[str] = None
    error_description: Optional[str] = None
