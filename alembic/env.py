from pathlib import Path
import os
from logging.config import fileConfig
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from alembic import context

from app.db.base import Base  # Base.metadata
# from app.models import user  # noqa


# ----------------------------
# Load Env
# ----------------------------
load_dotenv(dotenv_path=Path("env/.env"))

env_mode = os.getenv("APP_ENV", "development")  # fallback도 지정
env_file = Path(f"env/.env.{env_mode}")

if env_file.exists():
    load_dotenv(dotenv_path=env_file, override=True)
else:
    raise RuntimeError(f".env file not found for APP_ENV={env_mode} → {env_file}")


# ----------------------------
# Alembic Config
# ----------------------------
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


# ----------------------------
# Migration 실행
# ----------------------------
def run_migrations_online() -> None:
    config.set_main_option("sqlalchemy.url", os.getenv("SYNC_DATABASE_URL"))

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
