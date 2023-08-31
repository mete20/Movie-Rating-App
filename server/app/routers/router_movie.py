from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_movie
from app.schemas import schema_movie
from app.db.database import get_db
from typing import List
from app.authentication.jwt import is_admin_dep

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schema_movie.Movie)
def create_movie(movie: schema_movie.MovieCreate, db: Session = Depends(get_db), is_admin: bool = Depends(is_admin_dep)):
    db_movie = crud_movie.get_movie_by_name(db, name= movie.Name)
    if db_movie:
        raise HTTPException(
            status_code=400,
            detail={
                "error code:": 400,
                "error description": "Movie already exist",
                "message": f"Movie with Name: '{movie.Name}' created before.",
            },
        )
    return crud_movie.create_movie(db=db, movie=movie)


@router.get("/", response_model=List[schema_movie.Movie])
def read_movies(skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    movies = crud_movie.get_movies(db, skip=skip, limit=limit)
    return movies


@router.get("/{movie_id}", response_model=schema_movie.Movie)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = crud_movie.get_movie(db, movie_id=movie_id)
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


@router.delete("/{movie_id}", response_model=schema_movie.Movie)
def delete_movie(movie_id: int, db: Session = Depends(get_db), is_admin: bool = Depends(is_admin_dep)):
    db_movie = crud_movie.delete_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error code": 404,
                "error description": "Not Found",
                "message": f"Movie with ID: '{movie_id}' could not be found",
            },
        )
    return db_movie