from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base


class Job(Base):
    """Job Model."""

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)  # Links to User table
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    salary = Column(String, nullable=True)  # Can store range or amount as string
    location = Column(String, nullable=False)
    tags = Column(String, nullable=True)  # Store comma-separated keywords
    is_remote = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="jobs")
