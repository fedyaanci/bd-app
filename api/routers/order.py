from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.database_config import get_db
from api.schemas.order import OrderCreate, OrderResponse
from models.user import User
from models.order import Order
from models.listing import Listing
from api.utils.auth import get_current_user
router = APIRouter(prefix='/orders', tags=['orders'])

security = HTTPBearer()

@router.post("/create", response_model=OrderResponse)
async def create_order(order: OrderCreate,
                       current_user: User = Depends(get_current_user),
                       db: AsyncSession = Depends(get_db)):
    
    listing = await db.get(Listing, order.listing_id)
    
    if not listing:
        raise HTTPException(404, "Listing not found")
    
    if listing.is_sold:
        raise HTTPException(400, "Listing already sold")
    
    if listing.seller_id == current_user.id:
        raise HTTPException(400, "Cannot buy your own artwork")
    
    new_order = Order(
        listing_id = order.listing_id,
        buyer_id = current_user.id
    )

    listing.is_sold = True

    db.add(new_order)

    await db.commit()
    await db.refresh(new_order)

    return new_order


    
