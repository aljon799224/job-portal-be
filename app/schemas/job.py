from pydantic import BaseModel, ConfigDict
from datetime import datetime


class JobBase(BaseModel):
    """Job Base Class."""

    model_config = ConfigDict(from_attributes=True, extra="ignore")

    title: str
    description: str
    salary: str | None = None
    location: str
    tags: str | None = None
    is_remote: bool | None = None


class JobIn(JobBase):
    """Job In Class."""

    user_id: int


class JobOut(JobBase):
    """Job Out Class."""

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
