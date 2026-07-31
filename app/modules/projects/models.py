<<<<<<< HEAD
"""
Projects Module - SQLAlchemy Models
"""

from datetime import datetime
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Project(Base):
    """
    SQLAlchemy model representing the projects table.
    """

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
=======
from typing import TypedDict


class Project(TypedDict):

    project_id: str

    project_name: str

    location_name: str

    application_type: str

    charging_source: str

    current_step: int
>>>>>>> fb7a2c0 (Implemented project details and location weather APIs)
