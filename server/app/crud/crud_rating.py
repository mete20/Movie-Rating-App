from sqlalchemy.orm import Session
from app.models import model_rating
from app.schemas import schema_rating
from .crud_movie import get_movie

def create_rating(db: Session, rating: schema_rating.RatingCreate):
    db_rating = model_rating.Rating(**rating.dict())
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
    
    rating = db.query(model_rating.Rating).filter(model_rating.Rating.user_id == user_id, model_rating.Rating.movie_id == movie_id).first()
    
    if (rating is not None):
        return True