"""Application Endpoint."""
import json
import os

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from app import schemas, models
from app.core.config import Settings
from app.core.security import get_current_active_user
from app.db.session import get_db
from app.use_cases.application import ApplicationUseCase
from urllib.parse import unquote

application_router = APIRouter()


@application_router.get("/application", response_model=Page[schemas.ApplicationOut])
def get_applications(
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user),
):
    """Get all applications."""
    application_uc = ApplicationUseCase(db=db)

    applications = application_uc.get_applications()

    return applications


@application_router.get("/application/job/{job_id}", response_model=Page[schemas.ApplicationOut])
def get_applications_by_job_id(
        job_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user),
):
    """Get all applications."""
    application_uc = ApplicationUseCase(db=db)

    applications = application_uc.get_applications_by_job_id(job_id=job_id)

    return applications


@application_router.get("/application/{_id}", response_model=schemas.ApplicationOut)
def get_application(
        _id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user),
):
    """Get application by ID."""
    application_uc = ApplicationUseCase(db=db)

    application = application_uc.get_application(_id=_id)

    return application


@application_router.post("/application/{job_id}", response_model=schemas.ApplicationOut)
async def create(
        job_id: int,
        obj_in: str = Form(...),
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user),
):
    """Create application."""

    application_uc = ApplicationUseCase(db=db)

    # Ensure the directory exists
    os.makedirs(Settings.UPLOAD_DIR, exist_ok=True)  # 🔹 This will create the directory if it doesn't exist

    obj_data = json.loads(obj_in)
    obj_data.update({"job_id": job_id})

    # Generate a unique filename to avoid conflicts
    filename = f"user_{obj_data['user_id']}_{file.filename}"
    file_path = os.path.join(Settings.UPLOAD_DIR, filename)

    obj_data.update({"resume": file_path})

    obj_in_schema = schemas.ApplicationIn(**obj_data)

    # Save the file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    application = application_uc.create_application(obj_in=obj_in_schema)

    return application


@application_router.get("/application/download/{filename}")
async def download_resume(
        filename: str,
        current_user: models.User = Depends(get_current_active_user),
):
    """Download resume file."""
    decoded_filename = unquote(filename)  # Decode URL-encoded filename

    # Ensure we're not adding "resumes" twice
    file_path = os.path.join(Settings.UPLOAD_DIR, decoded_filename)

    print(f"📂 Looking for file: {file_path}")  # Debugging log

    if not os.path.exists(file_path):
        print(f"❌ File NOT FOUND: {file_path}")  # Debugging log
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, filename=decoded_filename, media_type="application/pdf")

@application_router.put("/application", response_model=schemas.ApplicationOut)
def update(
        _id: int,
        obj_in: schemas.ApplicationIn,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user),
):
    """Update application by ID."""
    application_uc = ApplicationUseCase(db=db)

    application = application_uc.update_application(obj_in=obj_in, _id=_id)

    return application


@application_router.delete("/application/{_id}", response_model=schemas.ApplicationOut)
def delete(
        _id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user),
):
    """Delete application by ID."""
    application_uc = ApplicationUseCase(db=db)

    application = application_uc.delete_application(_id=_id)

    return application
