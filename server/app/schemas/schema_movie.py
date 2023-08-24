from pydantic import BaseModel, Field
from typing import Optional

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