from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_

from fastapi import HTTPException, status

from app.models.project_code import ProjectCode
from app.schemas.ProjectCode import ProjectCodeCreate, ProjectCodeUpdate


async def get_project_codes(
        db: AsyncSession,
        id, project_code
):
    
    project_code_q = select(ProjectCode)

    if id:
        project_code_q = id.where(project_code.id == id)

    if project_code:
        project_code_q = project_code.where(project_code.project_code == project_code)
    
    result = await db.execute(project_code_q).scalars().all()
    return result


async def create_project_code(db: AsyncSession, _created_project_code: ProjectCodeCreate) -> ProjectCode:
    _ProjectCode = await db.execute(
        select(ProjectCode).where(
            and_(
                ProjectCode.project_code == _created_project_code.project_code,
                ProjectCode.period == _created_project_code.period
            )
        )
    )
    existing_ProjectCode = _ProjectCode.scalar_one_or_none()
    if existing_ProjectCode:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 프로젝트 코드 입니다.")
    
    _ProjectCode = ProjectCode(
        project_code = _created_project_code.project_code,
        period = _created_project_code.period,
        require_scope12 = _created_project_code.require_scope12,
        require_waste = _created_project_code.require_waste,
        require_material = _created_project_code.require_material,
        require_transport = _created_project_code.require_transport,
        status_code = _created_project_code.status_code,
        start_date = _created_project_code.start_date,
        end_date = _created_project_code.end_date,
        tartge_end_date = _created_project_code.tartge_end_date,
        memo = _created_project_code.memo
    )

    # 4. 저장 및 반환
    db.add(_ProjectCode)
    await db.commit()
    await db.refresh(_ProjectCode)
    return _ProjectCode


async def update_project_codes(db: AsyncSession, updated_project_code: ProjectCodeUpdate) -> ProjectCode:
    _ProjectCode = await db.execute(
        select(ProjectCode).where(ProjectCode.id == updated_project_code)
    )

    existing_ProjectCode = _ProjectCode.scalar_one_or_none()
    if not existing_ProjectCode:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 프로젝트 코드 입니다.")
    
    _ProjectCode.project_code = updated_project_code.project_code        
    _ProjectCode.period = updated_project_code.period        
    _ProjectCode.require_scope12 = updated_project_code.require_scope12        
    _ProjectCode.require_waste = updated_project_code.require_waste        
    _ProjectCode.require_material = updated_project_code.require_material        
    _ProjectCode.require_transport = updated_project_code.require_transport        
    _ProjectCode.status_code = updated_project_code.status_code        
    _ProjectCode.start_date = updated_project_code.start_date        
    _ProjectCode.end_date = updated_project_code.end_date        
    _ProjectCode.tartge_end_date = updated_project_code.tartge_end_date        
    _ProjectCode.memo = updated_project_code.memo        

    await db.commit()
    await db.refresh(_ProjectCode)
    return _ProjectCode
