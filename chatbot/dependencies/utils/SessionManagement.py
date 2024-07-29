import json
import os
from enum import Enum
from typing import Any
from itsdangerous import URLSafeTimedSerializer
from pydantic import BaseModel

from chatbot.logger import logger


class SessionDataType(Enum):
    USER = 1
    STAFF = 0


class SessionData(BaseModel):
    id: int
    type: SessionDataType


class SessionManagement:
    secret_key = os.environ.get("SECRET_KEY", "123")
    serializer = URLSafeTimedSerializer(secret_key)

    @classmethod
    def create_session_token(cls, data: SessionData) -> str:
        """
        Creates a session token based on the input data.

        Args:
            data (dict): The data to be serialized into the session token.

        Returns:
            str: The generated session token.
        """
        return cls.serializer.dumps(data.json())

    @classmethod
    def verify_session_token(cls, token: str) -> Any | None:
        """
        Verifies the session token by deserializing it using the serializer.

        Args:
            token (str): The session token to be verified.

        Returns:
            Any | None: The deserialized data from the token, or None if verification fails.
        """

        if token is None:
            return None

        try:
            data = cls.serializer.loads(token, max_age=15 * 24 * 60 * 60)
            return json.loads(data)
        except Exception as e:
            logger.error(e)
            return None
