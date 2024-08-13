from io import BytesIO

import httpx
from loguru import logger

from keystone_msgraph.models import UserProfile

graph_base_url = "https://graph.microsoft.com/v1.0"


async def get_graph_access_token(client_id: str, client_secret: str, tenant_id: str, assertion: str) -> str:
    async with httpx.AsyncClient() as client:
        # Use the users access token and fetch a new access token for the Graph API
        obo_response: httpx.Response = await client.post(
                f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
                data={
                        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                        "client_id": client_id,
                        "client_secret": client_secret,
                        "assertion": assertion,
                        "scope": "https://graph.microsoft.com/user.read",
                        "requested_token_use": "on_behalf_of",
                },
        )

        if obo_response.is_success:
            return obo_response.json()["access_token"]
        else:
            logger.error(obo_response.json()["error_description"])
            msg = "failed to get token from microsoft"
            raise Exception(msg)


async def get_user_photo(token: str) -> BytesIO:
    async with httpx.AsyncClient() as client:
        graph_response: httpx.Response = await client.get(
                f"{graph_base_url}/me/photo/$value",
                headers={
                        "Authorization": f"Bearer {token}"
                },
        )
        graph_response.raise_for_status()
        graph = graph_response.content
        image = BytesIO()
        image.write(graph)
        image.seek(0)

        return image


async def get_user_info(token: str) -> UserProfile:
    async with httpx.AsyncClient() as client:
        graph_response: httpx.Response = await client.get(
                f"{graph_base_url}/me",
                headers={
                        "Authorization": f"Bearer {token}"
                },
        )
        graph_response.raise_for_status()

        return UserProfile.model_validate(graph_response.json())
