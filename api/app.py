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
- Initialize shared services
- Configure logging
- Initialize database tables
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

from fastapi import FastAPI

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

from api.routes.whatsapp import (
    router as whatsapp_router
)

# ---------------------------------------------------------
# OPTIONAL DASHBOARD ROUTES
# ---------------------------------------------------------

try:

    from api.routes.dashboard import (
        router as dashboard_router
    )

    DASHBOARD_ENABLED = True

except ImportError:

    DASHBOARD_ENABLED = False


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

    # -------------------------------------------------
    # STARTUP
    # -------------------------------------------------

    logger.info(
        f"Starting "
        f"{settings.app_name} "
        f"v{settings.app_version}"
    )

    # -------------------------------------------------
    # CREATE DATABASE TABLES
    # -------------------------------------------------

    try:

        Base.metadata.create_all(
            bind=engine
        )

        logger.info(
            "Database tables initialized."
        )

    except Exception as e:

        logger.exception(
            "Database initialization failed."
        )

        raise e

    # -------------------------------------------------
    # INITIALIZE SHARED RAG SERVICE
    # -------------------------------------------------

    try:

        app.state.rag_service = (
            RAGService()
        )

        logger.info(
            "RAG service initialized."
        )

    except Exception as e:

        logger.exception(
            "RAG service initialization failed."
        )

        raise e

    # -------------------------------------------------
    # STARTUP COMPLETE
    # -------------------------------------------------

    logger.info(
        "Application startup complete."
    )

    yield

    # -------------------------------------------------
    # SHUTDOWN
    # -------------------------------------------------

    logger.info(
        "Shutting down API."
    )


# ---------------------------------------------------------
# FASTAPI APP
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
# REGISTER ROUTES
# ---------------------------------------------------------

app.include_router(
    chat_router
)

app.include_router(
    whatsapp_router
)

# ---------------------------------------------------------
# OPTIONAL DASHBOARD ROUTES
# ---------------------------------------------------------

if DASHBOARD_ENABLED:

    app.include_router(
        dashboard_router
    )

    logger.info(
        "Dashboard routes enabled."
    )

else:

    logger.warning(
        "Dashboard routes not found."
    )