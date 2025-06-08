from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.User import UserCreate, UserRead
from app.handlers import user as handlers_user
from typing import List

router = APIRouter()

@router.get("/", response_model=List[UserRead])
async def read_users(db: AsyncSession = Depends(get_db)):
    return await handlers_user.get_users(db)


@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await handlers_user.create_user(db, user)
