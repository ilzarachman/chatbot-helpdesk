from fastapi import Depends, HTTPException, status, Request, Response

from chatbot.database.models.User import User as UserModel
from chatbot.database import SessionLocal
from chatbot.dependencies.utils.SessionManagement import SessionManagement


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


async def protected(token: str = Depends(get_token_from_cookie), response: Response = None):
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
    user: UserModel = db.query(UserModel).get(data["user_id"])

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return user
