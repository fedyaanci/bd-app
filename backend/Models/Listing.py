from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, ForeignKey, Boolean, Column, Identity, Numeric, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime

from . import Base

class Listing(Base):

    __tablename__ = "listing"
    
    id = Column(Integer, primary_key=True, index=True)
    artwork_id= Column(Integer,ForeignKey('artwork.id') ,nullable=False)
    seller_id=Column(Identity, ForeignKey('user.id'), nullable=False)
    price = Column(Numeric(10,2))
    is_sold = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=False), default=datetime.now)
    sold_at = Column(TIMESTAMP(timezone=False), default=datetime.now)


    artwork = relationship("Artwork", back_populates="listings")
    seller = relationship("User", back_populates="listings_sold")
    order = relationship("Order", back_populates="listing", uselist=False)  # один к одному