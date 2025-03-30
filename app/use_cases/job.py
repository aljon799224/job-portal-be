"""Job Use Case."""

import logging
from typing import Union

from fastapi_pagination import paginate, Page
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import schemas
from app.models import Job, Application
from app.repositories.application import ApplicationRepository
from app.repositories.job import JobRepository
from exceptions.exceptions import DatabaseException, APIException

logger = logging.getLogger(__name__)


class JobUseCase:
    """Job Use Case Class."""

    def __init__(self, db: Session):
        """Initialize with db and Job Repository."""
        self.db = db
        self.job_repository = JobRepository(Job)
        self.application_repository = ApplicationRepository(Application)

    def get_jobs(self) -> Union[Page[schemas.JobOut], JSONResponse]:
        """Get all jobs record."""
        try:
            jobs = self.job_repository.get_all(self.db)

        except DatabaseException as e:
            logger.error(f"Database error occurred while fetching jobs: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        return paginate(jobs)

    def get_job(self, _id: int) -> Union[schemas.JobOut, JSONResponse]:
        """Get job record."""
        try:
            job = self.job_repository.get(self.db, _id)

            return schemas.JobOut.model_validate(job)

        except APIException as e:
            logger.error(f"Database error occurred while fetching job: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def get_jobs_by_user_id(
            self, user_id: int
    ) -> Union[Page[schemas.JobOut], JSONResponse]:
        """Get all jobs by user id record."""
        try:

            jobs = self.job_repository.get_all_by_user_id(
                self.db, user_id=user_id
            )

        except DatabaseException as e:
            logger.error(
                f"Database error occurred while fetching evaluations: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        return paginate(jobs)

    def get_applied_jobs(
            self, user_id: int
    ) -> Union[Page[schemas.JobOut], JSONResponse]:
        """Get all jobs by user id record."""
        try:
            jobs = []

            applications = self.application_repository.get_all_by_user_id(self.db, user_id=user_id)

            for app in applications:
                job = self.job_repository.get(self.db, _id=app.job_id)
                jobs.append(job)

        except DatabaseException as e:
            logger.error(
                f"Database error occurred while fetching evaluations: {e.detail}"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        return paginate(jobs)

    def create_job(
            self,
            *,
            obj_in: schemas.JobIn,
    ) -> Union[schemas.JobOut, JSONResponse]:
        """Create job record."""
        try:
            job = self.job_repository.create(db=self.db, obj_in=obj_in)

            return schemas.JobOut.model_validate(job)

        except DatabaseException as e:
            logger.error(f"Database error occurred while creating job: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def update_job(
            self,
            _id: int,
            *,
            obj_in: schemas.JobIn,
    ) -> Union[schemas.JobOut, JSONResponse]:
        """Update job record."""
        try:
            job = self.job_repository.get(db=self.db, _id=_id)

            job_update = self.job_repository.update(
                db=self.db, obj_in=obj_in, db_obj=job
            )

            return schemas.JobOut.model_validate(job_update)

        except (DatabaseException, APIException) as e:
            logger.error(f"Database error occurred while updating job: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def delete_job(self, _id: int) -> Union[schemas.JobOut, JSONResponse]:
        """Delete job record."""
        try:
            job_update = self.job_repository.delete(db=self.db, _id=_id)

            return schemas.JobOut.model_validate(job_update)

        except (DatabaseException, APIException) as e:
            logger.error(f"Database error occurred while deleting job: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
