from typing import Type

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from chatbot.database import Base, TimeStampMixin


class Student(Base, TimeStampMixin):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    student_number = Column(String(length=255), nullable=False, unique=True)
    name = Column(String(length=255), nullable=False)
    access_level = Column(Integer, nullable=False, default=1)
    email = Column(String(length=255), nullable=False, unique=True)
    password = Column(String(length=255), nullable=False)
    salt = Column(String(length=255), nullable=False)

    @classmethod
    def get_user_by_student_number(cls, db: Session, student_number: str) -> Type["Student"] | None:
        """
        Returns the user with the given student number.

        Args:
            db (Session): The database session.
            student_number (str): The student number of the user.

        Returns:
            Student: The user with the given student number.
        """
        return db.query(cls).filter_by(student_number=student_number).first()
