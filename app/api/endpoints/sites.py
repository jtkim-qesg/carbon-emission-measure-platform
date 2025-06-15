from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.decorator.user import deco_require_roles
from app.decorator.sites import check_user_site
from app.models.enums import UserRoleEnum
from app.schemas.Sites import (
	CreateSite,
	ReadUpdateDeleteSite
)
from app.handlers.admin.sites import (
	create_site,
	read_sites,
	update_site
)
from app.db.session import get_db

router = APIRouter()

@deco_require_roles([UserRoleEnum.SUPER, UserRoleEnum.GENERAL])
@check_user_site()
@router.get("/", response_model=List[ReadUpdateDeleteSite])
async def read_sites_by_user(
	company_id: Optional[int] = Query(None),
	db: AsyncSession = Depends(get_db),
):
	return await read_sites(db, None, None, company_id)


@deco_require_roles([UserRoleEnum.SUPER, UserRoleEnum.GENERAL])
@check_user_site()
@router.post("/", response_model=ReadUpdateDeleteSite)
async def create_site_by_user(
	site: CreateSite,
	db: AsyncSession = Depends(get_db),
):
	return await create_site(db, site)


@deco_require_roles([UserRoleEnum.SUPER, UserRoleEnum.GENERAL])
@check_user_site()
@router.patch("/{site_id}", response_model=ReadUpdateDeleteSite)
async def update_site_by_user(
	site: ReadUpdateDeleteSite,
	site_id: int,
	db: AsyncSession = Depends(get_db),
):
	return await update_site(db, site_id, site)