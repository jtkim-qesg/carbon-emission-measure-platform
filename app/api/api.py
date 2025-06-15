# 라우터만 정의하는 모듈, 여러 endpoint들을 모아 api_router에 등록
# 즉, 엔드포인트 모듈들의 중앙 허브 역할

from fastapi import APIRouter
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.company import router as user_company_router
from app.api.endpoints.admin import router as admin_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth")
api_router.include_router(admin_router, prefix="/admin")
api_router.include_router(user_company_router, prefix="/companies", tags=["User Company"])
