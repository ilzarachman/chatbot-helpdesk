import os

from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# engine = create_async_engine(db_url, pool_size=100, max_overflow=0)
engine = create_engine(
    os.getenv("DATABASE_URL"),
    pool_size=10,  # Increase pool size
    max_overflow=20,  # Increase overflow limit
    pool_timeout=30,  # Adjust timeout as needed
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class TimeStampMixin:
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
