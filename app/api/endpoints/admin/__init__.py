from fastapi import APIRouter
from app.api.endpoints.admin import user as admin_user_router

router = APIRouter()
router.include_router(admin_user_router.router, prefix="/users", tags=["Admin Users"])