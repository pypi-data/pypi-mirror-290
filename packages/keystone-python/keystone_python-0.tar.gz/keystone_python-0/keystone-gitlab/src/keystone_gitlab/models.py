from typing import List

from pydantic import BaseModel


class IssuePayload(BaseModel):
    title: str
    text: str
    labels: List[str]
