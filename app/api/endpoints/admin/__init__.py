from fastapi import APIRouter
from app.api.endpoints.admin import user as admin_user_router
from app.api.endpoints.admin import company as admin_company_router

router = APIRouter()
router.include_router(admin_user_router.router, prefix="/users", tags=["Admin Users"])
router.include_router(admin_company_router.router, prefix="/company", tags=["Admin Companies"])
