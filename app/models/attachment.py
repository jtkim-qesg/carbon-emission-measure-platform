from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLEnum
from app.db.base_class import Base
from .base import BaseMixin
from .enums import AttachmentTypeEnum, ReviewStatusEnum

class EstimateAttachment(Base, BaseMixin):
    __tablename__ = "estimate_attachment"
    id = Column(Integer, primary_key=True)
    cycle_id = Column(Integer, ForeignKey("estimate_cycle.id", ondelete="RESTRICT"), nullable=False)
    type = Column(SQLEnum(AttachmentTypeEnum), nullable=False)

    review = relationship("EstimateAttachmentReview", backref="EstimateAttachment")
    info = relationship("EstimateAttachmentInfo", backref="EstimateAttachment")

class EstimateAttachmentInfo(Base, BaseMixin):
    __tablename__ = "estimate_attachment_info"
    id = Column(Integer, primary_key=True)
    attachment_id = Column(Integer, ForeignKey("estimate_attachment.id", ondelete="RESTRICT"), nullable=False)
    filename = Column(String(255), nullable=False)
    s3_key = Column(String(255), nullable=False)
    content_type = Column(String(100))
    checksum = Column(String(100))
    version = Column(Integer, default=1)
    is_latest = Column(String(5), default='True')

class EstimateAttachmentReview(Base, BaseMixin):
    __tablename__ = "estimate_attachment_review"
    id = Column(Integer, primary_key=True)
    attachment_id = Column(Integer, ForeignKey("estimate_attachment.id", ondelete="RESTRICT"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("user.id", ondelete="RESTRICT"), nullable=False)
    status = Column(SQLEnum(ReviewStatusEnum), nullable=False)
    comment = Column(String(500))

