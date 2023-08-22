from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.db.database import Base

class Rating(Base):
    __tablename__ = "rating"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movie.MovieID'), nullable=False)
    rating = Column(Integer, nullable=False)

    user = relationship("User", back_populates="rating_movies")
    movie = relationship("Movie", back_populates="ratings")