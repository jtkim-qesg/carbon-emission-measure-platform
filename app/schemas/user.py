from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional, List
from enum import Enum
from datetime import datetime
from app.models.enums import UserRoleEnum

# 공통 속성
class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str
    company_id: int
    role: UserRoleEnum


# 생성 요청 시 사용
class UserCreate(UserBase):
    pass

# 응답 시 사용
class UserRead(UserBase):
    id: int
    last_login_at: Optional[datetime]

    class Config:
        model_config = ConfigDict(from_attributes=True)
