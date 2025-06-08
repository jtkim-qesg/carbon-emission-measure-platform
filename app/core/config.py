# FastAPI 프로젝트에서 설정(Configuration) 관련된 모든 정보를 중앙에서 관리하는 역할
#  실무적으로 보면 .env 환경 변수 → Python 설정 객체로 매핑하는 핵심 파일

import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path
from functools import lru_cache

# .env 파일에서 APP_ENV만 먼저 로드
load_dotenv(dotenv_path=Path("env/.env"))


# APP_ENV 값에 따라 해당 환경의 .env.* 파일 추가 로딩
app_env = os.getenv("APP_ENV", "development")
env_file = Path(f"env/.env.{app_env}")

if env_file.exists():
    load_dotenv(dotenv_path=env_file, override=True)

class Settings(BaseSettings):
    APP_NAME: str = "Carbon Emission Platform"
    APP_ENV: str
    APP_PORT: int

    DATABASE_URL: str
    SYNC_DATABASE_URL: str
    
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    # REDIS_URL: str

    class Config:
        # Pydantic도 추적 가능하도록 지정
        env_file = str(env_file)
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
