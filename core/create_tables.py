import sys
import os
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:3214@localhost:5432/art_db"
engine = create_engine(DATABASE_URL)

from models import Base
from models.artwork import Artwork
from models.user import User
from models.category import Category
from models.listing import Listing
from models.order import Order
from models.rating import Rating

Base.metadata.create_all(bind=engine)
    
