from pydantic import BaseModel, Field
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
    MovieID: Optional[int] = Field(default=None, primary_key=True)    
    class Config:
        from_attributes = True
        

#### Rating


class RatingBase(BaseModel):
    user_id: int
    movie_id: int
    rating: int
    
class RatingCreate(RatingBase):
    pass

class Rating(RatingBase):
    id: int

    class Config:
        orm_mode = True