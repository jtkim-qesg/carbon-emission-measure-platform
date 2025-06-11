from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.decorator.user import require_roles
from app.models.user import User
from app.models.enums import UserRoleEnum
from app.schemas.ProjectCode import (
    ProjectCodeRead,
    ProjectCodeCreate,
    ProjectCodeCreatedRead,
    ProjectCodeUpdate,
    ProjectCodeDelete
)
from app.handlers.admin.project_code import (
    get_project_codes,
    create_project_code,
    update_project_code,
    delete_project_code
)
from app.db.session import get_db


router = APIRouter()

@router.get("/", response_model=list[ProjectCodeRead])
async def read_project_code_by_admin(
    id: Optional[int] = Query(None),
    project_code: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = require_roles([UserRoleEnum.SUPER])
):
    return await get_project_codes(db, id, project_code)


@router.post("/", response_model=ProjectCodeCreatedRead)
async def create_project_code_by_admin(
    project_code: ProjectCodeCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_project_code(
        db,
        project_code
    )

@router.patch("/{project_code_id}", response_model=ProjectCodeRead)
async def create_project_code_by_admin(
    project_code_id: int,
    project_code: ProjectCodeUpdate,
    db: AsyncSession = Depends(get_db)
):
    return await update_project_code(
        db,
        project_code_id,
        project_code
    )


@router.delete("/{project_code_id}", response_model=ProjectCodeDelete)
async def delete_project_code_by_admin(
    project_code_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await delete_project_code(
        db,
        project_code_id
    )