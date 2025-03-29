from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ApplicationBase(BaseModel):
    """Application Base Class."""

    model_config = ConfigDict(from_attributes=True, extra="ignore")

    email: str | None = None
    mobile_number: str | None = None
    expected_salary: int | None = None
    resume: str | None = None
    user_id: int
    job_id: int


class ApplicationIn(ApplicationBase):
    """Application In Class."""

    user_id: int


class ApplicationOut(ApplicationBase):
    """Application Out Class."""

    id: int
    applied_at: datetime
