from pydantic import BaseModel
from datetime import datetime


class UserLogin(BaseModel):
    username: str
    password: str

class UserBase(BaseModel):
    username: str
    is_artist: bool = False
    avatar_url: str | None = None

class UserCreate(UserBase):
    password: str #(открытый парорль только для входа)

class UserUpdate(UserBase):
    password_hash: str | None = None

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True