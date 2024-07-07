from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TimeStampMixin:
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())