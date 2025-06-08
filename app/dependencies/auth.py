from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from app.core.security import decode_token
from app.models.user import User
from app.db.session import get_db  # 세션 의존성 주입


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # 로그인 엔드포인트

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="토큰이 유효하지 않거나 만료되었습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc
    
    user = await db.get(User, int(user_id))
    if user is None:
        raise credentials_exception
    return user

## how to use
# @router.get("/me", response_model=UserOut)
# async def read_users_me(current_user: User = Depends(get_current_user)):
#     return current_user
