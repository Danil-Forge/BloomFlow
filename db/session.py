import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# .env расположен в корне BloomFlow, а этот файл — в BloomFlow/db/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Не задана переменная окружения {name}")
    return value


try:
    db_port = int(required_env("DB_PORT"))
except ValueError as exc:
    raise RuntimeError("DB_PORT должен быть числом") from exc


database_url = URL.create(
    drivername="postgresql+asyncpg",
    username=required_env("DB_USER"),
    password=required_env("DB_PASSWORD"),
    host=required_env("DB_HOST"),
    port=db_port,
    database=required_env("DB_NAME"),
)

engine = create_async_engine(
    database_url,
    echo=False,
    pool_pre_ping=True,
)

SessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
