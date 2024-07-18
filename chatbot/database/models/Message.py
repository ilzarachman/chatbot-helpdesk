from sqlalchemy import Column, Integer, String, TIMESTAMP, Enum, Text
from chatbot.database import Base, TimeStampMixin


class Message(Base, TimeStampMixin):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, nullable=False)
    text = Column(Text(4294000000), nullable=False)
