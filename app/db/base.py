from sqlalchemy.orm import DeclarativeBase

# SQLAlchemy 2.0 방식의 Base 클래스
class Base(DeclarativeBase):
    pass



# 아래는 Alembic autogenerate를 위한 import (참조만 하면 됨)
# 이 라인은 실제로 쓰지 않더라도 메타데이터 등록용이므로 noqa 처리
from app.models import user  # noqa