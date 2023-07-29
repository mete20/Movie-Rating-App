from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

class Movie(Base):
    __tablename__ = "moview"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    score = Column(String)
    is_active = Column(Boolean, default=True)

