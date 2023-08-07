from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from .database import Base
from typing import Optional

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True)
    hashed_password = Column(String(255), unique=True)
    
    rating_movies = relationship("Rating", back_populates="user")
    

class Movie(Base):
    __tablename__ = "movie"

    MovieID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Name = Column(String(255), unique=True)
    Year = Column(Integer)
    Runtime = Column(Integer)
    Rating = Column(Float)
    Votes = Column(Integer)
    Revenue = Column(Float, nullable=True)
    
    ratings = relationship("Rating", back_populates="movie")


class Rating(Base):
    __tablename__ = "rating"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movie.MovieID'), nullable=False)
    rating = Column(Integer, nullable=False)

    user = relationship("User", back_populates="rating_movies")
    movie = relationship("Movie", back_populates="ratings")