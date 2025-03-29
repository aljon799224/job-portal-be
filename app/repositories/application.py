"""Application Repository."""
from typing import List, cast

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models import Application
from app.repositories.base import BaseRepository
from app.schemas import ApplicationIn


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
