# from pydantic import BaseModelfrom pydantic import BaseModel, ConfigDict, EmailStr
from enum import Enum
from pydantic import BaseModel, ConfigDict
from app.models.enums import UserRoleEnum

# 공통 속성
class CompanyBase(BaseModel):
    company_name: str
    company_code: str


# 생성 요청 시 사용
class CompanyCreate(BaseModel):
    company_name: str
    company_code: str


# 응답 시 사용
class CompanyRead(CompanyBase):
    id: int
    company_name: str
    company_code: str

    class Config:
        model_config = ConfigDict(from_attributes=True)
