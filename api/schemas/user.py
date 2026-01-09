from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    username: str
    is_artist: bool = False
    avatar_url: str | None = None

class UserCreate(UserBase):
    password_hash: str

class UserUpdate(UserBase):
    password_hash: str | None = None

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True