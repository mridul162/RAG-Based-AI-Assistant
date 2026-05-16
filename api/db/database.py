"""
database.py

Purpose:
--------
Centralized SQLAlchemy database configuration
for the Hasanah Mart multilingual RAG system.

Responsibilities:
-----------------
- Create database engine
- Configure session factory
- Provide declarative base
- Support PostgreSQL deployment
- Support connection pooling

Architecture Philosophy:
------------------------
Single database entrypoint.
Production-friendly configuration.
Simple session management.
"""

from sqlalchemy import (
    create_engine
)

from sqlalchemy.orm import (
    sessionmaker,
    declarative_base,
)

from api.core.config import (
    settings
)

from api.core.logging import (
    get_logger
)


# ---------------------------------------------------------
# LOGGER
# ---------------------------------------------------------

logger = get_logger(__name__)


# ---------------------------------------------------------
# DATABASE ENGINE
# ---------------------------------------------------------

engine = create_engine(

    settings.database_url,

    pool_pre_ping=True,

    pool_size=5,

    max_overflow=10,

    echo=False,
)


# ---------------------------------------------------------
# SESSION FACTORY
# ---------------------------------------------------------

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine,
)


# ---------------------------------------------------------
# DECLARATIVE BASE
# ---------------------------------------------------------

Base = declarative_base()


# ---------------------------------------------------------
# DATABASE DEPENDENCY
# ---------------------------------------------------------

def get_db():
    """
    FastAPI database dependency.
    """

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# ---------------------------------------------------------
# DATABASE TEST
# ---------------------------------------------------------

def test_database_connection():
    """
    Simple database connectivity test.
    """

    try:

        with engine.connect() as connection:

            logger.info(
                "Database connection successful."
            )

            return True

    except Exception as e:

        logger.exception(
            "Database connection failed."
        )

        return False