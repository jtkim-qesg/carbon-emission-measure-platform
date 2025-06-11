from typing import List
from fastapi import Depends, HTTPException, status
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