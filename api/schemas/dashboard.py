"""
dashboard.py

Purpose:
--------
Pydantic schemas for dashboard APIs of the
Hasanah Mart multilingual RAG assistant.

Responsibilities:
-----------------
- Conversation response serialization
- Dashboard analytics serialization
- ORM compatibility
- Admin/dashboard API contracts

Architecture Philosophy:
------------------------
Clean API responses.
Frontend-ready structure.
Observability-friendly schemas.
"""

from datetime import (
    datetime
)

from typing import (
    Optional,
    Any,
)

from pydantic import (
    BaseModel,
    Field,
)


# ---------------------------------------------------------
# CONVERSATION RESPONSE
# ---------------------------------------------------------

class ConversationResponse(BaseModel):
    """
    Serialized conversation response.
    """

    id: int

    phone_number: Optional[str] = Field(

        default=None,

        description=(
            "WhatsApp user phone number."
        ),
    )

    user_message: str = Field(

        ...,

        description=(
            "Original user query."
        ),
    )

    ai_response: str = Field(

        ...,

        description=(
            "Generated AI response."
        ),
    )

    retrieved_sources: Optional[
        list[dict[str, Any]]
    ] = Field(

        default=None,

        description=(
            "Retrieved semantic sources."
        ),
    )

    query_language: Optional[str] = Field(

        default=None,

        description=(
            "Detected query language."
        ),
    )

    created_at: datetime = Field(

        ...,

        description=(
            "Conversation timestamp."
        ),
    )

    # -----------------------------------------------------
    # ORM MODE
    # -----------------------------------------------------

    class Config:

        from_attributes = True


# ---------------------------------------------------------
# ANALYTICS RESPONSE
# ---------------------------------------------------------

class AnalyticsResponse(BaseModel):
    """
    Dashboard analytics response.
    """

    total_conversations: int = Field(

        ...,

        description=(
            "Total stored conversations."
        ),
    )

    total_users: int = Field(

        ...,

        description=(
            "Unique WhatsApp users."
        ),
    )

    total_messages: int = Field(

        ...,

        description=(
            "Total processed messages."
        ),
    )

    latest_activity: Optional[
        datetime
    ] = Field(

        default=None,

        description=(
            "Latest conversation timestamp."
        ),
    )