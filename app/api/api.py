# 라우터만 정의하는 모듈, 여러 endpoint들을 모아 api_router에 등록
# 즉, 엔드포인트 모듈들의 중앙 허브 역할

from fastapi import APIRouter
from app.api.endpoints import users

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["Users"])
