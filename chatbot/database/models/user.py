from sqlalchemy import Column, Integer, String
from chatbot.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    student_number = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
