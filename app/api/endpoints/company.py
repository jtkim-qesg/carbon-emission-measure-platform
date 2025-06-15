from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.dependencies.auth import get_current_user
from app.db.session import get_db
from app.decorator.user import require_roles, check_company_access
from app.models.company import Company
from app.models.user import User
from app.models.enums import UserRoleEnum
from app.handlers.companies import (
    get_company,
    create_company,
    update_company
)
from app.schemas.Company import (
    CreateCompany, ReadCompany
)

router = APIRouter()

@router.get("/{company_id}", response_model=ReadCompany)
@check_company_access(param="company_id")
async def get_company_overview(
    company_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = require_roles([UserRoleEnum.SUPER, UserRoleEnum.GENERAL])
):
    return await get_company(db, company_id)


@router.patch("/{company_id}", response_model=ReadCompany)
@check_company_access(param="company_id")
async def get_company_overview(
    company_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = require_roles([UserRoleEnum.SUPER, UserRoleEnum.GENERAL])
):
    return await create_company(db, company_id)


# 회원가입시 기업 생성 API은 다른 API에서 생성