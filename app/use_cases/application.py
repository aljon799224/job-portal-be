"""Application Use Case."""

import logging
from typing import Union

from fastapi_pagination import paginate, Page
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import schemas
from app.models import Application
from app.repositories.application import ApplicationRepository
from exceptions.exceptions import DatabaseException, APIException

logger = logging.getLogger(__name__)


class ApplicationUseCase:
    """Application Use Case Class."""

    def __init__(self, db: Session):
        """Initialize with db and Application Repository."""
        self.db = db
        self.application_repository = ApplicationRepository(Application)

    def get_applications(self) -> Union[Page[schemas.ApplicationOut], JSONResponse]:
        """Get all applications record."""
        try:
            applications = self.application_repository.get_all(self.db)

        except DatabaseException as e:
            logger.error(f"Database error occurred while fetching applications: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        return paginate(applications)

    def get_applications_by_job_id(self, job_id: int) -> Union[Page[schemas.ApplicationOut], JSONResponse]:
        """Get all applications record."""
        try:
            applications = self.application_repository.get_all_by_job_id(self.db, job_id=job_id)

        except DatabaseException as e:
            logger.error(f"Database error occurred while fetching applications: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        return paginate(applications)

    def get_application(self, _id: int) -> Union[schemas.ApplicationOut, JSONResponse]:
        """Get application record."""
        try:
            application = self.application_repository.get(self.db, _id)

            return schemas.ApplicationOut.model_validate(application)

        except APIException as e:
            logger.error(f"Database error occurred while fetching application: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def get_application_by_user_and_job_id(self, user_id: int, job_id: int) -> Union[schemas.ApplicationOut, JSONResponse]:
        """Get application record."""
        try:
            application = self.application_repository.get_by_user_id_and_job_id(self.db, user_id=user_id, job_id=job_id)

            return schemas.ApplicationOut.model_validate(application)

        except APIException as e:
            logger.error(f"Database error occurred while fetching application: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def create_application(
            self,
            *,
            obj_in: schemas.ApplicationIn,
    ) -> Union[schemas.ApplicationOut, JSONResponse]:
        """Create application record."""
        try:
            application = self.application_repository.create(db=self.db, obj_in=obj_in)

            return schemas.ApplicationOut.model_validate(application)

        except DatabaseException as e:
            logger.error(f"Database error occurred while creating application: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def update_application(
            self,
            _id: int,
            *,
            obj_in: schemas.ApplicationIn,
    ) -> Union[schemas.ApplicationOut, JSONResponse]:
        """Update application record."""
        try:
            application = self.application_repository.get(db=self.db, _id=_id)

            application_update = self.application_repository.update(
                db=self.db, obj_in=obj_in, db_obj=application
            )

            return schemas.ApplicationOut.model_validate(application_update)

        except (DatabaseException, APIException) as e:
            logger.error(f"Database error occurred while updating application: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def delete_application(self, _id: int) -> Union[schemas.ApplicationOut, JSONResponse]:
        """Delete application record."""
        try:
            application_update = self.application_repository.delete(db=self.db, _id=_id)

            return schemas.ApplicationOut.model_validate(application_update)

        except (DatabaseException, APIException) as e:
            logger.error(f"Database error occurred while deleting application: {e.detail}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
