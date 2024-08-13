from utilities import create_env_file

from keystone_security.services import oauth_service
from keystone_security.settings import idp_settings


def test_oidc_discovery_doc_for_entra_id():
    create_env_file(tenant_id="b5877d89-99af-40d2-ab0a-1a00dfc7dc8b")
    settings = idp_settings.get_settings()
    doc = oauth_service.get_oidc_discovery_doc(settings.entra_id_issuer)

    assert doc is not None


def test_oidc_discovery_doc_for_gitlab():
    create_env_file(provider="gitlab.purplejay.net")
    settings = idp_settings.get_settings()
    doc = oauth_service.get_oidc_discovery_doc(settings.issuer)

    assert doc.issuer == settings.issuer
