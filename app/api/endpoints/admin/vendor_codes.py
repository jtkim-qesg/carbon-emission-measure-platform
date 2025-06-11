from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.decorator.user import require_roles
from app.db.session import get_db
from app.models.enums import UserRoleEnum
from app.models.user import User
from app.schemas.VendorCode import (
	VendorCodeBase,
	VendorCodeCreate,
	VendorCodeCreatedRead,
	VendorCodeRead,
	VendorCodeUpdate,
	VendorCodeDelete
)

from app.handlers.admin.vendor_code import (
	create_vendor_code,
	read_vendor_codes,
	update_vendor_code,
	delete_vendor_code
)


router = APIRouter()

@router.get("/", response_model=list[VendorCodeRead])
async def read_vendor_code_by_admin(
	id: Optional[int] = Query(None),
    project_code_id: Optional[str] = Query(None),
	vendor_code: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = require_roles([UserRoleEnum.SUPER])
):
	return await read_vendor_codes(db, id, project_code_id, vendor_code)


@router.post("/", response_model=VendorCodeCreatedRead)
async def create_vendor_code_by_admin(
	vendor_code: VendorCodeCreate,
    db: AsyncSession = Depends(get_db),
	current_user: User = require_roles([UserRoleEnum.SUPER])
):
	return await create_vendor_code(db, vendor_code)


@router.patch("/", response_model=VendorCodeRead)
async def update_vender_code_by_admin(
    vendor_code_id: int,
    vendor_code: VendorCodeUpdate,
    db: AsyncSession = Depends(get_db),
	current_user: User = require_roles([UserRoleEnum.SUPER])
):
    return await update_vendor_code(
        db,
        vendor_code_id,
        vendor_code
    )


@router.delete("/", response_model=VendorCodeDelete)
async def delete_vendor_code_by_admin(
	vendor_code_id: int,
    db: AsyncSession = Depends(get_db),
	current_user: User = require_roles([UserRoleEnum.SUPER])
):
	return await delete_vendor_code(db, vendor_code_id)
