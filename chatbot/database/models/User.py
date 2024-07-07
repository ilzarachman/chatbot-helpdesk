from sqlalchemy import Column, Integer, String
from chatbot.database import Base, TimeStampMixin


class User(Base, TimeStampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    student_number = Column(String(length=255), nullable=False, unique=True)
    name = Column(String(length=255), nullable=False)
    email = Column(String(length=255), nullable=False, unique=True)
    password = Column(String(length=255), nullable=False)
    salt = Column(String(length=255), nullable=False)
