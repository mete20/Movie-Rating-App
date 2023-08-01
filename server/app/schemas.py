from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    class Config:
        from_attributes = True

        

class MovieBase(BaseModel):
    name: str
    year: int


class MovieCreate(MovieBase):
    pass


class Movie(MovieBase):
    id: int
    class Config:
        from_attributes = True
