from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLEnum
from app.db.base_class import Base
from .base import BaseMixin
from .enums import UserRoleEnum
from datetime import datetime


class User(Base, BaseMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("company.id", ondelete="RESTRICT"), nullable=False)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRoleEnum), nullable=False, default=UserRoleEnum.GENERAL)
    mfa_token = Column(String(255), nullable=True)
    is_verified_mfa = Column(Boolean, default=False)
    refresh_token = Column(String(500), nullable=True)
    last_login_at = Column(DateTime, default=datetime.utcnow)

    company = relationship('Company', back_populates="users")
    user_sites = relationship('UserSite', back_populates="users")

class UserSite(Base, BaseMixin):
    __tablename__ = "user_site"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="RESTRICT"), nullable=False)
    company_id = Column(Integer, ForeignKey("company.id", ondelete="RESTRICT"), nullable=False)

    users = relationship('User', back_populates="user_sites")
