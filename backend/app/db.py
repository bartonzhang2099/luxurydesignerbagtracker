"""
Phase 5.5: Database engine & session setup.

Concepts: SQLAlchemy `Engine` (manages a pool of DB connections),
`sessionmaker` (a factory for `Session` objects, each representing a unit
of work / transaction), and the declarative `Base` class that ORM models
inherit from.

`DATABASE_URL` defaults to the Postgres container started by
`docker compose up -d` (see `docker-compose.yml` and `.env.example`).
Tests override this with an in-memory SQLite URL so they don't require
Docker.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/bagtracker"
)

# `echo=True` is useful while learning - it prints every SQL statement
# SQLAlchemy executes. Feel free to flip it on/off.
engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def init_db() -> None:
    """Create all tables defined by models that inherit from `Base`.

    TODO:
    - Import `app.db_models` here (so its `BagORM`/`PricePointORM`
      classes are registered on `Base.metadata` before we create tables -
      Python only registers a class once its module has been imported).
    - Call `Base.metadata.create_all(bind=engine)`.
    """
    raise NotImplementedError
