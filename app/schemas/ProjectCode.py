from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.models.enums import ProjectCodeStatusEnum
from app.schemas.EstimateInfo import ReadEstimatesInfo

# 공통 속성
class ProjectCodeBase(BaseModel):
    project_code: str
    period: Optional[str]
    require_scope12: bool = True
    require_waste: bool = True
    require_material: bool = True
    require_transport: bool = True
    status_code: ProjectCodeStatusEnum = ProjectCodeStatusEnum.NOT_STARTED
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    tartge_end_date: Optional[datetime]
    memo: Optional[str]
    class Config:
        model_config = ConfigDict(from_attributes=True)

# 생성 요청 시 사용
class ProjectCodeCreate(ProjectCodeBase):
    pass

class ProjectCodeCreatedRead(ProjectCodeCreate):
    id: int

# 응답 시 사용
class ProjectCodeRead(ProjectCodeBase):
    id: int
    estimates: List[ReadEstimatesInfo] = []

# 수정 시 사용
class ProjectCodeUpdate(ProjectCodeBase):
    id: int
    estimates: List[ReadEstimatesInfo] = []

# # 삭제 시 사용
class ProjectCodeDelete(BaseModel):
    pass
