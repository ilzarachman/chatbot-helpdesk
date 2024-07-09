from typing import Any

from pydantic import BaseModel


class Response(BaseModel):
    """
    Response model.
    """

    message: str
    data: Any
