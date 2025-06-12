from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, exists
from sqlalchemy import and_

from fastapi import HTTPException, status

# from app.models.estimate import EstimateInfo
from app.models.project_code import ProjectCode
from app.models.enums import ProjectCodeStatusEnum
from app.schemas.ProjectCode import (
    # ProjectCodeRead,
    ProjectCodeCreate,
    ProjectCodeUpdate
)


async def create_project_code(
    db: AsyncSession,
    _created_project_code: ProjectCodeCreate
) -> ProjectCode:
    pc_exists_q = select(
        exists().where(
            and_(
                ProjectCode.project_code == _created_project_code.project_code,
                ProjectCode.period == _created_project_code.period
            )
        )
    )
    result = await db.execute(pc_exists_q)
    existing_pc = result.scalar()

    if existing_pc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 프로젝트 코드 입니다.")

    _ProjectCode = ProjectCode(
        project_code=_created_project_code.project_code,
        period=_created_project_code.period,
        require_scope12=_created_project_code.require_scope12,
        require_waste=_created_project_code.require_waste,
        require_material=_created_project_code.require_material,
        require_transport=_created_project_code.require_transport,
        status_code=_created_project_code.status_code,
        start_date=_created_project_code.start_date,
        end_date=_created_project_code.end_date,
        tartge_end_date=_created_project_code.tartge_end_date,
        memo=_created_project_code.memo
    )

    db.add(_ProjectCode)
    await db.commit()
    await db.refresh(_ProjectCode)
    return _ProjectCode


async def get_project_codes(
        db: AsyncSession,
        id,
        project_code,
) -> list[ProjectCode]:
    project_code_q = select(ProjectCode).options(
        selectinload(ProjectCode.estimates)
    )

    if id:
        project_code_q = project_code_q.where(ProjectCode.id == id)

    if project_code:
        project_code_q = project_code_q.where(ProjectCode.project_code == project_code)
    
    result = await db.execute(project_code_q)
    return result.scalars().all()


async def update_project_code(
        db: AsyncSession,
        project_code_id: int,
        updated_project_code: ProjectCodeUpdate
) -> ProjectCode:
    _ProjectCode = await db.execute(
        select(ProjectCode)
        .where(ProjectCode.id == project_code_id)
        .options(
            selectinload(ProjectCode.estimates)
        )
    )
    existing_pc = _ProjectCode.scalar_one_or_none()
    if not existing_pc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 프로젝트 코드 입니다.")
    
    if existing_pc.status_code != ProjectCodeStatusEnum.NOT_STARTED:
        not_updated_started_project_code_opt = any([
            existing_pc.project_code != updated_project_code.project_code,
            existing_pc.period != updated_project_code.period,
            existing_pc.require_scope12 != updated_project_code.require_scope12,
            existing_pc.require_waste != updated_project_code.require_waste,
            existing_pc.require_material != updated_project_code.require_material,
            existing_pc.require_transport != updated_project_code.require_transport,
            existing_pc.status_code != updated_project_code.status_code and updated_project_code.status_code == ProjectCodeStatusEnum.NOT_STARTED
        ])

        if not_updated_started_project_code_opt:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 시작한 프로젝트 코드 입니다.")
    
    existing_pc.project_code = updated_project_code.project_code
    existing_pc.period = updated_project_code.period
    existing_pc.require_scope12 = updated_project_code.require_scope12
    existing_pc.require_waste = updated_project_code.require_waste
    existing_pc.require_material = updated_project_code.require_material
    existing_pc.require_transport = updated_project_code.require_transport
    existing_pc.status_code = updated_project_code.status_code      
    existing_pc.start_date = updated_project_code.start_date    
    existing_pc.end_date = updated_project_code.end_date
    existing_pc.tartge_end_date = updated_project_code.tartge_end_date
    existing_pc.memo = updated_project_code.memo

    await db.commit()
    await db.refresh(existing_pc)
    return existing_pc


async def delete_project_code(
        db: AsyncSession,
        project_code_id: int
) -> ProjectCode:
    _deleting_pc = await db.execute(
        select(ProjectCode)
        .where(ProjectCode.id == project_code_id)
        .options(
            selectinload(ProjectCode.estimates)
        )
    )
    _deleting_pc = _deleting_pc.scalar_one_or_none()
    
    if not _deleting_pc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 프로젝트 코드 입니다.")
    
    if _deleting_pc.status_code == ProjectCodeStatusEnum.STARTED:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 시작한 프로젝트 코드 입니다.")

    if _deleting_pc.estimates:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="프로젝트 코드에 참여한 기업 및 사업장이 있습니다.")
    
    await db.delete(_deleting_pc)
    await db.commit()
    return HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="프로젝트 코드 삭제 완료")
