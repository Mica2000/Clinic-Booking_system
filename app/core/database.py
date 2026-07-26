from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.base import Base

# Create the SQLAlchemy engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
)

# Create a session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db():
    """
    Provides a database session for each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()