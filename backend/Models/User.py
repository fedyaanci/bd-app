from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Text, Boolean, DateTime, Column, SmallInteger, TIMESTAMP
from sqlalchemy.orm import relationship  
from datetime import datetime

Base = declarative_base()

class User(Base):
    
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_artist = Column(Boolean,default=False)
    avatar_url = Column(String)
    created_at = Column(TIMESTAMP(timezone=False),default=datetime.now)

    artworks = relationship("Artwork", back_populates="seller")  # Художник → его картины
    ratings_given = relationship("Rating", foreign_keys="[Rating.reviewer_id]", back_populates="reviewer")
    ratings_received = relationship("Rating", foreign_keys="[Rating.artist_id]", back_populates="artist")
    orders = relationship("Order", foreign_keys="[Order.buyer_id]", back_populates="buyer")
    listings_sold = relationship("Listing", foreign_keys="[Listing.seller_id]", back_populates="seller")