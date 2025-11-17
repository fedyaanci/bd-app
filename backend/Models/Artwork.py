from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Column, TIMESTAMP, ForeignKey, Table
from datetime import datetime

Base = declarative_base()

class Artwork(Base):
    __tablename__ = "artwork"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    artist_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=False), default=datetime.utcnow)


    seller = relationship("User", back_populates="artworks")
    listings = relationship("Listing", back_populates="artwork")

artwork_has_category = Table(
    'artwork_has_category',
    Base.metadata,
    Column('artwork_id', Integer, ForeignKey('artwork.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('category.id'), primary_key=True)
)

    