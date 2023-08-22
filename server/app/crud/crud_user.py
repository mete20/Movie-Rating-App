from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import model_user
from app.schemas import schema_user

def get_user(db: Session, user_id: int):
    return db.query(model_user.User).filter(model_user.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(model_user.User).filter(model_user.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model_user.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schema_user.UserCreate):
    fake_hashed_password = user.password
    db_user = model_user.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user