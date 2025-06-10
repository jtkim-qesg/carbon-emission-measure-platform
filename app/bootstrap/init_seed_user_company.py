# app/bootstrap/init_super_user.py

from sqlalchemy import select, and_
from app.models.company import Company
from app.models.user import User
from app.models.enums import UserRoleEnum
from app.core.security import get_password_hash
from app.db.session import AsyncSessionLocal  # ✅ async_sessionmaker 기반 세션

async def init_seed_user_company():
    print("init_seed_user_company 실행")
    async with AsyncSessionLocal() as session:
        seed_company = await session.execute(
            select(Company).where(and_(
                company_name = "(주)퀀티파이드이에스지",
                company_code = "349-86-01679"
            ))
        )
        existing_company = seed_company.scalar_one_or_none()
        if existing_company:
            print("✅ 씨드 컴퍼니가 이미 존재합니다.")
        else:
            seed_company = Company(
                company_name="(주)퀀티파이드이에스지",
                company_code="349-86-01679"
            )
            session.add(seed_company)
            await session.commit()
            await session.refresh(seed_company)

        seed_user = await session.execute(
            select(User).where(User.email == "super@qesg.co.kr")
        )
        existing_user = seed_user.scalar_one_or_none()

        if existing_user:
            print("✅ SUPER 유저가 이미 존재합니다.")
        else:
            super_user = User(
                email="super@qesg.co.kr",
                username="superadmin",
                hashed_password=get_password_hash("supersecure123"),
                role=UserRoleEnum.SUPER,
                company_id=1,  # 존재하는 company_id가 있어야 합니다!
            )

            session.add(super_user)
            await session.commit()
            await session.refresh(super_user)

            print("✅ SUPER 유저 생성 완료.")
