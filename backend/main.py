from fastapi  import FastAPI
from database.database_config import engine, Base
from routers import auth

app = FastAPI(title="PictureMarket")

app.include_router(auth.router, prefix="/api")


# # import asyncio
## from sqlalchemy import text

# # async def test_connection():
# #     async with engine.connect() as conn:
# #         result = await conn.execute(text("SELECT 1"))
# #         print("✅ База данных подключена успешно")


# # Запуск проверки
# # asyncio.run(test_connection())