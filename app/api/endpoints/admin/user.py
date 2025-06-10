from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.schemas.User import UserCreate, UserRead
from app.models.user import User
from app.models.enums import UserRoleEnum
from app.dependencies.auth import get_current_user
from app.db.session import get_db
from app.handlers.user import create_user

router = APIRouter()

@router.get("/", response_model=list[UserRead])
async def read_user_by_admin(
    user_id: Optional[int] = Query(None),
    company_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRoleEnum.SUPER:
        raise HTTPException(status_code=403, detail="SUPER 권한이 필요합니다.")

    user_q = select(User)

    if user_id:
        user_q = user_q.where(User.id == user_id)

    if company_id:
        user_q = user_q.where(User.company_id == company_id)

    result = await db.execute(user_q)
    users = result.scalars().all()
    return users


@router.post("/", response_model=UserRead)
async def create_user_by_admin(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 관리자 권한 체크
    if current_user.role != UserRoleEnum.SUPER:
        raise HTTPException(status_code=403, detail="SUPER 권한이 필요합니다.")

    return await create_user(db, user_in)
