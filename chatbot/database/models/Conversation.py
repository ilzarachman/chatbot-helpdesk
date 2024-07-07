from sqlalchemy import Column, Integer, String, TIMESTAMP
from chatbot.database import Base, TimeStampMixin


class Conversation(Base, TimeStampMixin):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)
