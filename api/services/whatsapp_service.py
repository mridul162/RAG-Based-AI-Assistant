"""
app.py

Purpose:
--------
Main FastAPI application entrypoint for the
Hasanah Mart multilingual RAG assistant.

Responsibilities:
-----------------
- Initialize FastAPI app
- Configure middleware
- Register API routes
- Initialize database
- Initialize shared services
- Configure logging
- Expose health endpoints

Architecture Philosophy:
------------------------
Thin application layer.
Centralized initialization.
Production-style backend structure.
"""

from contextlib import (
    asynccontextmanager
)

from fastapi import (
    FastAPI
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

from api.core.config import (
    settings
)

# ---------------------------------------------------------
# LOGGING
# ---------------------------------------------------------

from api.core.logging import (

    setup_logging,

    get_logger,
)

# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------

from api.db.database import (
    engine
)

from api.db.models import (
    Base
)

# ---------------------------------------------------------
# SERVICES
# ---------------------------------------------------------

from api.services.rag_service import (
    RAGService
)

# ---------------------------------------------------------
# ROUTES
# ---------------------------------------------------------

from api.routes.chat import (
    router as chat_router
)

from api.routes.dashboard import (
    router as dashboard_router
)


# ---------------------------------------------------------
# SETUP LOGGING
# ---------------------------------------------------------

setup_logging()

logger = get_logger(__name__)


# ---------------------------------------------------------
# APPLICATION LIFESPAN
# ---------------------------------------------------------

@asynccontextmanager
async def lifespan(
    app: FastAPI
):

    # -----------------------------------------------------
    # STARTUP
    # -----------------------------------------------------

    logger.info(

        f"Starting "

        f"{settings.app_name} "

        f"v{settings.app_version}"
    )

    # -----------------------------------------------------
    # CREATE DATABASE TABLES
    # -----------------------------------------------------

    try:

        Base.metadata.create_all(
            bind=engine
        )

        logger.info(
            "Database tables initialized."
        )

    except Exception:

        logger.exception(
            "Database initialization failed."
        )

        raise

    # -----------------------------------------------------
    # INITIALIZE SHARED RAG SERVICE
    # -----------------------------------------------------

    try:

        app.state.rag_service = (
            RAGService()
        )

        logger.info(
            "RAG service initialized successfully."
        )

    except Exception:

        logger.exception(
            "Failed to initialize RAG service."
        )

        raise

    logger.info(
        "Application startup complete."
    )

    yield

    # -----------------------------------------------------
    # SHUTDOWN
    # -----------------------------------------------------

    logger.info(
        "Shutting down API."
    )


# ---------------------------------------------------------
# FASTAPI APPLICATION
# ---------------------------------------------------------

app = FastAPI(

    title=settings.app_name,

    description=(

        "Multilingual RAG-powered AI assistant "

        "for Hasanah Mart organic food business."
    ),

    version=settings.app_version,

    debug=settings.debug,

    lifespan=lifespan,
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(

    CORSMiddleware,

    allow_origins=(
        settings.allowed_origins
    ),

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ---------------------------------------------------------
# ROOT ENDPOINT
# ---------------------------------------------------------

@app.get("/")
def root():

    return {

        "message": (

            f"{settings.app_name} "

            f"is running."
        ),

        "version": (
            settings.app_version
        ),

        "status": "running",
    }


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/health")
def health_check():

    return {

        "status": "healthy",

        "service": (
            settings.app_name
        ),

        "version": (
            settings.app_version
        ),
    }

# ---------------------------------------------------------
# Send WhatsApp Message
# ---------------------------------------------------------

import requests

from api.core.config import settings
from api.core.logging import get_logger

logger = get_logger(__name__)


def send_whatsapp_message(
    to_number: str,
    message: str,
):

    url = (
        f"https://graph.facebook.com/"
        f"{settings.whatsapp_api_version}/"
        f"{settings.whatsapp_phone_number_id}"
        f"/messages"
    )

    headers = {
        "Authorization": (
            f"Bearer "
            f"{settings.whatsapp_access_token}"
        ),

        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",

        "to": to_number,

        "type": "text",

        "text": {
            "body": message
        },
    }

    response = requests.post(

        url=url,

        headers=headers,

        json=payload,

        timeout=30,
    )

    response.raise_for_status()

    logger.info(
        f"WhatsApp message sent "
        f"to {to_number}"
    )

    return response.json()


# ---------------------------------------------------------
# REGISTER ROUTES
# ---------------------------------------------------------

app.include_router(
    chat_router
)

app.include_router(
    dashboard_router
)