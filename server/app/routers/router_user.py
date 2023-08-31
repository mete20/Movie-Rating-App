from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import crud_user
from app.schemas import schema_user
from app.db.database import SessionLocal
from app.db.database import get_db
from app.authentication.jwt import get_current_user_email, is_admin_dep
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user_email)],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schema_user.User)
def create_user(
    user: schema_user.UserCreate, db: Session = Depends(get_db), is_admin: bool = Depends(is_admin_dep)
    ):
    print(user)
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail={
                "error code:": 400,
                "error description": "Not Found",
                "message": f"User with email: '{user.email}' already registered.",
            },
        )
    return crud_user.create_user(db=db, user=user)

@router.get("/", response_model=List[schema_user.User])
def read_users(skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schema_user.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error code:": 404,
                "error description": "Not Found",
                "message": f"User with ID: '{user_id}' not found",
            },
        )
    return db_user

@router.get("/details/")
async def get_user_details(
    current_email: str = Depends(get_current_user_email), db: Session = Depends(get_db)
    ):
    user = crud_user.get_user_by_email(db, current_email)
    if user is not None:
        return {"email": user.email, "user_id": user.id, "role": user.role}  # Add other fields as needed
    else:
        print("Error is here")
        raise HTTPException(status_code=404, detail="User not found")
