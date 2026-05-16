"""
dashboard.py

Purpose:
--------
Dashboard API routes for the Hasanah Mart
multilingual RAG assistant.

Responsibilities:
-----------------
- Fetch conversation history
- Fetch conversation details
- Provide dashboard analytics
- Support admin observability

Architecture Philosophy:
------------------------
Thin route layer.
Repository-driven queries.
Dashboard-ready APIs.
"""

from fastapi import (

    APIRouter,

    Depends,

    HTTPException,
)

from sqlalchemy.orm import (
    Session
)

# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------

from api.db.database import (
    get_db
)

from api.db.repositories.conversation_repository import (

    get_conversations,

    get_conversation_by_id,

    get_dashboard_analytics,
)

# ---------------------------------------------------------
# SCHEMAS
# ---------------------------------------------------------

from api.schemas.dashboard import (

    ConversationResponse,

    AnalyticsResponse,
)

# ---------------------------------------------------------
# LOGGING
# ---------------------------------------------------------

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

    prefix="/dashboard",

    tags=["Dashboard"],
)


# ---------------------------------------------------------
# FETCH CONVERSATIONS
# ---------------------------------------------------------

@router.get(

    "/conversations",

    response_model=list[
        ConversationResponse
    ],
)
def fetch_conversations(

    limit: int = 50,

    db: Session = Depends(get_db),
):
    """
    Fetch recent conversations.
    """

    logger.info(
        "Fetching dashboard conversations."
    )

    return get_conversations(

        db=db,

        limit=limit,
    )


# ---------------------------------------------------------
# FETCH SINGLE CONVERSATION
# ---------------------------------------------------------

@router.get(

    "/conversations/{conversation_id}",

    response_model=ConversationResponse,
)
def fetch_conversation(

    conversation_id: int,

    db: Session = Depends(get_db),
):
    """
    Fetch conversation by ID.
    """

    logger.info(

        f"Fetching conversation "
        f"{conversation_id}"
    )

    conversation = (

        get_conversation_by_id(

            db=db,

            conversation_id=conversation_id,
        )
    )

    if not conversation:

        logger.warning(

            f"Conversation not found: "
            f"{conversation_id}"
        )

        raise HTTPException(

            status_code=404,

            detail=(
                "Conversation not found"
            ),
        )

    return conversation


# ---------------------------------------------------------
# DASHBOARD ANALYTICS
# ---------------------------------------------------------

@router.get(

    "/analytics",

    response_model=AnalyticsResponse,
)
def fetch_dashboard_analytics(

    db: Session = Depends(get_db),
):
    """
    Fetch dashboard analytics.
    """

    logger.info(
        "Fetching dashboard analytics."
    )

    return get_dashboard_analytics(
        db=db
    )