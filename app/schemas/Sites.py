# from pydantic import BaseModelfrom enum import Enum
from pydantic import BaseModel, ConfigDict
# from app.models.enums import UserRoleEnum
from app.schemas.EstimateInfo import (
    ReadEstimatesInfo
)

# 공통 속성
class SiteBase(BaseModel):
    company_id: int
    site_name: str
    site_location: str
    class Config:
        model_config = ConfigDict(from_attributes=True)


class CreateSite(SiteBase):
    pass

class ReadUpdateDeleteSite(SiteBase):
    id: int

class ReadSiteWithEstimate(SiteBase):
    id: int
    estimate_info: ReadEstimatesInfo
