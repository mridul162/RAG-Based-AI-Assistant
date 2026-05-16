"""
chat.py

Purpose:
--------
Main RAG chat API routes for the
Hasanah Mart multilingual AI assistant.

Responsibilities:
-----------------
- Receive user queries
- Execute RAG pipeline
- Return grounded responses
- Handle API errors
- Provide observability logging

Architecture Philosophy:
------------------------
Thin route layer.
Business logic inside services.
Clean dependency injection.
"""

from fastapi import (

    APIRouter,

    HTTPException,

    Depends,
)

from api.schemas.chat import (

    ChatRequest,

    ChatResponse,

    ErrorResponse,
)

from api.services.rag_service import (
    RAGService
)

from api.dependencies.dependencies import (
    get_rag_service
)

from api.core.logging import (
    get_logger
)


# ---------------------------------------------------------
# LOGGER
# ---------------------------------------------------------

logger = get_logger(__name__)


# ---------------------------------------------------------
# ROUTER
# ---------------------------------------------------------

router = APIRouter(

    prefix="/chat",

    tags=["RAG Chat"],
)


# ---------------------------------------------------------
# CHAT ENDPOINT
# ---------------------------------------------------------

@router.post(

    "/ask",

    response_model=ChatResponse,

    responses={

        500: {
            "model": ErrorResponse
        }
    }
)
def ask_question(

    payload: ChatRequest,

    rag_service: RAGService = Depends(
        get_rag_service
    ),
):
    """
    Execute multilingual RAG query.
    """

    try:

        logger.info(

            f"Incoming chat query: "
            f"{payload.query}"
        )

        # -------------------------------------------------
        # EXECUTE RAG PIPELINE
        # -------------------------------------------------

        response = rag_service.ask(

            query=payload.query,

            top_k=payload.top_k,

            include_sources=(
                payload.include_sources
            ),
        )

        logger.info(
            "RAG response generated successfully."
        )

        return response

    # -----------------------------------------------------
    # ERROR HANDLING
    # -----------------------------------------------------

    except Exception as e:

        logger.exception(

            "Error occurred while "
            "processing chat request."
        )

        raise HTTPException(

            status_code=500,

            detail=(
                "Internal server error."
            ),
        )