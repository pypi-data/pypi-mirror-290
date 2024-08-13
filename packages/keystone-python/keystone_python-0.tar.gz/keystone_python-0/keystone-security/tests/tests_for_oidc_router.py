# NOTE: This is not an automated test, but a simple api to test different configurations

from typing import Optional

import uvicorn
from fastapi import FastAPI, Query, Request, status
from fastapi.responses import RedirectResponse
from utilities import create_env_file

from keystone_security.models import OIDCLoginForm
from keystone_security.services import oidc_router_helper

# see https://manage.auth0.com/dashboard/us/dev-wlcb7dccdn2hmrgu/insights
use_okta = True

if not use_okta:
    create_env_file(
            client_id="a82ca8e1-c359-4707-bb63-29be82ed2bee",
            client_host="http://localhost:8000",
            auth_router_prefix="oidc",
            tenant_id="b5877d89-99af-40d2-ab0a-1a00dfc7dc8b"
    )

else:
    create_env_file(
            client_id="IemZrqD9W3014UwWrVOpMbWWAIWyiGWi",
            client_host="http://localhost:8000",
            auth_router_prefix="oidc",
            provider="dev-wlcb7dccdn2hmrgu.us.auth0.com"
    )

app = FastAPI()


@app.get("/oidc/login")
async def login(
        state: Optional[str] = Query("/", description="uri of where to be redirected after login"),
):
    url = oidc_router_helper.get_redirect_for_login(state)

    return RedirectResponse(
            status_code=status.HTTP_303_SEE_OTHER, url=url
    )


@app.post("/oidc/login")
async def complete_login(
        request: Request
):
    form_data = await request.form()
    payload = OIDCLoginForm.model_validate(form_data)
    response, claims, user_info = oidc_router_helper.handle_form_post_from_idp(payload)

    if response.status_code == status.HTTP_400_BAD_REQUEST:
        return response

    return claims, user_info


if __name__ == "__main__":
    uvicorn.run("tests_for_oidc_router:app")
