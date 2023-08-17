from .jwt import get_current_user_email
from . import crud, models, schemas
from .database import SessionLocal, engine
from typing import List, Annotated
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.auth import auth_app
from app.auth import get_current_user

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="!secret")


app.mount('/auth', auth_app)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail={
                "error code:": 400,
                "error description": "Not Found",
                "message": f"User with email: '{user.email}' already registered.",
            },
        )
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
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


@app.post("/movies/", response_model=schemas.Movie)
def create_movie(movie: schemas.MovieCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_email)):
    db_movie = crud.get_movie_by_name(db, name= movie.Name)
    if db_movie:
        raise HTTPException(
        
            status_code=400,
            detail={
                "error code:": 400,
                "error description": "Movie already exist",
                "message": f"Movie with ID: '{movie.movie_id}' created before.",
            },
        )
    return crud.create_movie(db=db, movie=movie)


@app.get("/movies/", response_model=List[schemas.Movie])
def read_movies(skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    movies = crud.get_movies(db, skip=skip, limit=limit)
    return movies

@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def read_user(movie_id: int, db: Session = Depends(get_db)):
    db_movie = crud.get_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error code:": 404,
                "error description": "Not Found",
                "message": f"Movie with ID: '{movie_id}' could not be found",
            },
        )
    return db_movie


@app.post("/ratings/", response_model=schemas.Rating)
def create_rating(rating: schemas.RatingCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id = rating.user_id)
    db_movie = crud.get_movie(db, rating.movie_id)

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
    
    is_rating_exist = crud.is_rating_exist(db, rating.user_id, rating.movie_id)
    
    if is_rating_exist:
        raise HTTPException(
            status_code=400,
            detail={
                "error code:": 400,
                "error description": "Rating already exist",
                "message": f"User with ID: '{rating.user_id}' has voted the movie '{rating.movie_id}' before.",
            },
        )
    return crud.create_rating(db, rating)



