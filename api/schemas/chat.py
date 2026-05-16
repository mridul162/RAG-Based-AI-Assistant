"""
chat.py

Purpose:
--------
Pydantic schemas for multilingual RAG chat API.

Responsibilities:
-----------------
- Validate incoming chat requests
- Standardize API responses
- Structure retrieval source metadata
- Provide consistent error schemas

Architecture Philosophy:
------------------------
Strict validation.
Readable API contracts.
Frontend/dashboard-friendly responses.
"""

from typing import (
    List,
    Optional,
    Any,
)

from pydantic import (
    BaseModel,
    Field,
)


# ---------------------------------------------------------
# CHAT REQUEST
# ---------------------------------------------------------

class ChatRequest(BaseModel):
    """
    Incoming multilingual RAG query.
    """

    query: str = Field(

        ...,

        min_length=1,

        max_length=2000,

        description=(
            "User query for the RAG system."
        ),
    )

    top_k: int = Field(

        default=5,

        ge=1,

        le=10,

        description=(
            "Number of chunks to retrieve."
        ),
    )

    include_sources: bool = Field(

        default=True,

        description=(
            "Include retrieved source chunks."
        ),
    )


# ---------------------------------------------------------
# SOURCE INFO
# ---------------------------------------------------------

class SourceInfo(BaseModel):
    """
    Retrieved chunk metadata.
    """

    chunk_id: str = Field(

        ...,

        description=(
            "Unique chunk identifier."
        ),
    )

    score: float = Field(

        ...,

        description=(
            "Semantic similarity score."
        ),
    )

    metadata: dict[str, Any] = Field(

        ...,

        description=(
            "Chunk metadata."
        ),
    )

    preview: Optional[str] = Field(

        default=None,

        description=(
            "Optional chunk preview."
        ),
    )


# ---------------------------------------------------------
# CHAT RESPONSE
# ---------------------------------------------------------

class ChatResponse(BaseModel):
    """
    Final multilingual RAG response.
    """

    query: str = Field(

        ...,

        description=(
            "Original user query."
        ),
    )

    answer: str = Field(

        ...,

        description=(
            "Generated grounded answer."
        ),
    )

    sources: Optional[
        List[SourceInfo]
    ] = Field(

        default=None,

        description=(
            "Retrieved semantic sources."
        ),
    )


# ---------------------------------------------------------
# ERROR RESPONSE
# ---------------------------------------------------------

class ErrorResponse(BaseModel):
    """
    Standardized API error response.
    """

    error: str = Field(

        ...,

        description=(
            "Primary error message."
        ),
    )

    details: Optional[str] = Field(

        default=None,

        description=(
            "Additional error details."
        ),
    )