from sqlalchemy import Integer, String, Column, TIMESTAMP, ForeignKey, Table
from . import Base

artwork_has_category = Table( # чтобы не выделять отдельный класс для создания промежуточной таблицы
    'artwork_has_category', Base.metadata, # имя тб в бд и обьект который    собирает инфо о всех таблицах
    Column('artwork_id', Integer, ForeignKey('artwork.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('category.id'), primary_key=True)
)