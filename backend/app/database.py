import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.models import Base

# Use environment variable for database URL
# Tests can override this to use a separate test database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./gallery.db")

# Only use check_same_thread for SQLite (Postgres doesn't need it)
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    """Get a database session. Use as a context manager or dependency."""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
