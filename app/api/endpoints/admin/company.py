from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.dependencies.auth import get_current_user
from app.db.session import get_db

from app.models.company import Company
from app.models.enums import UserRoleEnum
from app.schemas.Company import (
    CreateCompany, ReadCompany
)

# from app.handlers.user import create_user

router = APIRouter()

@router.get("/", response_model=list[ReadCompany])
async def read_user_by_admin(
    company_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    company_q = select(Company)

    if company_id:
        company_q = company_q.where(Company.id == company_id)

    result = await db.execute(company_q)
    company_q = result.scalars().all()
    return company_q


# @router.post("/", response_model=ReadCompany)
# async def create_user_by_admin(
#     user_in: UserCreate,
#     db: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     # 관리자 권한 체크
#     if current_user.role != UserRoleEnum.SUPER:
#         raise HTTPException(status_code=403, detail="SUPER 권한이 필요합니다.")

#     return await create_user(db, user_in)
