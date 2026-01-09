from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .artwork import Artwork
from .user import User
from .category import Category
from .listing import Listing
from .order import Order
from .rating import Rating

