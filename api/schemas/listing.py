from pydantic import BaseModel
from datetime import datetime

class ListingCreate(BaseModel):
    artwork_id: int
    price: float

class ListingBase(BaseModel):
    artwork_id: int
    seller_id: int
    price: float
    is_sold: bool

class ListingResponse(ListingBase):
    id: int

    class Config:
        from_attributes = True