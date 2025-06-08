from sqlalchemy.orm import DeclarativeBase

# ✅ Base는 맨 위에 정의되어야 함
class Base(DeclarativeBase):
    pass