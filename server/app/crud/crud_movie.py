from sqlalchemy.orm import Session
from app.models import model_movie
from app.schemas import schema_movie

def get_movie(db: Session, movie_id: int):
    return db.query(model_movie.Movie).filter(model_movie.Movie.MovieID == movie_id).first()

    
def get_movie_by_name(db: Session, name: str):
    return db.query(model_movie.Movie).filter(model_movie.Movie.Name == name).first()


def get_movies(db: Session, skip: int = 0, limit: int = 200):
    return db.query(model_movie.Movie).offset(skip).limit(limit).all()


def create_movie(db: Session, movie: schema_movie.MovieCreate):
    db_movie = model_movie.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def delete_movie(db: Session, movie_id: int):
    db_movie = db.query(model_movie.Movie).filter(model_movie.Movie.MovieID == movie_id).first()
    if not db_movie:
        return None
    db.delete(db_movie)
    db.commit()
    return db_movie
