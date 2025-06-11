from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Boolean, DateTime
from datetime import datetime, timezone

Base = declarative_base()

class BaseMixin:
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.now(timezone.utc)

    @classmethod
    def get_not_deleted(cls, session):
        return session.query(cls).filter(cls.is_deleted == False)
