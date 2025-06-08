from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Boolean, DateTime
from datetime import datetime

Base = declarative_base()

class BaseMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()

    @classmethod
    def get_not_deleted(cls, session):
        return session.query(cls).filter(cls.is_deleted == False)
