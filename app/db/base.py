# app/db/base.py
from app.db.base_class import Base

# 아래는 Alembic autogenerate를 위한 import (참조만 하면 됨)
# -- enum (필요 시 초기화 가능)
from app.models.enums import UserRoleEnum
from app.models.enums import CycleStatusEnum
from app.models.enums import AttachmentTypeEnum
from app.models.enums import ReviewStatusEnum

# -- attachment 관련 모델
from app.models.attachment import EstimateAttachment
from app.models.attachment import EstimateAttachmentInfo
from app.models.attachment import EstimateAttachmentReview

# -- company 관련 모델
from app.models.company import Company
from app.models.company import Site
from app.models.company import User
from app.models.company import UserSite

# -- estimate 관련 모델
from app.models.estimate import EstimateInfo
from app.models.estimate import EstimateCycle
from app.models.estimate import EstimateFeedback
from app.models.estimate import EstimateResult
from app.models.estimate import EstimateInfoShare

# -- project_code 관련 모델
from app.models.project_code import ProjectCode
from app.models.project_code import VendorCode
from app.models.project_code import ProjectCodeClient

__all__ = [
    "Base",
    # company
    "Company", "Site",  "User", "UserSite",
	# project_code
	"ProjectCode", "VendorCode", "ProjectCodeClient",
    # estimate
    "EstimateInfo", "EstimateCycle", "EstimateResult", "EstimateInfoShare",
    "EstimateFeedback", "EstimateAttachment", "EstimateAttachmentInfo", "EstimateAttachmentReview",
    # enum
    "AttachmentTypeEnum", "CycleStatusEnum", "UserRoleEnum",
]
