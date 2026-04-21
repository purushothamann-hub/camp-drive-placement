from typing import List, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime

class JobBase(BaseModel):
    company_name: str
    role: str
    description: str
    min_cgpa: float = Field(..., ge=0, le=10)
    allowed_departments: List[str]
    allowed_years: List[int]
    max_backlogs: int = Field(..., ge=0)
    deadline: datetime

    @validator("deadline")
    def deadline_must_be_future(cls, v):
        if v.replace(tzinfo=None) <= datetime.now():
            raise ValueError("Deadline must be in the future")
        return v

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    company_name: Optional[str] = None
    role: Optional[str] = None
    description: Optional[str] = None
    min_cgpa: Optional[float] = None
    allowed_departments: Optional[List[str]] = None
    allowed_years: Optional[List[int]] = None
    max_backlogs: Optional[int] = None
    deadline: Optional[datetime] = None

class JobOut(JobBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
