"""
models.py

Purpose:
--------
SQLAlchemy ORM models for the Hasanah Mart
multilingual RAG assistant.

Responsibilities:
-----------------
- Conversation persistence
- Retrieval observability
- Dashboard analytics support
- WhatsApp interaction storage

Architecture Philosophy:
------------------------
Simple relational schema.
Analytics-ready structure.
Future extensibility.
"""

from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    JSON,
)

from api.db.database import (
    Base
)


# ---------------------------------------------------------
# CONVERSATION MODEL
# ---------------------------------------------------------

class Conversation(Base):

    __tablename__ = "conversations"

    # -------------------------------------------------
    # PRIMARY KEY
    # -------------------------------------------------

    id = Column(

        Integer,

        primary_key=True,

        index=True,
    )

    # -------------------------------------------------
    # WHATSAPP USER
    # -------------------------------------------------

    phone_number = Column(

        String,

        nullable=True,

        index=True,
    )

    # -------------------------------------------------
    # USER QUERY
    # -------------------------------------------------

    user_message = Column(

        Text,

        nullable=False,
    )

    # -------------------------------------------------
    # AI RESPONSE
    # -------------------------------------------------

    ai_response = Column(

        Text,

        nullable=False,
    )

    # -------------------------------------------------
    # RETRIEVAL SOURCES
    # -------------------------------------------------

    retrieved_sources = Column(

        JSON,

        nullable=True,
    )

    # -------------------------------------------------
    # QUERY LANGUAGE
    # -------------------------------------------------

    query_language = Column(

        String,

        nullable=True,
    )

    # -------------------------------------------------
    # CREATED TIME
    # -------------------------------------------------

    created_at = Column(

        DateTime,

        default=datetime.utcnow,

        nullable=False,
    )