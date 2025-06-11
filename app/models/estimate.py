from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLEnum
from app.db.base_class import Base
from .base import BaseMixin, SoftDeleteMixin
from .enums import CycleStatusEnum

class EstimateInfo(Base, BaseMixin):
    __tablename__ = "estimate_info"
    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey("site.id", ondelete="RESTRICT"), nullable=False)
    requested_by_user_id = Column(Integer, ForeignKey("user.id", ondelete="RESTRICT"), nullable=False)

    site = relationship("Site", back_populates="estimate_info")

class EstimateCycle(Base, BaseMixin, SoftDeleteMixin):
    __tablename__ = "estimate_cycle"
    id = Column(Integer, primary_key=True)
    estimate_info_id = Column(Integer, ForeignKey("estimate_info.id", ondelete="RESTRICT"), nullable=False)
    cycle_status = Column(SQLEnum(CycleStatusEnum), nullable=False)

    feedback = relationship("EstimateFeedback", backref="EstimateCycle")
    attachments = relationship("EstimateAttachment", backref="EstimateCycle")

class EstimateFeedback(Base, BaseMixin):
    __tablename__ = "estimate_feedback"
    id = Column(Integer, primary_key=True)
    cycle_id = Column(Integer, ForeignKey("estimate_cycle.id", ondelete="RESTRICT"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="RESTRICT"), nullable=False)
    content = Column(String(1000))
    is_send_mail = Column(Boolean, default=False)
    sent_mail_at = Column(DateTime)


class EstimateResult(Base, BaseMixin):
    __tablename__ = "estimate_result"
    id = Column(Integer, primary_key=True)
    estimate_info_id = Column(Integer, ForeignKey("estimate_info.id", ondelete="RESTRICT"), nullable=False)
    comment = Column(String(500))


class EstimateInfoShare(Base, BaseMixin):
    __tablename__ = "estimate_info_share"
    id = Column(Integer, primary_key=True)
    estimate_info_id = Column(Integer, ForeignKey("estimate_info.id", ondelete="RESTRICT"), nullable=False)
    project_code_id = Column(Integer, ForeignKey("project_code.id", ondelete="RESTRICT"), nullable=False)