from pydantic import BaseModel, Field


class RatingBase(BaseModel):
    user_id: int = Field(
        ..., description="The unique ID of the user giving the rating.", example=12345
        )
    movie_id: int = Field(
        ..., description="The unique ID of the movie being rated.", example=6789
        )
    rating: int = Field(
        ..., description="The rating given by the user for the movie on a scale (e.g., 1-10).", example=8
        )


class RatingCreate(RatingBase):
    pass


class Rating(RatingBase):
    id: int = Field(
        ..., description="The unique ID for this rating entry.", example=101112
        )


    class Config:
        orm_mode = True
