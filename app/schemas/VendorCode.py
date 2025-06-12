from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from datetime import datetime

# from app.models.enums import ProjectCodeStatusEnum
from app.schemas.ProjectCode import ProjectCodeCreatedRead
from app.schemas.Company import CompanyRead

# 공통 속성
class VendorCodeBase(BaseModel):
	project_code_id: Optional[int] = None
	vendor_code: str
	company_id: Optional[int] = None
	used: bool = False
	used_at: Optional[datetime] = None
	
	class Config:
		model_config = ConfigDict(from_attributes=True)

# 생성 요청 시 사용
class VendorCodeCreate(VendorCodeBase):
    pass

class VendorCodeCreatedRead(VendorCodeCreate):
    id: int

# 응답 시 사용
class VendorCodeRead(VendorCodeBase):
    id: int
    company: CompanyRead
    project_code: ProjectCodeCreatedRead

# 수정 시 사용
class VendorCodeUpdate(VendorCodeBase):
    id: int
    company: CompanyRead
    project_code: ProjectCodeCreatedRead

# # 삭제 시 사용
class VendorCodeDelete(BaseModel):
    pass
