from collections.abc import Generator
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    pass


def _build_engine(database_uri: Optional[str] = None):
    uri = database_uri or settings.SQLALCHEMY_DATABASE_URI
    connect_args = {"check_same_thread": False} if uri.startswith("sqlite") else {}
    return create_engine(uri, echo=False, future=True, connect_args=connect_args)


engine = _build_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


def init_db() -> None:
    # Import models to register them with metadata before create_all
    from app.models import user, category, product, cart, order, address  # noqa: F401

    Base.metadata.create_all(bind=engine)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()