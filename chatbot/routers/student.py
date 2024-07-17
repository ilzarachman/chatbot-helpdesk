import os

from fastapi import APIRouter, Depends, HTTPException, status, Request
from chatbot.database import SessionLocal
from pydantic import BaseModel
from chatbot.database.models.Student import Student as UserModel
import hashlib
import secrets

from chatbot.http.Response import Response
from chatbot.dependencies.utils.auth import protected_route, ACL

router = APIRouter(prefix="/student", tags=["Student"])


class CreateStudentRequest(BaseModel):
    """
    Represents a user with student information.
    """

    student_number: str
    name: str
    email: str
    password: str


class Student(BaseModel):
    """
    Represents a user with student information.
    """

    id: int
    student_number: str
    name: str
    email: str


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: CreateStudentRequest, auth_user=Depends(protected_route())
) -> Response:
    """
    Creates a new user in the database.

    Args:
        user (CreateStudentRequest): User data including student number, name, email, and password.
        auth_user (User, optional): The authenticated user. Defaults to Depends(protected_route()).

    Returns:
        UserResponse: A message indicating successful user creation and the created user details.
    """
    with SessionLocal() as db:
        new_user = UserModel()

        # Generate a random salt
        salt = secrets.token_hex(16)  # 16 bytes (128 bits) for a secure salt
        salted_password = user.password + salt
        hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()

        new_user.student_number = user.student_number
        new_user.name = user.name
        new_user.email = user.email
        new_user.password = hashed_password
        new_user.salt = salt

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    return Response(
        data=Student(
            id=new_user.id,
            student_number=new_user.student_number,
            name=new_user.name,
            email=new_user.email,
        ),
        message="User created",
    )


class UpdateStudentRequest(BaseModel):
    """
    Represents a user with student information.
    """

    student_number: str | None = None
    name: str | None = None
    email: str | None = None


@router.put("/update/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
    user_id: int, user: UpdateStudentRequest, auth_user=Depends(protected_route())
) -> Response:
    """
    Updates a user in the database.

    Args:
        user_id (int): The ID of the user to update.
        user (CreateStudentRequest): User data including student number, name, email, and password.
        auth_user (Depends(protected_route())): The authenticated user.

    Returns:
        dict: A message indicating successful user update and the updated user details.
    """
    with SessionLocal() as db:
        user_to_update = db.query(UserModel).filter(UserModel.id == user_id).first()

        if user_to_update:
            user_to_update.student_number = (
                user.student_number
                if user.student_number
                else user_to_update.student_number
            )
            user_to_update.name = user.name if user.name else user_to_update.name
            user_to_update.email = user.email if user.email else user_to_update.email

            db.commit()
            db.refresh(user_to_update)

        return Response(
            data=Student(
                id=user_to_update.id,
                student_number=user_to_update.student_number,
                name=user_to_update.name,
                email=user_to_update.email,
            ),
            message="User updated",
        )

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.delete("/delete/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, auth_user=Depends(protected_route())) -> Response:
    """
    Deletes a user from the database.

    Args:
        user_id (int): The ID of the user to delete.

    Returns:
        dict: A message indicating successful user deletion.
    """
    with SessionLocal() as db:
        user_to_delete = db.query(UserModel).filter(UserModel.id == user_id).first()

        if user_to_delete:
            db.delete(user_to_delete)
            db.commit()

            return Response(
                data=Student(
                    id=user_to_delete.id,
                    student_number=user_to_delete.student_number,
                    name=user_to_delete.name,
                    email=user_to_delete.email,
                ),
                message=f"User with ID:{user_id} deleted",
            )

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.get("/get/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int, auth_user=Depends(protected_route())) -> Response:
    """
    Retrieves a user from the database.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        dict: A message indicating successful user retrieval and the retrieved user details.
    """
    with SessionLocal() as db:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if user:
        return Response(
            data=Student(
                id=user.id,
                student_number=user.student_number,
                name=user.name,
                email=user.email,
            ),
            message="User retrieved",
        )

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_all_users(auth_user=Depends(protected_route())) -> Response:
    """
    Retrieves all users from the database.

    Returns:
        dict: A message indicating successful user retrieval and the retrieved user details.
    """
    with SessionLocal() as db:
        users = db.query(UserModel).all()

        _users = [
            Student(
                id=user.id,
                student_number=user.student_number,
                name=user.name,
                email=user.email,
            )
            for user in users
        ]

    if users:
        return Response(data=_users, message="Users retrieved")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")


@router.get("/search", status_code=status.HTTP_200_OK)
async def search_user(
    request: Request, auth_user=Depends(protected_route())
) -> Response:
    """
    Searches for a user in the database using a query string.

    Returns:
        dict: A message indicating successful user search and the retrieved user details.
    """
    query = request.query_params.get("query")

    with SessionLocal() as db:
        users = (
            db.query(UserModel)
            .filter(
                UserModel.name.contains(query)
                | UserModel.email.contains(query)
                | UserModel.student_number.contains(query)
            )
            .all()
        )

        _users = [
            Student(
                id=user.id,
                student_number=user.student_number,
                name=user.name,
                email=user.email,
            )
            for user in users
        ]

    if users:
        return Response(data=_users, message="Users retrieved")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")
