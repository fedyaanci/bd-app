from pydantic import BaseModel
from datetime import datetime

class ArtworkBase(BaseModel):
    title: str
    image_url: str
    artist_id: int

class ArtworkCreate(ArtworkBase):
    pass

class ArtworkUpdate(ArtworkBase):
    title: str | None = None
    image_url: str | None = None
    artist_id: int | None = None

class ArtworkResponse(ArtworkBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True