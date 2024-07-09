from fastapi import APIRouter, Depends, HTTPException, status
from chatbot.database import SessionLocal
from pydantic import BaseModel
from chatbot.database.models.User import User as UserModel
import hashlib
import secrets

router = APIRouter(prefix="/user", tags=["user"])


class UserRequest(BaseModel):
    """
    Represents a user with student information.
    """

    student_number: str
    name: str
    email: str
    password: str


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserRequest):
    """
    Creates a new user in the database.

    Args:
        user (UserRequest): User data including student number, name, email, and password.

    Returns:
        dict: A message indicating successful user creation and the user details.
    """
    db = SessionLocal()
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
    db.close()
    return {"message": "User created", "user": new_user}


@router.put("/update/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UserRequest):
    """
    Updates a user in the database.

    Args:
        user_id (int): The ID of the user to update.
        user (UserRequest): User data including student number, name, email, and password.

    Returns:
        dict: A message indicating successful user update and the updated user details.
    """
    db = SessionLocal()
    user_to_update = db.query(UserModel).filter(UserModel.id == user_id).first()

    if user_to_update:
        user_to_update.student_number = user.student_number
        user_to_update.name = user.name
        user_to_update.email = user.email

        salt = secrets.token_hex(16)  # 16 bytes (128 bits) for a secure salt
        salted_password = user.password + salt
        hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()

        user_to_update.password = hashed_password
        user_to_update.salt = salt

        db.commit()
        db.refresh(user_to_update)
        db.close()
        return {"message": "User updated", "user": user_to_update}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.delete("/delete/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int):
    """
    Deletes a user from the database.

    Args:
        user_id (int): The ID of the user to delete.

    Returns:
        dict: A message indicating successful user deletion.
    """
    db = SessionLocal()
    user_to_delete = db.query(UserModel).filter(UserModel.id == user_id).first()

    if user_to_delete:
        db.delete(user_to_delete)
        db.commit()
        db.close()
        return {"message": f"User with ID:{user_id} deleted"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.get("/get/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int):
    """
    Retrieves a user from the database.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        dict: A message indicating successful user retrieval and the retrieved user details.
    """
    db = SessionLocal()
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    db.close()

    if user:
        return {"message": "User retrieved", "user": user}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
