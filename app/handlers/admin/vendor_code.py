from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, exists
from sqlalchemy import and_, or_

from fastapi import HTTPException, status

from app.models.project_code import VendorCode
from app.models.company import Company
from app.models.enums import ProjectCodeStatusEnum
from app.schemas.VendorCode import (
	VendorCodeBase,
	VendorCodeCreate,
	VendorCodeCreatedRead,
	VendorCodeRead,
	VendorCodeUpdate,
	VendorCodeDelete
)

async def create_vendor_code(
	db: AsyncSession,
	_created_vendor_code: VendorCodeCreate
) -> VendorCode:
	vc_exists_q = select(
        exists().where(
            and_(
                VendorCode.project_code_id == _created_vendor_code.project_code_id,
                VendorCode.vendor_code == _created_vendor_code.vendor_code
            )
        )
    )
	result = await db.execute(vc_exists_q)
	existing_vc = result.scalar()

	if existing_vc:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 벤더코드 입니다.")
	
	_VendorCode = VendorCode(
		project_code_id = _created_vendor_code.project_code_id,
		vendor_code = _created_vendor_code.vendor_code,
		company_id = _created_vendor_code.company_id,
		used = _created_vendor_code.used,
		used_at = _created_vendor_code.used_at
	)

	db.add(_VendorCode)
	await db.commit()
	await db.refresh(_VendorCode)
	return _VendorCode


async def read_vendor_codes(
	db: AsyncSession,
    id,
	project_code_id,
    vendor_code,
) -> list[VendorCode]:
	vendor_code_q = select(VendorCode).options(
        selectinload(VendorCode.company),
		selectinload(VendorCode.project_code)
    )

	if id:
		vendor_code_q = vendor_code_q.where(VendorCode.id == id)

	if project_code_id:
		vendor_code_q = vendor_code_q.where(VendorCode.project_code_id == project_code_id)
	
	if vendor_code:
		vendor_code_q = vendor_code_q.where(VendorCode.vendor_code == vendor_code)
	
	result = await db.execute(vendor_code_q)
	return result.scalars().all()


async def update_vendor_code(
	db: AsyncSession,
	vc_id: int,
	updating_vc: VendorCodeUpdate
) -> VendorCode:
	_VendorCode = await db.execute(
        select(VendorCode)
        .where(VendorCode.id == vc_id)
        .options(
            selectinload(VendorCode.project_code),
			selectinload(VendorCode.company)
        )
    )

	existing_vc = _VendorCode.scalar_one_or_none()
	if not existing_vc:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 벤더코드 입니다.")
	
	if existing_vc.used and (
		any([
			existing_vc.project_code_id != updating_vc.project_code_id,
			existing_vc.company_id != updating_vc.company_id
		])
	):
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 사용된 벤더코드 입니다.")
	
	existing_vc.project_code_id = updating_vc.project_code_id
	existing_vc.vendor_code = updating_vc.vendor_code
	existing_vc.company_id = updating_vc.company_id
	existing_vc.used = updating_vc.used
	existing_vc.used_at = updating_vc.used_at

	await db.commit()
	await db.refresh(existing_vc)
	return existing_vc


async def delete_vendor_code(
	db: AsyncSession,
	vc_id: int
) -> VendorCode:
	_deleting_vc = await db.execute(
        select(VendorCode)
        .where(VendorCode.id == vc_id)
        .options(
            selectinload(VendorCode.project_code),
			selectinload(VendorCode.company)
        )
    )
	
	_deleting_vc = _deleting_vc.scalar_one_or_none()
	if not _deleting_vc:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 벤더더젝트 코드 입니다.")
	
	if _deleting_vc.used and all([
		_deleting_vc.project_code_id, _deleting_vc.company_id,
		_deleting_vc.project_code.status_code != ProjectCodeStatusEnum.NOT_STARTED
	]):
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 사용된 벤더코드 입니다.")
	
	await db.delete(_deleting_vc)
	await db.commit()
	return HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="벤더코드 삭제 완료")