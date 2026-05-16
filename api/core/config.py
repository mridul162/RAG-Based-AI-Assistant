"""
config.py

Purpose:
--------
Centralized configuration management for the
Hasanah Mart multilingual RAG system.

Architecture Philosophy:
------------------------
Single source of truth.
Environment-driven configuration.
Deployment-friendly settings.
"""

from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

from pydantic import Field

from pydantic_settings import (
    BaseSettings
)


# ---------------------------------------------------------
# LOAD ENV VARIABLES
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[2]
)

ARTIFACTS_DIR = (
    PROJECT_ROOT / "artifacts"
)

FAISS_DIR = (
    ARTIFACTS_DIR / "faiss"
)


# ---------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------

class Settings(BaseSettings):

    # -------------------------------------------------
    # APPLICATION
    # -------------------------------------------------

    app_name: str = (
        "Hasanah Mart RAG API"
    )

    app_version: str = "1.0.0"

    debug: bool = True

    environment: str = (
        "development"
    )


    # -------------------------------------------------
    # OPENAI
    # -------------------------------------------------

    openai_api_key: str = Field(
        ...,
        alias="OPENAI_API_KEY"
    )

    chat_model: str = (
        "gpt-4.1-mini"
    )

    temperature: float = 0.2


    # -------------------------------------------------
    # EMBEDDING
    # -------------------------------------------------

    embedding_model: str = (
        "text-embedding-3-small"
    )

    embedding_dimension: int = 1024


    # -------------------------------------------------
    # FAISS
    # -------------------------------------------------

    faiss_index_path: str = str(

        FAISS_DIR
        / "sample.index"
    )

    faiss_metadata_path: str = str(

        FAISS_DIR
        / "sample_metadata.json"
    )


    # -------------------------------------------------
    # RETRIEVAL
    # -------------------------------------------------

    default_top_k: int = 5

    max_top_k: int = 10


    # -------------------------------------------------
    # CHUNKING
    # -------------------------------------------------

    chunk_size: int = 500

    chunk_overlap: int = 100


    # -------------------------------------------------
    # PROMPTING
    # -------------------------------------------------

    max_context_chars: int = 4000


    # -------------------------------------------------
    # WHATSAPP
    # -------------------------------------------------

    whatsapp_verify_token: str = Field(
        ...,
        alias="WHATSAPP_VERIFY_TOKEN"
    )

    whatsapp_access_token: str = Field(
        ...,
        alias="WHATSAPP_ACCESS_TOKEN"
    )

    whatsapp_phone_number_id: str = Field(
        ...,
        alias="WHATSAPP_PHONE_NUMBER_ID"
    )

    whatsapp_api_version: str = (
        "v22.0"
    )


    # -------------------------------------------------
    # DATABASE
    # -------------------------------------------------

    database_url: str = Field(
        ...,
        alias="DATABASE_URL"
    )


    # -------------------------------------------------
    # CORS
    # -------------------------------------------------

    allowed_origins: list[str] = [
        "*"
    ]


    # -------------------------------------------------
    # PYDANTIC SETTINGS
    # -------------------------------------------------

    model_config = {

        "env_file": ".env",

        "extra": "ignore",
    }


# ---------------------------------------------------------
# CACHED SETTINGS INSTANCE
# ---------------------------------------------------------

@lru_cache
def get_settings():

    return Settings()


# ---------------------------------------------------------
# GLOBAL SETTINGS
# ---------------------------------------------------------

settings = get_settings()