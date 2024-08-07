from typing import Type, List

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session, relationship, Mapped

from chatbot.database import Base, TimeStampMixin
# from chatbot.database.models.Document import Document


class Staff(Base, TimeStampMixin):
    __tablename__ = "staffs"

    id = Column(Integer, primary_key=True)
    staff_number = Column(String(length=255), nullable=False, unique=True)
    name = Column(String(length=255), nullable=False)
    access_level = Column(Integer, nullable=False, default=0)
    email = Column(String(length=255), nullable=False, unique=True)
    password = Column(String(length=255), nullable=False)
    salt = Column(String(length=255), nullable=False)
    documents: Mapped[List["Document"]] = relationship(back_populates="uploader")

    @classmethod
    def get_user_by_staff_number(
        cls, session: Session, staff_number: str
    ) -> Type["Staff"]:
        return session.query(cls).filter_by(staff_number=staff_number).first()
