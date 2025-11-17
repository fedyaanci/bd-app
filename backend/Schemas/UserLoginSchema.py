from pydantic import BaseModel
from sqlalchemy import Integer, String, Text, Boolean, DateTime, Column
# превращает таблицы sql в питон классы

class UserLoginSchema(BaseModel):
    username: str
    password: str

