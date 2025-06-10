from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

async def create_user(db: AsyncSession, user_create: UserCreate) -> User:
    # 1. 이메일 중복 확인
    result = await db.execute(select(User).where(User.email == user_create.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 등록된 이메일입니다.")


    # 2. 비밀번호 해싱
    hashed_pw = get_password_hash(user_create.password)

    # 3. 사용자 모델 생성 (명시적으로 필드 지정)
    user = User(
        email=user_create.email,
        username=user_create.username,
        hashed_password=hashed_pw,
        role=user_create.role,
        company_id=user_create.company_id,
    )

    # 4. 저장 및 반환
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user