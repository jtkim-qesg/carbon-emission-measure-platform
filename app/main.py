# FastAPI 애플리케이션의 진입점, FastAPI 인스턴스를 만들고 라우터들을 등록
# 즉, FastAPI 서버 실행용 엔트리포인트

from fastapi import FastAPI
from app.bootstrap.init_seed_user_company import init_seed_user_company
from app.api.api import api_router

app = FastAPI(
    title="Carbon Emission Measure Platform",
    version="1.0.0"
)
 
@app.on_event("startup")
async def startup_event(): 
    await init_seed_user_company()

# 라우터 등록
app.include_router(api_router)

