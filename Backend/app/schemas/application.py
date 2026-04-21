from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.application import ApplicationStatus
from app.schemas.user import UserOut
from app.schemas.job import JobOut

class ApplicationBase(BaseModel):
    job_id: int

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus

class ApplicationOut(BaseModel):
    id: int
    student_id: int
    job_id: int
    status: ApplicationStatus
    applied_at: datetime
    
    # Optional detailed fields
    student: Optional[UserOut] = None
    job: Optional[JobOut] = None

    class Config:
        from_attributes = True
