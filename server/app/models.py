from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from .database import Base
from typing import Optional

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True)
    hashed_password = Column(String(255), unique=True)
    
    movies = relationship("UserMovie", back_populates="user")
    

class Movie(Base):
    __tablename__ = "movies"

    MovieID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Name = Column(String(255), unique=True)
    Year = Column(Integer)
    Runtime = Column(Integer)
    Rating = Column(Float)
    Votes = Column(Integer)
    Revenue = Column(Float, nullable=True)
    
    ratings = relationship("UserMovie", back_populates="movie")


class UserMovie(Base):
    __tablename__ = "user_movie"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.MovieID'), nullable=False)
    rating = Column(Integer, nullable=False)

    user = relationship("User", back_populates="movies")
    movie = relationship("Movie", back_populates="ratings")