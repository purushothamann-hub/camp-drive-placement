from typing import List
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.routes.deps import get_current_active_student
from app.models.user import User
from app.schemas.job import JobOut
from app.schemas.application import ApplicationOut
from app.services import job_service, application_service, user_service
from app.utils.file_upload import save_resume

router = APIRouter()

@router.get("/jobs", response_model=List[JobOut])
def list_available_jobs(
    db: Session = Depends(get_db),
    current_student: User = Depends(get_current_active_student)
):
    """View all available jobs"""
    return job_service.get_jobs(db)

@router.post("/jobs/{job_id}/apply", response_model=ApplicationOut)
def apply_to_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_student: User = Depends(get_current_active_student)
):
    """Apply for a job"""
    return application_service.apply_for_job(db, student_id=current_student.id, job_id=job_id)

@router.get("/applications", response_model=List[ApplicationOut])
def get_my_applications(
    db: Session = Depends(get_db),
    current_student: User = Depends(get_current_active_student)
):
    """Track application status"""
    return application_service.get_student_applications(db, student_id=current_student.id)

@router.post("/upload-resume")
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_student: User = Depends(get_current_active_student)
):
    """Upload resume (PDF only)"""
    file_path = save_resume(file, current_student.id)
    user_service.update_user_resume(db, user_id=current_student.id, resume_url=file_path)
    return {"message": "Resume uploaded successfully", "path": file_path}
