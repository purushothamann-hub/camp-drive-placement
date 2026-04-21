from sqlalchemy.orm import Session
from app.models.job import Job
from app.schemas.job import JobCreate
from typing import List

def create_job(db: Session, job_in: JobCreate) -> Job:
    db_job = Job(
        company_name=job_in.company_name,
        role=job_in.role,
        description=job_in.description,
        min_cgpa=job_in.min_cgpa,
        allowed_departments=job_in.allowed_departments,
        allowed_years=job_in.allowed_years,
        max_backlogs=job_in.max_backlogs,
        deadline=job_in.deadline
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_jobs(db: Session) -> List[Job]:
    return db.query(Job).all()

def get_job_by_id(db: Session, job_id: int) -> Job:
    return db.query(Job).filter(Job.id == job_id).first()
