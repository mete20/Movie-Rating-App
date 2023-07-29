from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    class Config:
        orm_mode = True
        

class MovieBase(BaseModel):
    name: str


class MovieCreate(MovieBase):
    score: str


class Movie(MovieBase):
    id: int
    is_active: bool
    class Config:
        orm_mode = True

