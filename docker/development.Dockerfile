# Python 3.11 기반 경량 이미지 사용
FROM python:3.11-slim

# Poetry 설치를 위한 환경 변수
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false

# 시스템 패키지 설치 및 Poetry 설치
RUN apt-get update && \
    apt-get install -y gcc libmariadb-dev build-essential curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 생성
WORKDIR /app

# Poetry 설정 파일만 복사하고 의존성 설치
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root

# 전체 소스코드 복사
COPY . .

# 개발 서버 실행 (hot reload)
CMD ["sh", "-c", "poetry run uvicorn app.main:app --host 0.0.0.0 --port $APP_PORT --reload"]



# ✨ 주요 포인트 설명
# 항목	설명
# libmariadb-dev	pymysql, MySQL 드라이버 사용 시 C header 필요
# poetry install --no-root	프로젝트 자체는 설치하지 않지만 의존성은 설치
# CMD	--reload 옵션으로 개발 시 코드 변경 자동 반영
# ENV POETRY_VIRTUALENVS_CREATE=false	Docker 환경에서는 가상환경을 따로 만들지 않도록 설정 (컨테이너 자체가 가상환경이기 때문)