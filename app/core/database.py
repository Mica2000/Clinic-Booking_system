from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# Create the SQLAlchemy engine
engine = create_engine(
    settings.database_url,
    echo=True,
)

# Create a session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for all database models
Base = declarative_base()


def get_db():
    """
    Provides a database session for each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()