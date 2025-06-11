from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError, ExpiredSignatureError
from app.models.user import User
from app.db.session import get_db
from app.core.security import (
    SECRET_KEY, ALGORITHM,
    create_access_token, create_refresh_token,
    REFRESH_TOKEN_EXPIRE_DAYS
)
from app.handlers.auth import authenticate_user
from app.schemas.auth import Token
from app.schemas.auth import RefreshRequest
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/docs/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    # refresh token DB 저장
    user.refresh_token = refresh_token
    await db.commit()

    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/docs/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    current_user.refresh_token = None
    await db.commit()
    return {"detail": "Logged out successfully"}


@router.post("/refresh", response_model=Token)
async def refresh_token(
    request: RefreshRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        token_type: str = payload.get("type")

        if token_type != "refresh":
            raise HTTPException(status_code=400, detail="Invalid token type")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # DB에서 사용자 조회 및 refresh token 확인
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or user.refresh_token != request.refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token mismatch")

    # 새로운 access token 발급
    new_access_token = create_access_token(data={"sub": user.email})

    # refresh token 갱신 조건: 남은 유효 기간이 3일 미만이면 갱신
    now = datetime.utcnow()
    exp_timestamp = payload.get("exp", 0)
    exp_datetime = datetime.utcfromtimestamp(exp_timestamp)
    refresh_token_days_left = (exp_datetime - now).days

    if refresh_token_days_left < 3:
        new_refresh_token = create_refresh_token(data={"sub": user.email})
        user.refresh_token = new_refresh_token
        await db.commit()
    else:
        new_refresh_token = user.refresh_token  # 기존 거 유지

    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token
    )


