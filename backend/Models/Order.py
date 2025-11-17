from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, ForeignKey, Column, TIMESTAMP
from datetime import datetime
from sqlalchemy.orm import relationship
from . import Base

class Order(Base):

    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey('listening.id'),nullable=False)
    buyer_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    purchased_at = Column(TIMESTAMP(timezone=False), default=datetime.now)

    listing = relationship("Listing", foreign_keys='[Listing.id]',back_populates="order")
    buyer = relationship("User", foreign_keys='[User.id]',back_populates="orders")