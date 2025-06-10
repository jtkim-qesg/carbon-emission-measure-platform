from sqlalchemy import Column, Integer, String, Enum as SQLEnum, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base, BaseMixin
from app.models.enums import UserRoleEnum


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)  # ← 실제 DB에 저장되는 해시값
    username = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRoleEnum), nullable=False, default=UserRoleEnum.GENERAL)
    company_id = Column(Integer, ForeignKey("company.id", ondelete="RESTRICT"), nullable=False)

    # optional fields
    mfa_token = Column(String(255), nullable=True)
    is_verified_mfa = Column(Boolean, default=False)
    refresh_token = Column(String(500), nullable=True)
    last_login_at = Column(DateTime, default=datetime.now)

    # relationship
    company = relationship("Company", back_populates="users")
