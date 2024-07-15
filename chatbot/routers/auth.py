import hashlib

from fastapi import APIRouter, Response, HTTPException, status, Request, Depends
from chatbot.http.Response import Response as ResponseTemplate
from pydantic import BaseModel
from chatbot.database.models.User import User as UserModel
from chatbot.database import SessionLocal
from dependencies.utils.SessionManagement import SessionManagement
from dependencies.utils.auth import protected

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_auth(auth: str = Depends(protected)):
    """
    Retrieves authentication information based on the provided auth token.

    Parameters:
    - auth (str, optional): The authentication token to validate.

    Returns:
    - bool: True if the authentication is successful, False otherwise.
    """
    return True


class Credential(BaseModel):
    student_number: str
    password: str


def compare_password(user_hashed_password: str, salt: str, password: str) -> bool:
    """
    Compares a user's hashed password with its salt and password.

    Args:
        user_hashed_password (str): The user's hashed password.
        salt (str): The user's salt.
        password (str): The user's password.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    salted_password = password + salt
    hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
    return user_hashed_password == hashed_password


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(credential: Credential, response: Response):
    """
    Authenticates a user based on the provided credentials.

    Args:
        credential (Credential): The user's credential object containing student_number and password.
        response (Response): The response object to set the session token cookie.

    Raises:
        HTTPException: If the user is not found or if the credentials are invalid.

    Returns:
        ResponseTemplate: A response indicating the success of the login and the user's ID.
    """
    student_number = credential.student_number
    password = credential.password

    db = SessionLocal()
    user = UserModel.get_user_by_student_number(db, student_number)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    if not compare_password(user.password, user.salt, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    # generate JWT token for session token
    session_token = SessionManagement.create_session_token({"user_id": user.id})

    response.set_cookie(key="session_token", value=session_token, httponly=True)

    return ResponseTemplate(
        message="Login successful",
        data={"user_id": user.id},
    )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response, auth_user=Depends(protected)):
    """
    Logs out a user by removing the session token cookie.

    Args:
        response (Response): The response object to remove the session token cookie.

    Returns:
        ResponseTemplate: A response indicating the success of the logout.
    """
    response.delete_cookie(key="session_token")
    return {"message": "Logout successful"}
