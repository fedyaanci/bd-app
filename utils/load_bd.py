from models.user import User
from core.database_config import SessionLocal

fedya = User(username='fedya20011', is_artist=False, password_hash='fjidgbwsfew', avatar_url='fedya.png')

import asyncio
from sqlalchemy import select
async def LoadDataToTable(obj):
    try:
        async with SessionLocal() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            print('Y')
            return True
    except Exception as e:
        print('N')
        if session:
            await session.rollback()
        return False

async def DownloadUsers():
    try:
        async with SessionLocal() as session:
            result = await session.execute(select(User))
            users = result.scalars().all()
            return users
    except Exception as e:
        print(f"Ошибка при получении пользователей: {e}")
        return None

#asyncio.run(LoadDataToTable(fedya))

async def main():
    users = await DownloadUsers()
    
    if users:
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Is Artist: {user.is_artist}")

asyncio.run(main())

