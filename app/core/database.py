"""
Core Database Configuration and Session Setup
"""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

class Base(DeclarativeBase):
    pass

engine = create_engine(
    "sqlite:///./bess.db",
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    Dependency for generating database sessions.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
