from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from app.models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: UserRole = UserRole.STUDENT

class UserCreate(UserBase):
    password: str
    cgpa: Optional[float] = Field(None, ge=0, le=10)
    department: Optional[str] = None
    year: Optional[int] = None
    backlogs: Optional[int] = Field(0, ge=0)

class UserUpdate(BaseModel):
    name: Optional[str] = None
    cgpa: Optional[float] = Field(None, ge=0, le=10)
    department: Optional[str] = None
    year: Optional[int] = None
    backlogs: Optional[int] = Field(None, ge=0)
    resume_url: Optional[str] = None

class UserOut(UserBase):
    id: int
    cgpa: Optional[float] = None
    department: Optional[str] = None
    year: Optional[int] = None
    backlogs: Optional[int] = None
    resume_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
