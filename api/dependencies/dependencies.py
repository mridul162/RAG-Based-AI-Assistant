"""
dependencies.py

Purpose:
--------
Shared FastAPI dependency providers for the
Hasanah Mart multilingual RAG assistant.

Responsibilities:
-----------------
- Provide shared RAG service
- Centralize dependency injection
- Simplify route dependencies

Architecture Philosophy:
------------------------
Thin dependency layer.
Shared singleton-style services.
FastAPI-native dependency injection.
"""

from fastapi import (
    Request
)

from api.services.rag_service import (
    RAGService
)


# ---------------------------------------------------------
# RAG SERVICE DEPENDENCY
# ---------------------------------------------------------

def get_rag_service(
    request: Request
) -> RAGService:
    """
    Retrieve shared RAG service instance
    from FastAPI application state.
    """

    return (
        request.app.state.rag_service
    )