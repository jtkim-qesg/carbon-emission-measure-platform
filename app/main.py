# FastAPI 애플리케이션의 진입점, FastAPI 인스턴스를 만들고 라우터들을 등록
# 즉, FastAPI 서버 실행용 엔트리포인트

from fastapi import FastAPI
from app.api.api import api_router
from app.core.config import settings

app = FastAPI(
    title="Carbon Emission Measure Platform",
    version="1.0.0"
)

# 라우터 등록
app.include_router(api_router)

