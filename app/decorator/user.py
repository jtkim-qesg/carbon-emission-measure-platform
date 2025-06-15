from typing import List
from functools import wraps
from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.user import User
from app.models.enums import UserRoleEnum
from app.dependencies.auth import get_current_user

def require_roles(allowed_roles: List[UserRoleEnum]):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized"
            )
        return current_user
    return Depends(role_checker)

# 추후 변경해야함
# from typing import Callable
# def require_roles(allowed_roles: List[UserRoleEnum]):
#     def decorator(func: Callable):
#         @wraps(func)
#         async def wrapper(
#             *args,
#             request: Request,
#             db: AsyncSession = Depends(get_db),
#             current_user: User = Depends(get_current_user),
#             **kwargs
#         ):
#             if current_user.role not in allowed_roles:
#                 raise HTTPException(
#                     status_code=status.HTTP_403_FORBIDDEN,
#                     detail="접근 권한이 없습니다."
#                 )
#             return await func(*args, request=request, db=db, current_user=current_user, **kwargs)
#         return wrapper
#     return decorator


def check_company_access(param: str = "company_id"):
    def decorator(func):
        @wraps(func)
        async def wrapper(
            *args,
            request: Request,
            db: AsyncSession = Depends(get_db),
            current_user: User = Depends(get_current_user),
            **kwargs
        ):
            company_id = int(request.path_params.get(param) or kwargs.get(param))
            if not company_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Bad Request",
                )
            
            if current_user.role != "SUPER" and current_user.company_id != company_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not belong to this company.",
                )
            return await func(*args, request=request, db=db, current_user=current_user, **kwargs)
        return wrapper
    return decorator