"""SavedJob Use Case."""

import logging
from typing import Union

from fastapi_pagination import paginate, Page
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import schemas
from app.models import SavedJob, Job
from app.repositories.job import JobRepository
from app.repositories.save_job import SavedJobRepository
from exceptions.exceptions import DatabaseException, APIException

logger = logging.getLogger(__name__)


class SavedJobUseCase:
    """SavedJob Use Case Class."""

    def __init__(self, db: Session):
        """Initialize with db and SavedJob Repository."""
        self.db = db
        self.save_job_repository = SavedJobRepository(SavedJob)
        self.job_repository = JobRepository(Job)

    def get_saved_jobs(self) -> Union[Page[schemas.SavedJobOut], JSONResponse]:
        """Get all save_jobs record."""
        try:
            save_jobs = self.save_job_repository.get_all(self.db)

        except DatabaseException as e:
            logger.error(f"Database error occurred while fetching save_jobs: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        return paginate(save_jobs)

    def get_saved_job(self, _id: int) -> Union[schemas.SavedJobOut, JSONResponse]:
        """Get save_job record."""
        try:
            save_job = self.save_job_repository.get(self.db, _id)

            return schemas.SavedJobOut.model_validate(save_job)

        except APIException as e:
            logger.error(f"Database error occurred while fetching save_job: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def get_saved_job_by_user_and_job_id(self, user_id: int, job_id: int) -> Union[schemas.SavedJobOut, JSONResponse]:
        """Get save_job record."""
        try:
            save_job = self.save_job_repository.get_by_user_id_and_job_id(self.db, user_id=user_id, job_id=job_id)

            return schemas.SavedJobOut.model_validate(save_job)

        except APIException as e:
            logger.error(f"Database error occurred while fetching save_job: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def get_saved_jobs_by_user_id(self, user_id: int) -> Union[Page[schemas.SavedJobsOut], JSONResponse]:
        """Get all save_jobs by user id record."""
        try:
            save_jobs = self.save_job_repository.get_all_by_user_id(self.db, user_id=user_id)
            updated_saved_jobs = []
            for save_job in save_jobs:
                job = self.job_repository.get(self.db, _id=save_job.job_id)
                save_job_dict = save_job.__dict__
                save_job_dict.update({'job_title': job.title})
                save_job_dict.update({'job_location': job.location})
                save_job_dict.update({'job_description': job.description})
                save_job_dict.update({'job_salary': job.salary})

                updated_saved_jobs.append(schemas.SavedJobsOut(**save_job_dict))

        except DatabaseException as e:
            logger.error(f"Database error occurred while fetching save_jobs: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        return paginate(updated_saved_jobs)

    def create_saved_job(
        self,
        *,
        obj_in: schemas.SavedJobIn,
    ) -> Union[schemas.SavedJobOut, JSONResponse]:  # schemas.SavedJobOut
        """Create save_job record."""
        try:
            save_job = self.save_job_repository.create(db=self.db, obj_in=obj_in)

            return schemas.SavedJobOut.model_validate(save_job)

        except DatabaseException as e:
            logger.error(f"Database error occurred while creating save_job: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def update_saved_job(
        self,
        _id: int,
        *,
        obj_in: schemas.SavedJobIn,
    ) -> Union[schemas.SavedJobOut, JSONResponse]:
        """Update save_job record."""
        try:
            save_job = self.save_job_repository.get(db=self.db, _id=_id)

            save_job_update = self.save_job_repository.update(
                db=self.db, obj_in=obj_in, db_obj=save_job
            )

            return schemas.SavedJobOut.model_validate(save_job_update)

        except (DatabaseException, APIException) as e:
            logger.error(f"Database error occurred while updating save_job: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def delete_saved_job(self, _id: int) -> Union[schemas.SavedJobOut, JSONResponse]:
        """Delete save_job record."""
        try:
            save_job_update = self.save_job_repository.delete(db=self.db, _id=_id)

            return schemas.SavedJobOut.model_validate(save_job_update)

        except (DatabaseException, APIException) as e:
            logger.error(f"Database error occurred while deleting save_job: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
