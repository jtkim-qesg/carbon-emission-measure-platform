from typing import List
from enum import Enum
from pydantic import BaseModel, ConfigDict
from app.schemas.Sites import (
    # ReadSite,
    ReadSiteWithEstimate
)

# 공통 속성
class CompanyBase(BaseModel):
    company_name: str
    company_code: str
    class Config:
        model_config = ConfigDict(from_attributes=True)


# 생성 요청 시 사용
class CreateCompany(CompanyBase):
    pass


# 응답 시 사용
class ReadCompany(CompanyBase):
    id: int

class ReadCompanyWithSites(ReadCompany):
    sites: List[ReadSiteWithEstimate] = []

class UpdateCompany(CompanyBase):
    id: int

    
