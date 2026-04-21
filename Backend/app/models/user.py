from sqlalchemy import Column, Integer, String, Float, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.session import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    STUDENT = "student"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.STUDENT)
    
    # Student specific fields
    cgpa = Column(Float, nullable=True)
    department = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    backlogs = Column(Integer, default=0)
    resume_url = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    applications = relationship("Application", back_populates="student")
