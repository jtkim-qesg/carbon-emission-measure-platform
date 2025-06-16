from fastapi import APIRouter
from app.api.endpoints.admin import user as admin_user_router
from app.api.endpoints.admin import company as admin_company_router
from app.api.endpoints.admin import sites as admin_sites_router
from app.api.endpoints.admin import project_codes as admin_project_codes_router
from app.api.endpoints.admin import vendor_codes as admin_vendor_codes_router

router = APIRouter()
router.include_router(admin_company_router.router, prefix="/company", tags=["Admin Companies"])
router.include_router(admin_user_router.router, prefix="/users", tags=["Admin Users"])
router.include_router(admin_sites_router.router, prefix="/sites", tags=["Admin Sites"])
router.include_router(admin_project_codes_router.router, prefix="/project_code", tags=["Admin ProjectCodes"])
router.include_router(admin_vendor_codes_router.router, prefix="/vendor_code", tags=["Admin VendorCodes"])
