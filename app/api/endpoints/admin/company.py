from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.dependencies.auth import get_current_user
from app.db.session import get_db
from app.decorator.user import require_roles
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

@router.get("/", response_model=list[ReadCompany])
async def read_user_by_admin(
    company_id: Optional[int] = Query(None),
    company_name: Optional[str] = Query(None),
    company_code: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    return await get_company(db, company_id, company_name, company_code)


@router.post("/", response_model=ReadCompany)
async def create_user_by_admin(
    company_in: CreateCompany,
    db: AsyncSession = Depends(get_db),
    current_user: User = require_roles([UserRoleEnum.SUPER])
):
    return await create_company(db, company_in)


@router.patch("/{company_id}", response_model=ReadCompany)
async def create_user_by_admin(
    company_id: int,
    company_in: ReadCompany,
    db: AsyncSession = Depends(get_db),
    current_user: User = require_roles([UserRoleEnum.SUPER])
):
    return await update_company(db, company_id, company_in)

# @router.delete("/{company_id}", response_model=ReadCompany)
# company delete는 나중에