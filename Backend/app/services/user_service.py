from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
from typing import Optional

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_in: UserCreate) -> User:
    db_user = User(
        email=user_in.email,
        name=user_in.name,
        password_hash=get_password_hash(user_in.password),
        role=user_in.role,
        cgpa=user_in.cgpa,
        department=user_in.department,
        year=user_in.year,
        backlogs=user_in.backlogs or 0
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_resume(db: Session, user_id: int, resume_url: str) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.resume_url = resume_url
        db.commit()
        db.refresh(user)
    return user
