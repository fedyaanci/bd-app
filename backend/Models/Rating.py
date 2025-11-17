from sqlalchemy import Integer, ForeignKey, Column, SmallInteger, TIMESTAMP
from datetime import datetime
from sqlalchemy.orm import relationship

from . import Base

class Rating(Base):

    __tablename__ = "rating"

    id = Column(Integer, primary_key=True, index=True)
    artwork_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    reviewer_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    score = Column(SmallInteger)
    created_at = Column(TIMESTAMP(timezone=False), default=datetime.now)

    artist = relationship("User", foreign_keys=['User.id'], back_populates="ratings_received")
    reviewer = relationship("User", foreign_keys=['User.id'], back_populates="ratings_given")