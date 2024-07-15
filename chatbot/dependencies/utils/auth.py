from enum import Enum

from fastapi import Depends, HTTPException, status, Request, Response

from chatbot.database.models.Student import Student as UserModel
from chatbot.database.models.Staff import Staff as StaffModel
from chatbot.database import SessionLocal
from chatbot.dependencies.utils.SessionManagement import SessionManagement
from dependencies.utils.SessionManagement import SessionDataType


def get_token_from_cookie(request: Request) -> str | None:
    """
    Retrieves the session token from the request's cookies.

    Args:
        request (Request): The request object.

    Returns:
        str | None: The session token if it exists, or None if it doesn't.
    """
    cookies = request.cookies
    if "session_token" in cookies:
        return cookies["session_token"]
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Session token not found"
    )


class ACL(Enum):
    """
    Enum representing the access levels of a user.
    """

    STAFF = 0
    USER = 1


def protected_route(access_level: ACL = ACL.STAFF):
    async def protected(
        token: str = Depends(get_token_from_cookie), response: Response = None
    ) -> UserModel | StaffModel:
        """
        Authenticates a user based on the provided session token.

        Args:
            token (str, optional): The session token. Defaults to Depends(get_token_from_cookie).
            response (Response, optional): The response object. Defaults to None.

        Raises:
            HTTPException: If the user is not found or if the credentials are invalid.

        Returns:
            user: The authenticated user.
        """
        data = SessionManagement.verify_session_token(token)
        if data is None:
            response.delete_cookie("session_token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        db = SessionLocal()

        if data["type"] == SessionDataType.STAFF.value:
            user: StaffModel = db.query(StaffModel).get(data["id"])
        elif data["type"] == SessionDataType.USER.value:
            user: UserModel = db.query(UserModel).get(data["id"])
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        if user.access_level > access_level.value:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied"
            )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )

        return user

    return protected
