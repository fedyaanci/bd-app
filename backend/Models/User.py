from sqlalchemy import Integer, String,  Boolean,  Column, TIMESTAMP
from sqlalchemy.orm import relationship  
from datetime import datetime

from . import Base

class User(Base):
    
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_artist = Column(Boolean,default=False)
    avatar_url = Column(String)
    created_at = Column(TIMESTAMP(timezone=False),default=datetime.now)

    artworks = relationship("Artwork", back_populates="seller")

    ratings_given = relationship("Rating", foreign_keys="[Rating.reviewer_id]", back_populates="reviewer")

    ratings_received = relationship("Rating", foreign_keys="[Rating.artist_id]", back_populates="artist")

    orders = relationship("Order", foreign_keys="[Order.buyer_id]", back_populates="buyer")

    listings_sold = relationship("Listing", foreign_keys="[Listing.seller_id]", back_populates="seller")


    # foreign key нужно добавлять со стороны многих в связи 1:n : ForeignKey - указывает на какую таблицу и колонку ссылаемся
    # а со стороны одного нужно добавлять relationship (создает связь в питоне) а затем надо добавить обратную связь тоже realtionship
    # в rekationship - 1 аргумент это класс а в foreign key атрибут - таблица 
    #post:
    # user_id = Column(Integer, ForeignKey('users.id'))

    #relationship('class', back_populates='table')

    #back_populates содержит имя свойства (не объект), которое указывает на обратный relationship в другом классе.

    #foreign_keys='[класс.поле]' 