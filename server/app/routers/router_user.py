from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import crud_user
from app.schemas import schema_user
from app.db.database import SessionLocal
from app.main import get_db
from typing import List

router = APIRouter()

@router.post("/", response_model=schema_user.User)
def create_user(user: schema_user.UserCreate, db: Session = Depends(get_db)):
    # ... (same as before)

@router.get("/", response_model=List[schema_user.User])
def read_users(skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    # ... (same as before)

@router.get("/{user_id}", response_model=schema_user.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    # ... (same as before)
