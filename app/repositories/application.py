"""Application Repository."""
from http import HTTPStatus
from typing import List, cast, Optional, Union

from sqlalchemy import desc
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.models import Application
from app.repositories.base import BaseRepository
from app.schemas import ApplicationIn
from exceptions.exceptions import APIException


class ApplicationRepository(BaseRepository[Application, ApplicationIn, ApplicationIn]):
    """Application Repository Class."""

    @staticmethod
    def get_all_by_job_id(db: Session, *, job_id: int) -> List[Application]:
        """Get by user id."""
        response = cast(
            List[Application],
            db.query(Application).filter(Application.job_id == job_id).order_by(desc(Application.updated_at)).all(),
        )

        return response

    @staticmethod
    def get_all_by_user_id(db: Session, *, user_id: int) -> List[Application]:
        """Get by user id."""
        response = cast(
            List[Application],
            db.query(Application).filter(Application.user_id == user_id).order_by(desc(Application.updated_at)).all(),
        )

        return response

    @staticmethod
    def get_by_user_id_and_job_id(db: Session, *, user_id: int, job_id: int) -> Application:
        """Get a single application by user ID and job ID."""
        application: Optional[Application] = (
            db.query(Application)
            .filter(Application.user_id == user_id, Application.job_id == job_id)
            .first()
        )

        if application is None:
            raise APIException(
                status_code=HTTPStatus.NOT_FOUND, detail="Record not found."
            )
        return application
