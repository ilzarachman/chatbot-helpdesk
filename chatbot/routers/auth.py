import hashlib
import secrets

from fastapi import APIRouter, Request, Response, HTTPException, status, Depends
from starlette.requests import Request as StarletteRequest
from pydantic import BaseModel

from chatbot.database import SessionLocal
from chatbot.database.models.Staff import Staff as StaffModel
from chatbot.database.models.Student import Student as UserModel
from chatbot.dependencies.utils.SessionManagement import (
    SessionManagement,
    SessionData,
    SessionDataType,
)
from chatbot.dependencies.utils.auth import protected_route, ACL
from chatbot.http.Response import Response as ResponseTemplate
from authlib.integrations.starlette_client import OAuth
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.responses import RedirectResponse
from chatbot.logger import logger
import os

router = APIRouter(prefix="/auth", tags=["Auth"])

# OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")

if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    raise Exception("Google client ID or secret not found")

oauth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    authorize_params=None,
    access_token_params=None,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    refresh_token_url=None,
    redirect_uri="http://localhost:8000/api/v1/auth/google-oauth/callback",
    client_kwargs={"scope": "openid email profile"},
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_auth(auth: StaffModel | UserModel = Depends(protected_route(ACL.USER))):
    """
    Retrieves authentication information based on the provided auth token.

    Parameters:
    - auth (str, optional): The authentication token to validate.

    Returns:
    - bool: True if the authentication is successful, False otherwise.
    """
    if isinstance(auth, UserModel):
        return {"access_level": ACL.USER.value, "user": auth}

    if isinstance(auth, StaffModel):
        return {"access_level": ACL.STAFF.value, "user": auth}

    return None


@router.get("/user", status_code=status.HTTP_200_OK)
async def get_user(auth_user=Depends(protected_route(ACL.USER))):
    """
    Retrieves user information based on the provided auth token.

    Parameters:
    - auth_user (User, optional): The authenticated user.

    Returns:
    - User: The authenticated user.
    """
    if isinstance(auth_user, UserModel):
        return {
            "number": auth_user.student_number,
            "name": auth_user.name,
            "email": auth_user.email,
        }

    if isinstance(auth_user, StaffModel):
        return {
            "number": auth_user.staff_number,
            "name": auth_user.name,
            "email": auth_user.email,
        }

    return None


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

    with SessionLocal() as db:
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
    with db:
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


@router.post("/google-oauth/login", status_code=status.HTTP_200_OK)
async def google_login(request: StarletteRequest):
    """
    Initiates a Google OAuth 2.0 login flow.

    Returns a redirect response to the Google authorization URL.
    """
    redirect_uri = request.url_for("auth_callback")  # Update this if needed
    google_oauth_uri = await oauth.google.authorize_redirect(request, redirect_uri)

    return {"redirect_url": google_oauth_uri._headers["location"]}


@router.get("/google-oauth/callback", status_code=status.HTTP_200_OK)
async def auth_callback(request: StarletteRequest, res: Response):
    """
    Callback endpoint for Google OAuth 2.0 login flow.

    Returns a JSON response with a message indicating successful login and the user's ID.
    """
    token = await oauth.google.authorize_access_token(request)
    user_info = token["userinfo"]

    logger.debug(f"Logged in using Google: {user_info}")

    # Validate email domain
    email = user_info["email"]
    if not (email.endswith("@unesa.ac.id") or email.endswith("@mhs.unesa.ac.id")):
        logger.error(f"Unauthorized email domain: {email}")
        # TODO: Change this to be a proper redirect
        return RedirectResponse(f"http://localhost:3000/redirect/none?error_msg=Unauthorized email domain&desc=Please use your Unesa email", status_code=status.HTTP_302_FOUND)

    with SessionLocal() as db:
        # Check if user already exists in the database
        existing_user = db.query(UserModel).filter(UserModel.email == email).first()

        if existing_user is None:
            # Save new user to the database
            new_user = UserModel()
            new_user.student_number = email.split("@")[0]
            new_user.name = user_info["name"]
            new_user.email = email
            new_user.password = secrets.token_hex(32)
            new_user.salt = secrets.token_hex(16)

            db.add(new_user)
            db.commit()

        session_token = SessionManagement.create_session_token(
            SessionData(
                id=existing_user.id if existing_user else new_user.id,
                type=SessionDataType.USER,
            )
        )

        res.set_cookie(key="session_token", value=session_token, httponly=True)

    # TODO: Change this to be a proper redirect
    return RedirectResponse(f"http://localhost:3000/redirect/{session_token}", status_code=status.HTTP_302_FOUND, headers=res.headers)


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
