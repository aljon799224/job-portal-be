from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import datetime


class SavedJobBase(BaseModel):
    """SavedJob Base Class."""

    model_config = ConfigDict(from_attributes=True, extra="ignore")

    user_id: int
    job_id: int


class SavedJobIn(SavedJobBase):
    """SavedJob In Class."""

    pass


class SavedJobOut(SavedJobBase):
    """SavedJob Out Class."""

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class SavedJobsOut(SavedJobBase):
    """SavedJob Out Class."""

    id: int
    user_id: int
    job_title: Optional[str] = None
    job_location: Optional[str] = None
    job_description: Optional[str] = None
    job_salary: Optional[str] = None
    created_at: datetime
    updated_at: datetime
