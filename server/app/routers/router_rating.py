from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_rating, crud_user, crud_movie
from app.schemas import schema_rating
from app.db.database import get_db
from app.authentication.jwt import get_current_user_email

router = APIRouter(
    prefix="/ratings",
    tags=["ratings"],
    dependencies=[Depends(get_current_user_email)],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schema_rating.Rating)
def create_rating(
        rating: schema_rating.RatingCreate, db: Session = Depends(get_db)
        ):
    db_user = crud_user.get_user(db, user_id = rating.user_id)
    db_movie = crud_movie.get_movie(db, rating.movie_id)

    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error code:": 404,
                "error description": "Not Found",
                "message": f"User with ID: '{rating.user_id}' could not be found",
            },
        )
    
    if db_movie is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error code:": 404,
                "error description": "Not Found",
                "message": f"Movie with ID: '{rating.movie_id}' could not be found",
            },
        )
    
    is_rating_exist = crud_rating.is_rating_exist(db, rating.user_id, rating.movie_id)
    
    if is_rating_exist:
        raise HTTPException(
            status_code=400,
            detail={
                "error code:": 400,
                "error description": "Rating already exist",
                "message": f"User with ID: '{rating.user_id}' has voted the movie '{rating.movie_id}' before.",
            },
        )
    return crud_rating.create_rating(db, rating)

