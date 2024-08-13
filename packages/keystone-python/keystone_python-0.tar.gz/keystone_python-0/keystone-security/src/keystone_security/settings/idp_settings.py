from pathlib import Path
from typing import Dict, Optional

from fastapi_azure_auth import MultiTenantAzureAuthorizationCodeBearer, SingleTenantAzureAuthorizationCodeBearer
from fastapi_azure_auth.exceptions import InvalidAuth
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class IdpSettings(BaseSettings):
    client_id: str = ""
    client_secret: str = ""
    provider: str = "login.microsoftonline.com"
    provider_scheme: str = "https"
    tenant_id: str = ""
    token_expiration_minutes: int = 60
    extra_scopes: Optional[str] = None

    model_config = SettingsConfigDict(case_sensitive=False, extra="ignore", env_prefix="idp_")

    @computed_field
    def issuer_base(self) -> str:
        return f"{self.provider_scheme}://{self.provider}"

    @computed_field
    def use_entra_id_issuer(self) -> bool:
        return self.provider == "login.microsoftonline.com"

    @computed_field
    def issuer(self) -> str:
        return self.issuer_base if not self.use_entra_id_issuer else self.entra_id_issuer

    @computed_field
    def entra_id_issuer(self) -> str:
        return f"{self.issuer_base}/{self.tenant_id}/v2.0"


class Context:
    settings: Optional[IdpSettings] = None


__ctx = Context()


def init_settings(root: Path):
    __ctx.settings = IdpSettings(_env_file=root / ".env")


def get_settings() -> IdpSettings:
    if __ctx.settings is None:
        msg = "Settings are not initialized -- call init_settings()"
        raise Exception(msg)
    return __ctx.settings


def get_azure_scheme(settings: IdpSettings) -> SingleTenantAzureAuthorizationCodeBearer:
    return SingleTenantAzureAuthorizationCodeBearer(
            app_client_id=settings.client_id,
            scopes={
                    f"api://{settings.client_id}/access_as_user": "**No client secret needed, leave blank**"
            },
            tenant_id=settings.tenant_id,
            allow_guest_users=True,
    )


def get_azure_scheme_multi_tenant(
        settings: IdpSettings, tid_to_iss_mapping: Dict[str, str]
) -> MultiTenantAzureAuthorizationCodeBearer:
    async def check_if_valid_tenant(tid: str) -> str:
        try:
            return tid_to_iss_mapping[tid]
        except KeyError:
            raise InvalidAuth("Tenant not allowed")

    return MultiTenantAzureAuthorizationCodeBearer(
            app_client_id=settings.client_id,
            scopes={
                    f"api://{settings.client_id}/access_as_user": "**No client secret needed, leave blank**"
            },
            allow_guest_users=False,
            validate_iss=True,
            iss_callable=check_if_valid_tenant
    )
