from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.db.database import Base

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