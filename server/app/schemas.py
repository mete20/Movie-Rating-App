from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    class Config:
        from_attributes = True
        

class MovieBase(BaseModel):
    Name: str
    Year: int
    Runtime: int
    Rating: float
    Votes: int
    Revenue: Optional[float]


class MovieCreate(MovieBase):
    pass


class Movie(MovieBase):
    MovieID: int
    class Config:
        from_attributes = True
        

#### UserMovie


class UserMovieCreate(BaseModel):
    user_id: int
    movie_id: int
    rating: int

class UserMovie(UserMovieCreate):
    id: int

    class Config:
        orm_mode = True