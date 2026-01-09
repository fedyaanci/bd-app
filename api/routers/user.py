from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  
from core.database_config import SessionLocal
from models.user import User
from api.schemas.user import UserResponse
from typing import List

router = APIRouter(prefix='/users', tags=['users'])

@router.get('/', response_model=List[UserResponse])
async def get_users():
    try:
        async with SessionLocal() as session:
            stmt = select(User)
            result = await session.execute(stmt)
            
            users = result.scalars().all()
            
            print(f"Найдено {len(users)} пользователей")
            return users
            
    except Exception as e:
        print(f"Ошибка при получении пользователей: {e}")
        import traceback
        traceback.print_exc()
        return {'error': str(e), 'code': '500'}