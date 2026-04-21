from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    description = Column(String, nullable=False)
    min_cgpa = Column(Float, nullable=False)
    allowed_departments = Column(JSON, nullable=False)  # List[str]
    allowed_years = Column(JSON, nullable=False)        # List[int]
    max_backlogs = Column(Integer, nullable=False)
    deadline = Column(DateTime, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    applications = relationship("Application", back_populates="job")
