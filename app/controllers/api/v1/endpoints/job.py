"""Job Endpoint."""

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from app import schemas, models
from app.core.security import get_current_active_user
from app.db.session import get_db
from app.use_cases.job import JobUseCase

job_router = APIRouter()


@job_router.get("/job", response_model=Page[schemas.JobOut])
def get_jobs(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get all jobs."""
    job_uc = JobUseCase(db=db)

    jobs = job_uc.get_jobs()

    return jobs


@job_router.get("/job/{_id}", response_model=schemas.JobOut)
def get_job(
    _id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get job by ID."""
    job_uc = JobUseCase(db=db)

    job = job_uc.get_job(_id=_id)

    return job


@job_router.get("/jobs/user/{user_id}", response_model=Page[schemas.JobOut])
def get_job_by_user_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get job by ID."""
    job_uc = JobUseCase(db=db)

    job = job_uc.get_jobs_by_user_id(user_id=user_id)

    return job


@job_router.post("/job", response_model=schemas.JobOut)
def create(
    obj_in: schemas.JobIn,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Create job."""
    job_uc = JobUseCase(db=db)

    job = job_uc.create_job(obj_in=obj_in)

    return job


@job_router.put("/job/{_id}", response_model=schemas.JobOut)
def update(
    _id: int,
    obj_in: schemas.JobIn,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Update job by ID."""
    job_uc = JobUseCase(db=db)

    job = job_uc.update_job(obj_in=obj_in, _id=_id)

    return job


@job_router.delete("/job/{_id}", response_model=schemas.JobOut)
def delete(
    _id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Delete job by ID."""
    job_uc = JobUseCase(db=db)

    job = job_uc.delete_job(_id=_id)

    return job
