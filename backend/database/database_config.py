from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv

load_dotenv() # загрузить данные из .env файла 

DATABASE_URL = os.getenv("DATABASE_URL") # должны поместить туда значение DATABASE_URL(которое в файле)

engine = create_async_engine(DATABASE_URL) #создает асинхронное подключение (async await)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # (фабрика) для созданий сессий бд с предуставнеовленными настройками

Base = declarative_base() # для определения моделейй скл алхимии (автоматически связывает классы с таблицами БД)

