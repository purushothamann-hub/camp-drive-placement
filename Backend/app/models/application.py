from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.session import Base

class ApplicationStatus(str, enum.Enum):
    APPLIED = "Applied"
    SHORTLISTED = "Shortlisted"
    SELECTED = "Selected"
    REJECTED = "Rejected"

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.APPLIED)
    applied_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
