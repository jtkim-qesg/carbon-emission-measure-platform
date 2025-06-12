from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select, exists
from sqlalchemy import or_

from fastapi import HTTPException, status

from app.models.company import Company
from app.schemas.Company import (
    CreateCompany,
    UpdateCompany,
    ReadCompanyWithSites
)

async def create_company(
        db: AsyncSession,
        _creating_company: CreateCompany
) -> Company:
    existed_company = await db.execute(
        select(Company)
        .where(
            or_(
                Company.company_code == _creating_company.company_code,
                Company.company_name == _creating_company.company_name
            )
        )
    )

    existed_company = existed_company.scalar_one_or_none()
    if existed_company:
        return existed_company
    
    _new_Company = Company(
        company_code = _creating_company.company_code,
        company_name = _creating_company.company_name
    )

    db.add(_new_Company)
    await db.commit()
    await db.refresh(_new_Company)
    return _new_Company


async def get_company(db: AsyncSession, company_id, company_name, company_code) -> Company:
    if company_id == None and company_name == None and company_code == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="잘못된 요청입니다.")
    
    _Company_q = select(Company)
    if company_id:
        _Company_q = _Company_q.where(Company.id == company_id)
        
    if company_name:
        _Company_q = _Company_q.where(Company.company_name == company_name)

    if company_code:
        _Company_q = _Company_q.where(Company.company_code == company_code)

    _Company = await db.execute(_Company_q.options(selectinload(Company.sites)))

    _Company = _Company.scalar_one_or_none()
    if not _Company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 기업입니다.")

    return _Company


async def update_company(
    db: AsyncSession,
    updating_company: UpdateCompany
) -> Company:
    _Company = await db.execute(
        select(Company)
        .where(Company.id == updating_company.id)
    )

    _Company = _Company.scalar_one_or_none()
    if not _Company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 기업입니다.")
    
    _Company.company_code = updating_company.company_code
    _Company.company_name = updating_company.company_name

    await db.commit()
    await db.refresh(_Company)
    return _Company

# async def delete_company(
#     db: AsyncSession,
#     deleting_company: ReadCompanyWithSites
# ) -> Company:
#     _Company = await db.execute(
#         select(Company)
#         .where(Company.id == deleting_company.id)
#     )

#     _Company = _Company.scalar_one_or_none()
#     if not _Company:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 기업입니다.")
    
#     if any([deleting_company.sites.estimate_info])
# 기업의 사업장이 평가 받고 있는 프로젝트 코드가 시작됐을 경우, 일반 사용자에 의해 삭제될 수 없도록 lock 걸어야 함.