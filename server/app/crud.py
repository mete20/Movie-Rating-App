from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas

class DuplicateEntry(Exception):
    pass

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_movie(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.MovieID == movie_id).first()

    
def get_movie_by_name(db: Session, name: str):
    return db.query(models.Movie).filter(models.Movie.Name == name).first()

def get_movies(db: Session, skip: int = 0, limit: int = 200):
    return db.query(models.Movie).offset(skip).limit(limit).all()


def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def create_rating(db: Session, rating: schemas.RatingCreate):
    db_rating = models.Rating(**rating.dict())
    user_id = db_rating.user_id
    movie_id = db_rating.movie_id
    rate = db_rating.rating
    update_movie_rating(db=db, movie_id=movie_id, rate=rate)
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)  
    return db_rating

def update_movie_rating(db: Session, movie_id: int, rate: int):
    movie = get_movie(db, movie_id)
    movie_rate = movie.Rating
    movie_votes= movie.Votes
    total_rating = (movie_rate * movie_votes) + rate
    new_rating = total_rating / (movie_votes + 1)
    movie.Rating = new_rating
    movie.Votes += 1
    db.commit()

def is_rating_exist(db: Session, user_id: int, movie_id: int):
    
    rating = db.query(models.Rating).filter(models.Rating.user_id == user_id, models.Rating.movie_id == movie_id).first()
    
    if (rating is not None):
        return True