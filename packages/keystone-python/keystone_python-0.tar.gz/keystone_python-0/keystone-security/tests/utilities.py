from pathlib import Path
from typing import Optional

from keystone_security.settings import idp_settings, session_settings


def create_env_file(
        provider: Optional[str] = None,
        provider_scheme: Optional[str] = None,
        tenant_id: Optional[str] = None,
        client_host: Optional[str] = "localhost",
        client_id: Optional[str] = None,
        secret: Optional[str] = "fake-secret",
        auth_router_prefix: Optional[str] = "",
) -> None:
    root = Path(f"{Path(__file__).parent}")

    with open(f"{root}/.env", "w") as f:
        if provider:
            f.write(f"IDP_PROVIDER={provider}\n")

        if provider_scheme:
            f.write(f"IDP_PROVIDER_SCHEME={provider_scheme}\n")

        if tenant_id:
            f.write(f"IDP_TENANT_ID={tenant_id}\n")

        if client_id:
            f.write(f"IDP_CLIENT_ID={client_id}\n")

        if client_host is not None:
            f.write(f"SESSION_CLIENT_HOST={client_host}\n")

        if auth_router_prefix is not None:
            f.write(f"SESSION_AUTH_ROUTER_PREFIX={auth_router_prefix}\n")

        if secret is not None:
            f.write(f"SESSION_SECRET={secret}\n")
    idp_settings.init_settings(root)
    session_settings.init_settings(root)
