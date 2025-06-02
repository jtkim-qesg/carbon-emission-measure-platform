from pydantic import BaseModel, EmailStr

# 공통 속성
class UserBase(BaseModel):
    email: EmailStr
    name: str
    is_active: bool = True

# 생성 요청 시 사용
class UserCreate(UserBase):
    pass

# 응답 시 사용
class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True  # SQLAlchemy 객체 -> Pydantic 변환 허용
