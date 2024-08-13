from utilities import create_env_file

from keystone_security.settings import idp_settings


def test_idp_base_url_is_correct():
    create_env_file(
            provider="testing",
            provider_scheme="http",
            tenant_id=""
    )
    settings = idp_settings.get_settings()

    assert settings.issuer == "http://testing"


def test_entra_id_url():
    create_env_file(tenant_id="test")
    settings = idp_settings.get_settings()

    assert settings.entra_id_issuer == "https://login.microsoftonline.com/test/v2.0"
