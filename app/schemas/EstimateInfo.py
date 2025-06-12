from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from datetime import datetime


# 공통 속성
class EstimatesInfoBase(BaseModel):
    site_id: int
    project_code_id: int
    requested_by_user_id: int
    project_code: str
    class Config:
        model_config = ConfigDict(from_attributes=True)


class ReadEstimatesInfo(EstimatesInfoBase):
    id: int
