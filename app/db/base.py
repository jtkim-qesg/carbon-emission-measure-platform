# 일반적으로 SQLAlchemy ORM 모델을 FastAPI + Alembic 환경에서 자동으로 인식시키기 위한 엔트리포인트 역할
# 즉, Alembic이 테이블 생성을 위해 모든 모델을 "import해서 인지"하게 도와주는 모듈
# Alembic은 자동 마이그레이션을 할 때 env.py에서 아래처럼 Base metadata를 인식

# Alembic이 Base만 가져와서는 어떤 테이블도 모르고 있음이에요.
# 따라서 base.py는 모든 모델을 import해서 SQLAlchemy가 Base.metadata.tables에 다 등록되도록 도와주는 용도

from sqlalchemy.orm import DeclarativeBase

# SQLAlchemy 2.0 방식의 Base 클래스
class Base(DeclarativeBase):
    pass



# 아래는 Alembic autogenerate를 위한 import (참조만 하면 됨)
# 이 라인은 실제로 쓰지 않더라도 메타데이터 등록용이므로 noqa 처리
from app.models import user  # noqa