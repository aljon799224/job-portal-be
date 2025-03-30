"""Saved Job Repository."""
from http import HTTPStatus
from typing import List, cast, Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models import SavedJob
from app.repositories.base import BaseRepository
from app.schemas import SavedJobIn
from exceptions.exceptions import APIException


class SavedJobRepository(BaseRepository[SavedJob, SavedJobIn, SavedJobIn]):
    """Saved Job Repository Class."""

    @staticmethod
    def get_all_by_user_id(db: Session, *, user_id: int) -> List[SavedJob]:
        """Get by user id."""
        response = cast(
            List[SavedJob],
            db.query(SavedJob).filter(SavedJob.user_id == user_id).order_by(desc(SavedJob.updated_at)).all(),
        )

        return response

    @staticmethod
    def get_by_user_id_and_job_id(db: Session, *, user_id: int, job_id: int) -> SavedJob:
        """Get a single save job by user ID and job ID."""
        response: Optional[SavedJob] = (
            db.query(SavedJob)
            .filter(SavedJob.user_id == user_id, SavedJob.job_id == job_id)
            .first()
        )

        if response is None:
            raise APIException(
                status_code=HTTPStatus.NOT_FOUND, detail="Record not found."
            )
        return response
