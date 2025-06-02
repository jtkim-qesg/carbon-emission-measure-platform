# 빌드 단계 (Poetry 및 의존성 설치)
FROM python:3.11-slim AS builder

ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update && apt-get install -y curl gcc libmariadb-dev build-essential \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --no-dev


# 실행 단계 (불필요한 도구 제거된 가벼운 이미지)
FROM python:3.11-slim

WORKDIR /app

# 빌드한 라이브러리 복사
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /opt/poetry /opt/poetry
COPY --from=builder /usr/local/bin/poetry /usr/local/bin/poetry

# 프로젝트 코드 복사
COPY . .

# 포트 오픈
EXPOSE 8000

# 운영 환경에서는 --reload 없이 실행
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


# ✅ 운영 환경 실무 적용 팁
# 멀티 스테이지 빌드:	     최종 이미지 용량 감소, 빌드 도구 분리
# --no-dev 옵션:	        운영용엔 개발용 의존성 제거 (예: mypy, ruff, pytest)
# EXPOSE 8000:	            AWS EC2 보안 그룹에서 8000 포트 열어야 함
# .env.production만 반영:	env_file로 구성, 민감 정보는 AWS Secrets Manager 또는 CI/CD에서 주입