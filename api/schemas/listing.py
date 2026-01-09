from pydantic import BaseModel
from datetime import datetime

class ListingBase(BaseModel):
    artwork_id: int
    seller_id: int
    price: float
    is_sold: bool = False

class ListingCreate(ListingBase):
    pass

class ListingUpdate(ListingBase):
    price: float | None = None
    is_sold: bool | None = None

class ListingResponse(ListingBase):
    id: int
    created_at: datetime
    sold_at: datetime | None = None

    class Config:
        from_attributes = True