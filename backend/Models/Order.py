from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Boolean, Column, DECIMAL, DateTime, SmallInteger, TIMESTAMP
from datetime import datetime
from sqlalchemy.orm import relationship
Base = declarative_base()

class Order(Base):

    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, nullable=False)
    buyer_id = Column(Integer, nullable=False)
    purchased_at = Column(TIMESTAMP(timezone=False), default=datetime.now)

    listing = relationship("Listing", back_populates="order")
    buyer = relationship("User", back_populates="orders")