from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from .database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True)
    hashed_password = Column(String(255), unique=True)
    
    ratings = relationship("UserRating", back_populates="user")

class Movie(Base):
    __tablename__ = "movies"

    MovieID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Name = Column(String(255), unique=True)
    Year = Column(Integer)
    Runtime = Column(Integer)
    Rating = Column(Float)
    Votes = Column(Integer)
    Revenue = Column(Float)
    
    ratings = relationship("UserRating", back_populates="movie")

class UserRating(Base):
    __tablename__ = "user_ratings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True) ## It should be the combination of the two foreing keys
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.MovieID'), nullable=False)
    rating = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")
    

