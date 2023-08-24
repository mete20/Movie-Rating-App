from pydantic import BaseModel

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