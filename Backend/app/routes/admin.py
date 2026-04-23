from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.routes.deps import get_current_active_admin
from app.models.user import User
from app.schemas.job import JobCreate, JobOut
from app.schemas.application import ApplicationOut, ApplicationStatusUpdate
from app.services import job_service, application_service

router = APIRouter()

@router.post("/jobs", response_model=JobOut)
def create_new_job(
    job_in: JobCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_active_admin)
):
    """Create job postings"""
    return job_service.create_job(db, job_in=job_in)

@router.get("/jobs/{job_id}/applicants", response_model=List[ApplicationOut])
def get_job_applicants(
    job_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_active_admin)
):
    """View applicants for a job"""
    applicants = application_service.get_job_applicants(db, job_id=job_id)
    return applicants

@router.patch("/applications/{application_id}/status", response_model=ApplicationOut)
def update_application_status(
    application_id: int,
    status_update: ApplicationStatusUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_active_admin)
):
    """Update application status"""
    return application_service.update_application_status(
        db, application_id=application_id, new_status=status_update.status
    )

@router.get("/applications/all", response_model=List[ApplicationOut])
def get_all_applications(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_active_admin)
):
    """View all applications across all jobs"""
    from app.models.application import Application
    return db.query(Application).all()