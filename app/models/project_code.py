from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.base_class import Base
from .base import BaseMixin

from .enums import ProjectCodeStatusEnum


class ProjectCode(Base, BaseMixin):
    __tablename__ = "project_code"
    id = Column(Integer, primary_key=True)
    project_code = Column(String(255), nullable=False)
    period = Column(String(100), nullable=True)
    require_scope12 = Column(Boolean, default=True)
    require_waste = Column(Boolean, default=True)
    require_material = Column(Boolean, default=True)
    require_transport = Column(Boolean, default=True)
    status_code = Column(SQLEnum(ProjectCodeStatusEnum), nullable=False, default=ProjectCodeStatusEnum.NOT_STARTED)
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    tartge_end_date = Column(DateTime(timezone=True), nullable=True)
    memo = Column(String(750), nullable=True)

    client = relationship("ProjectCodeClient", backref="ProjectCode")

class VendorCode(Base, BaseMixin):
    __tablename__ = "vendor_code"
    id = Column(Integer, primary_key=True)
    project_code_id = Column(Integer, ForeignKey("project_code.id", ondelete="RESTRICT"), nullable=False)
    vendor_code = Column(String(255), nullable=False)
    company_id = Column(Integer, ForeignKey("company.id", ondelete="RESTRICT"), nullable=False)
    used = Column(Boolean, default=True)
    used_at = Column(DateTime(timezone=True), nullable=True)

class ProjectCodeClient(Base, BaseMixin):
    __tablename__ = "project_code_client"
    id = Column(Integer, primary_key=True)
    project_code_id = Column(Integer, ForeignKey("project_code.id", ondelete="RESTRICT"), nullable=False)
    client_id = Column(Integer, ForeignKey("company.id", ondelete="RESTRICT"), nullable=False)

