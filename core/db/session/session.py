from typing import Iterator
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    Session,
    sessionmaker,
)
from core.db.table import SQLModel

from core.config import config


SessionFactory = sessionmaker(
    bind=create_engine(config.DB_URL),
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)


def create_session() -> Iterator[Session]:
    session = SessionFactory()

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@contextmanager
def session_scope() -> Iterator[Session]:
    return create_session()


Base = SQLModel()
