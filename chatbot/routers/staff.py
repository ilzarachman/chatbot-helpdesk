import os

from fastapi import APIRouter, Depends, HTTPException, status, Request
from chatbot.database import SessionLocal
from pydantic import BaseModel
from chatbot.database.models.Staff import Staff as StaffModel
import hashlib
import secrets

from chatbot.http.Response import Response as ResponseTemplate
from chatbot.dependencies.utils.auth import protected_route, ACL
from chatbot.logger import logger

router = APIRouter(prefix="/staff", tags=["Staff"])


class CreateStaffRequest(BaseModel):
    staff_number: str
    name: str
    email: str
    password: str


class Staff(BaseModel):
    id: int
    staff_number: str
    name: str
    email: str


async def admin_access(request: Request):
    passkey = request.query_params.get("passkey")

    if not passkey:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No passkey provided",
        )

    if passkey != os.getenv("ADMIN_PASSKEY"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid passkey",
        )


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_staff(
    staff: CreateStaffRequest, admin_access=Depends(admin_access)
) -> ResponseTemplate:
    with SessionLocal() as db:
        new_staff = StaffModel()

        # Generate a random salt
        salt = secrets.token_hex(16)  # 16 bytes (128 bits) for a secure salt
        salted_password = staff.password + salt
        hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()

        new_staff.staff_number = staff.staff_number
        new_staff.name = staff.name
        new_staff.email = staff.email
        new_staff.password = hashed_password
        new_staff.salt = salt

        db.add(new_staff)
        db.commit()
        db.refresh(new_staff)

        staff = Staff(
            id=new_staff.id,
            staff_number=new_staff.staff_number,
            name=new_staff.name,
            email=new_staff.email,
        )

    logger.debug(f"Created staff: {staff}")

    return ResponseTemplate(data=staff, message="Staff created successfully")


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_staff(staff_id: int, admin_access=Depends(admin_access)) -> None:
    with SessionLocal() as db:
        staff = db.query(StaffModel).filter_by(id=staff_id).first()
        if not staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Staff not found",
            )

        db.delete(staff)
        db.commit()

    logger.debug(f"Deleted staff: {staff}")

    return None
