from sqlalchemy import Integer, String, Boolean, Column, DECIMAL, DateTime, SmallInteger, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship
Base = declarative_base()

class Rating(Base):

    __tablename__ = "rating"

    id = Column(Integer, primary_key=True, index=True)
    artwork_id = Column(Integer, nullable=False)
    reviewer_id = Column(Integer, nullable=False)
    score = Column(SmallInteger)
    created_at = Column(TIMESTAMP(timezone=False), default=datetime.now)

    artist = relationship("User", foreign_keys=[artist_id], back_populates="ratings_received")
    reviewer = relationship("User", foreign_keys=[reviewer_id], back_populates="ratings_given")