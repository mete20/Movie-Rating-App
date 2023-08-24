from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    


class UserCreate(UserBase):
    role: str


class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True