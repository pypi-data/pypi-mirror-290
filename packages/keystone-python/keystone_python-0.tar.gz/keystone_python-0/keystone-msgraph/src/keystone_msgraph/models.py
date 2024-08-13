from typing import Optional

from pydantic import BaseModel, Field


class ODataResponse(BaseModel):
    context: str = Field(alias="@odata.context")


class UserProfile(ODataResponse):
    displayName: str
    givenName: str
    jobTitle: Optional[str]
    mail: str
    mobilePhone: Optional[str]
    officeLocation: Optional[str]
    surname: str
    userPrincipalName: str
    id: str
