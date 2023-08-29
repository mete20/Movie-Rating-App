from pydantic import BaseModel, Field

class UserBase(BaseModel):
    email: str = Field(..., description="The email address of the user.", example="user@example.com")

class UserCreate(UserBase):
    role: str = Field(..., description="The role assigned to the user.", example="admin")

class User(UserBase):
    id: int = Field(..., description="The unique ID for the user.", example=101)

    class Config:
        from_attributes = True
