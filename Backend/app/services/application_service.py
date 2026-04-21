from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException, status
from app.models.application import Application, ApplicationStatus
from app.models.job import Job
from app.models.user import User
from typing import List

def apply_for_job(db: Session, student_id: int, job_id: int) -> Application:
    # 1. Fetch job and student
    job = db.query(Job).filter(Job.id == job_id).first()
    student = db.query(User).filter(User.id == student_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # 2. Check deadline
    if job.deadline < datetime.now():
        raise HTTPException(status_code=400, detail="Deadline has passed")
    
    # 3. Check duplicate application
    existing = db.query(Application).filter(
        Application.student_id == student_id,
        Application.job_id == job_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already applied for this job")
    
    # 4. Eligibility checks
    if student.cgpa < job.min_cgpa:
        raise HTTPException(status_code=400, detail=f"CGPA too low. Required: {job.min_cgpa}")
    
    if student.department not in job.allowed_departments:
        raise HTTPException(status_code=400, detail=f"Department {student.department} not eligible")
    
    if student.year not in job.allowed_years:
        raise HTTPException(status_code=400, detail=f"Year {student.year} not eligible")
    
    if student.backlogs > job.max_backlogs:
        raise HTTPException(status_code=400, detail=f"Too many backlogs. Max allowed: {job.max_backlogs}")
    
    # 5. Check if resume uploaded
    if not student.resume_url:
        raise HTTPException(status_code=400, detail="Please upload your resume first")

    # 6. Create application
    db_application = Application(
        student_id=student_id,
        job_id=job_id,
        status=ApplicationStatus.APPLIED
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

def update_application_status(db: Session, application_id: int, new_status: ApplicationStatus) -> Application:
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    current_status = application.status
    
    # Status transition rules:
    # Applied -> Shortlisted -> Selected/Rejected
    # Applied -> Rejected
    
    valid_transitions = {
        ApplicationStatus.APPLIED: [ApplicationStatus.SHORTLISTED, ApplicationStatus.REJECTED],
        ApplicationStatus.SHORTLISTED: [ApplicationStatus.SELECTED, ApplicationStatus.REJECTED],
        ApplicationStatus.SELECTED: [],
        ApplicationStatus.REJECTED: []
    }
    
    if new_status not in valid_transitions.get(current_status, []):
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid transition from {current_status} to {new_status}"
        )
    
    application.status = new_status
    db.commit()
    db.refresh(application)
    return application

def get_student_applications(db: Session, student_id: int) -> List[Application]:
    return db.query(Application).filter(Application.student_id == student_id).all()

def get_job_applicants(db: Session, job_id: int) -> List[Application]:
    return db.query(Application).filter(Application.job_id == job_id).all()
