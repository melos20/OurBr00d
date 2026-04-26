from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from tts_benchmark.core import ensure_runtime_directories
from tts_benchmark.core.config import RuntimeConfig


class Base(DeclarativeBase):
    pass


def build_sqlite_url(config: RuntimeConfig) -> str:
    ensure_runtime_directories(config)
    return f"sqlite:///{config.db_path}"


def create_sqlite_engine(config: RuntimeConfig):
    return create_engine(build_sqlite_url(config), future=True)


def create_session_factory(config: RuntimeConfig) -> sessionmaker[Session]:
    engine = create_sqlite_engine(config)
    return sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)


def init_database(config: RuntimeConfig) -> None:
    from tts_benchmark.models import db_models  # noqa: F401

    engine = create_sqlite_engine(config)
    Base.metadata.create_all(bind=engine)
