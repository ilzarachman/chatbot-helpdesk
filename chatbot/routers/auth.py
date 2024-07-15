import hashlib

from fastapi import APIRouter, Response, HTTPException, status, Request, Depends
from chatbot.http.Response import Response as ResponseTemplate
from pydantic import BaseModel
from chatbot.database.models.Student import Student as UserModel
from chatbot.database.models.Staff import Staff as StaffModel
from chatbot.database import SessionLocal
from chatbot.dependencies.utils.SessionManagement import (
    SessionManagement,
    SessionData,
    SessionDataType,
)
from chatbot.dependencies.utils.auth import protected_route, ACL

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_auth(auth: str = Depends(protected_route(ACL.USER))):
    """
    Retrieves authentication information based on the provided auth token.

    Parameters:
    - auth (str, optional): The authentication token to validate.

    Returns:
    - bool: True if the authentication is successful, False otherwise.
    """
    return True


class StudentCredential(BaseModel):
    student_number: str
    password: str


class StaffCredential(BaseModel):
    staff_number: str
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
async def login(credential: StudentCredential, response: Response):
    """
    Authenticates a user based on the provided credentials.

    Args:
        credential (StudentCredential): The user's credential object containing student_number and password.
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
    session_token = SessionManagement.create_session_token(
        SessionData(id=user.id, type=SessionDataType.USER)
    )

    response.set_cookie(key="session_token", value=session_token, httponly=True)

    return ResponseTemplate(
        message="Login successful",
        data={"user_id": user.id},
    )


@router.post("/staff/login", status_code=status.HTTP_200_OK)
async def staff_login(credential: StaffCredential, response: Response):
    """
    Authenticates a staff member based on the provided credentials.

    Args:
        credential (StaffCredential): The staff member's credential object containing staff_number and password.
        response (Response): The response object to set the session token cookie.

    Raises:
        HTTPException: If the staff member is not found or if the credentials are invalid.

    Returns:
        ResponseTemplate: A response indicating the success of the login and the staff member's ID.
    """
    staff_number = credential.staff_number
    password = credential.password

    db = SessionLocal()
    user = StaffModel.get_user_by_staff_number(db, staff_number)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    if not compare_password(user.password, user.salt, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    session_token = SessionManagement.create_session_token(
        SessionData(id=user.id, type=SessionDataType.STAFF)
    )

    response.set_cookie(key="session_token", value=session_token, httponly=True)

    return ResponseTemplate(
        message="Login successful",
        data={"user_id": user.id},
    )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response, auth_user=Depends(protected_route(ACL.USER))):
    """
    Logs out a user by removing the session token cookie.

    Args:
        response (Response): The response object to remove the session token cookie.

    Returns:
        ResponseTemplate: A response indicating the success of the logout.
    """
    response.delete_cookie(key="session_token")
    return {"message": "Logout successful"}
