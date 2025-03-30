"""Saved Job Endpoint."""

from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from app import schemas, models
from app.core.security import get_current_active_user
from app.db.session import get_db
from app.use_cases.save_job import SavedJobUseCase

save_job_router = APIRouter()


@save_job_router.get("/save-job", response_model=Page[schemas.SavedJobOut])
def get_save_jobs(
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user),
):
    """Get all save_jobs."""
    save_job_uc = SavedJobUseCase(db=db)

    save_jobs = save_job_uc.get_saved_jobs()

    return save_jobs


@save_job_router.get("/saved-jobs/{user_id}", response_model=Page[schemas.SavedJobsOut])
def get_save_jobs_by_user_id(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user),
):
    """Get all save_jobs."""
    save_job_uc = SavedJobUseCase(db=db)

    save_jobs = save_job_uc.get_saved_jobs_by_user_id(user_id=user_id)

    return save_jobs


# @save_job_router.get("/save-job/{_id}", response_model=schemas.SavedJobOut)
# def get_save_job(
#         _id: int,
#         db: Session = Depends(get_db),
#         current_user: models.User = Depends(get_current_active_user),
# ):
#     """Get save_job by ID."""
#     save_job_uc = SavedJobUseCase(db=db)
#
#     save_job = save_job_uc.get_saved_job(_id=_id)
#
#     return save_job


@save_job_router.get("/save-job/user-job", response_model=schemas.SavedJobOut)
def get_saved_job_user_and_job_id(
        user_id: int = Query(..., description="User ID"),
        job_id: int = Query(..., description="Job ID"),
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user),
):
    """Get save_job by job and user ID."""
    save_job_uc = SavedJobUseCase(db=db)

    save_job = save_job_uc.get_saved_job_by_user_and_job_id(user_id=user_id, job_id=job_id)

    return save_job


@save_job_router.post("/save-job", response_model=schemas.SavedJobOut)
def create(
        obj_in: schemas.SavedJobIn,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user),
):
    """Create save_job."""
    save_job_uc = SavedJobUseCase(db=db)

    save_job = save_job_uc.create_saved_job(obj_in=obj_in)

    return save_job


@save_job_router.put("/save-job", response_model=schemas.SavedJobOut)
def update(
        _id: int,
        obj_in: schemas.SavedJobIn,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user),
):
    """Update save_job by ID."""
    save_job_uc = SavedJobUseCase(db=db)

    save_job = save_job_uc.update_saved_job(obj_in=obj_in, _id=_id)

    return save_job


@save_job_router.delete("/save-job/{_id}", response_model=schemas.SavedJobOut)
def delete(
        _id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user),
):
    """Delete save_job by ID."""
    save_job_uc = SavedJobUseCase(db=db)

    save_job = save_job_uc.delete_saved_job(_id=_id)

    return save_job
