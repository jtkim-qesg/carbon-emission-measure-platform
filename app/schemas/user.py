from pydantic import BaseModel, ConfigDict, EmailStr
from enum import Enum
from app.models.enums import UserRoleEnum

# 공통 속성
class UserBase(BaseModel):
    email: EmailStr
    password: str
    username: str
    role: UserRoleEnum = UserRoleEnum.GENERAL
    company_id: int


# 생성 요청 시 사용
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str
    role: UserRoleEnum = UserRoleEnum.GENERAL
    company_id: int


# 응답 시 사용
class UserRead(UserBase):
    id: int
    email: EmailStr
    username: str
    role: UserRoleEnum
    company_id: int

    class Config:
        model_config = ConfigDict(from_attributes=True)
