from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from sqlalchemy import and_

from fastapi import HTTPException, status

from app.models.company import Sites
from app.schemas.Sites import (
	CreateSite,
	ReadUpdateDeleteSite
)


async def create_site(
	db: AsyncSession,
	_creating_site: CreateSite
) -> Sites:
	existed_site = await db.execute(
		select(Sites)
		.where(
			and_(
				Sites.company_id == _creating_site.company_id,
				Sites.site_name == _creating_site.site_name
			)
		)
	)

	_existed_site = existed_site.scalar_one_or_none()
	if _existed_site:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="이미 등록된 사업장 입니다.")
	
	_new_Site = Sites(
		company_id = _creating_site.company_id,
		site_name = _creating_site.site_name
	)
	
	db.add(_new_Site)
	await db.commit()
	await db.refresh(_new_Site)
	return _new_Site


async def read_sites(
	db: AsyncSession,
	company_id,
	site_id,
	site_name
) -> Sites:
	_Sites_q = select(Sites)
	if site_id:
		_Sites_q = _Sites_q.where(Sites.id == _Sites_q.site_id)

	if site_name:
		_Sites_q = _Sites_q.where(Sites.site_name == _Sites_q.site_name)

	if company_id:
		_Sites_q = _Sites_q.where(Sites.company_id == _Sites_q.company_id)
	
	_Sites = await db.execute(_Sites_q)
	_Sites = _Sites.scalar().all()
	if not _Sites:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 기업입니다.")
	return _Sites


async def update_site(
	db: AsyncSession,
	site_id: int,
	updating_site: ReadUpdateDeleteSite
) -> Sites:
	if site_id != updating_site.id:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="올바르지 못한 요청입니다.")
	
	_Site = await db.execute(
        select(Sites)
        .where(and_(Sites.id == updating_site.id, Sites.company_id == updating_site.company_id))
    )

	_Site = _Site.scalar_one_or_none()
	if not _Site:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 사업장입니다.")
	
	if _Site.name != updating_site.name:
		_Site.name = updating_site.name
	if _Site.location != updating_site.location:
		_Site.location = updating_site.location

	await db.commit()
	await db.refresh(_Site)
	return _Site


# 다음에...
# async def delete_site(
# 	db: AsyncSession,
# 	deleting_site: ReadUpdateDeleteSite
# ) -> Sites:
# 	...