from fastapi import status
from fastapi.exceptions import HTTPException


class Forbid(HTTPException):
    """
    Exception raised when the user is not authorized
    """

    def __init__(self, detail: str) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
