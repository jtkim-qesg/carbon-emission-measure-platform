from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.User import UserCreate

async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

async def create_user(db: AsyncSession, user_create: UserCreate):
    user = User(**user_create.dict())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user