"""Job Repository."""
from typing import Optional, List, cast

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models import Job
from app.repositories.base import BaseRepository
from app.schemas import JobIn


class JobRepository(BaseRepository[Job, JobIn, JobIn]):
    """Job Repository Class."""

    @staticmethod
    def get_all_by_user_id(db: Session, *, user_id: int) -> List[Job]:
        """Get by user id."""
        response = cast(
            List[Job],
            db.query(Job).filter(Job.user_id == user_id).order_by(desc(Job.updated_at)).all(),
        )

        return response
