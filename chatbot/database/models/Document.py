from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from chatbot.database import Base, TimeStampMixin
# from chatbot.database.models.Staff import Staff


class Document(Base, TimeStampMixin):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(length=255), nullable=False, unique=True)

    name = Column(String(length=255), nullable=False)
    uploader_id: Mapped[int] = mapped_column(ForeignKey("staffs.id"))
    uploader: Mapped["Staff"] = relationship("Staff", back_populates="documents")
    embedded = Column(Boolean, nullable=False, default=False)
    intent = Column(String(length=255), nullable=False)
    public = Column(Boolean, nullable=False, default=False)
    file_path = Column(String(length=500), nullable=True)

    def __repr__(self):
        return f"<Document(id={self.id}, uuid={self.uuid}, name={self.name}, uploader_id={self.uploader_id}, embedded={self.embedded})>"

    def __str__(self):
        return f"Document(id={self.id}, uuid={self.uuid}, name={self.name}, uploader_id={self.uploader_id}, embedded={self.embedded})"
