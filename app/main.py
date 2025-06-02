from fastapi import FastAPI
# from app.api.api import api_router
from app.api.endpoints import users
from app.core.config import settings

app = FastAPI(
    title="Carbon Emission Measure Platform",
    version="1.0.0"
)


# 라우터 등록
app.include_router(users.router, prefix="/api/users", tags=["Users"])

