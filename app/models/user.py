"""User model."""

from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    """User Class."""

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=True)
    email = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)

    jobs = relationship("Job", back_populates="user", cascade="all, delete")
