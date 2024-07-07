from sqlalchemy import Column, Integer, String, TIMESTAMP, Enum
from chatbot.database import Base, TimeStampMixin


class Message(Base, TimeStampMixin):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, nullable=False)
    message_type = Column(Enum("user", "assistant", "system"), nullable=False)
    text = Column(String(length=255), nullable=False)
