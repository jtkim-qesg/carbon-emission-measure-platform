from typing import List, Callable
from functools import wraps
from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists, and_
from app.db.session import get_db
from app.models.user import User, UserSite
from app.models.company import Sites
from app.models.enums import UserRoleEnum
from app.dependencies.auth import get_current_user

def check_user_site():
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            if not request:
                raise RuntimeError("Request 객체가 필요합니다")

            db: AsyncSession = request.app.state.db()
            current_user: User = await get_current_user(request)

            if current_user.role not in [UserRoleEnum.SUPER, UserRoleEnum.GENERAL]:
                raise HTTPException(status_code=403, detail="접근 권한이 없습니다.")

            if current_user.role == UserRoleEnum.GENERAL:
                site_id = request.path_params.get("site_id") or request.query_params.get("site_id")
                if not site_id:
                    raise HTTPException(status_code=400, detail="site_id가 필요합니다.")
                site_id = int(site_id)

                stmt = select(exists().where(
                    and_(
                        Sites.id == site_id,
                        Sites.company_id == current_user.company_id
                    )
                ))
                result = await db.execute(stmt)
                has_authorized = result.scalar()

                if not has_authorized:
                    raise HTTPException(status_code=403, detail="접근 권한이 없습니다.")

            kwargs["db"] = db
            kwargs["current_user"] = current_user
            kwargs["request"] = request

            return await func(*args, **kwargs)
        return wrapper
    return decorator