from typing import Type, List

from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import Session, relationship, Mapped

from chatbot.database import Base, TimeStampMixin


class Question(Base, TimeStampMixin):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    prompt = Column(Text, nullable=False)
    staff_answer = Column(Text, nullable=True)
    bot_answer = Column(Text, nullable=True)
    intent = Column(String(length=255), nullable=True)
    public = Column(Boolean, nullable=False, default=False)
    message = Column(Text, nullable=True)

    questioner_email = Column(String(length=255), nullable=True)
    questioner_name = Column(String(length=255), nullable=True)
    answered_by = Column(Integer, nullable=True) # Staff id
