from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship

from Artwork_has_category import artwork_has_category

from . import Base

class Category(Base):

    __tablename__ = "category"
     
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)

    artwork = relationship('Artwork',  secondary=artwork_has_category, back_populates='Category')