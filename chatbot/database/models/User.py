from typing import Type

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from chatbot.database import Base, TimeStampMixin


class User(Base, TimeStampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    student_number = Column(String(length=255), nullable=False, unique=True)
    name = Column(String(length=255), nullable=False)
    email = Column(String(length=255), nullable=False, unique=True)
    password = Column(String(length=255), nullable=False)
    salt = Column(String(length=255), nullable=False)

    @classmethod
    def get_user_by_student_number(cls, db: Session, student_number: str) -> Type["User"] | None:
        """
        Returns the user with the given student number.

        Args:
            db (Session): The database session.
            student_number (str): The student number of the user.

        Returns:
            User: The user with the given student number.
        """
        return db.query(cls).filter_by(student_number=student_number).first()
