from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas


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
    movie_id = db_rating.movie_id
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    update_movie_rating(db=db, movie_id=movie_id)
    return db_rating


def update_movie_rating(db: Session, movie_id: int):
    

    # Calculate the average rating
    average_rating = db.query(func.avg(models.Rating.rating)).filter(models.Rating.movie_id == movie_id).scalar()
    # Get the movie record
    movie = db.query(models.Movie).filter(models.Movie.MovieID == movie_id).first()
    # Update the Rating column with the calculated average rating
    # Calculate the new average rating
    new_rating = ((float(average_rating) * (movie.Votes - 1)) + movie.Rating) / movie.Votes
    # Update the Rating column with the calculated new rating
    movie.Rating = new_rating
    movie.Votes += 1
    # Commit the changes to the database
    db.commit()

    return movie
