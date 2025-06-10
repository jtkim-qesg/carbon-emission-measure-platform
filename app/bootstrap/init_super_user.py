# app/bootstrap/init_super_user.py

from sqlalchemy import select
from app.models.user import User, UserRoleEnum
from app.core.security import get_password_hash
from app.db.session import AsyncSessionLocal  # ✅ async_sessionmaker 기반 세션

async def init_super_user():
    print("init_super_user 실행")
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.email == "super@qesg.co.kr")
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            print("✅ SUPER 유저가 이미 존재합니다.")
            return

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
