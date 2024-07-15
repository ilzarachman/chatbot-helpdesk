from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Read the SQLAlchemy URL from alembic.ini
with open("alembic.ini") as config_file:
    for line in config_file:
        if line.startswith("sqlalchemy.url"):
            db_url = line.split("=")[1].strip()
            break

# engine = create_async_engine(db_url, pool_size=100, max_overflow=0)
engine = create_engine(
    db_url,
    pool_size=10,  # Increase pool size
    max_overflow=20,  # Increase overflow limit
    pool_timeout=30,  # Adjust timeout as needed
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class TimeStampMixin:
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
