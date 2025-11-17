from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Column, TIMESTAMP, ForeignKey
from datetime import datetime

from Artwork_has_category import artwork_has_category
from . import Base

class Artwork(Base):
    __tablename__ = "artwork"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    artist_id = Column(Integer,ForeignKey("user.id"), nullable=False )
    created_at = Column(TIMESTAMP(timezone=False), default=datetime.now)


    seller = relationship("User", back_populates="artworks")
    listings = relationship("Listing", back_populates="artwork")
    categories = relationship('Category', secondary = artwork_has_category, back_poulates="artwork")


    