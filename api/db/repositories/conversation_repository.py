"""
conversation_repository.py

Purpose:
--------
Database operations for conversation persistence
and dashboard analytics.

Responsibilities:
-----------------
- Save conversations
- Fetch conversations
- Fetch conversation details
- Dashboard analytics
- Retrieval observability support

Architecture Philosophy:
------------------------
Thin repository layer.
Simple CRUD operations.
Analytics-ready structure.
"""

from sqlalchemy.orm import Session

from sqlalchemy import func

from api.db.models import (
    Conversation
)


# ---------------------------------------------------------
# SAVE CONVERSATION
# ---------------------------------------------------------

def save_conversation(
    db: Session,
    phone_number: str | None,
    user_message: str,
    ai_response: str,
    retrieved_sources: list | None = None,
):
    """
    Persist conversation record.
    """

    conversation = Conversation(

        phone_number=phone_number,

        user_message=user_message,

        ai_response=ai_response,

        retrieved_sources=(
            retrieved_sources or []
        ),
    )

    db.add(conversation)

    db.commit()

    db.refresh(conversation)

    return conversation


# ---------------------------------------------------------
# FETCH CONVERSATIONS
# ---------------------------------------------------------

def get_conversations(
    db: Session,
    limit: int = 50,
):
    """
    Fetch recent conversations.
    """

    return (

        db.query(Conversation)

        .order_by(
            Conversation.created_at.desc()
        )

        .limit(limit)

        .all()
    )


# ---------------------------------------------------------
# FETCH CONVERSATION BY ID
# ---------------------------------------------------------

def get_conversation_by_id(
    db: Session,
    conversation_id: int,
):
    """
    Fetch single conversation.
    """

    return (

        db.query(Conversation)

        .filter(
            Conversation.id
            == conversation_id
        )

        .first()
    )


# ---------------------------------------------------------
# FETCH CONVERSATIONS BY PHONE NUMBER
# ---------------------------------------------------------

def get_conversations_by_phone(
    db: Session,
    phone_number: str,
    limit: int = 50,
):
    """
    Fetch conversation history
    for a WhatsApp user.
    """

    return (

        db.query(Conversation)

        .filter(
            Conversation.phone_number
            == phone_number
        )

        .order_by(
            Conversation.created_at.desc()
        )

        .limit(limit)

        .all()
    )


# ---------------------------------------------------------
# DASHBOARD ANALYTICS
# ---------------------------------------------------------

def get_dashboard_analytics(
    db: Session,
):
    """
    Aggregate dashboard analytics.
    """

    total_conversations = (

        db.query(Conversation)

        .count()
    )

    total_users = (

        db.query(

            func.count(

                func.distinct(
                    Conversation.phone_number
                )
            )
        )

        .scalar()
    )

    total_messages = total_conversations

    latest_conversation = (

        db.query(Conversation)

        .order_by(
            Conversation.created_at.desc()
        )

        .first()
    )

    return {

        "total_conversations": (
            total_conversations
        ),

        "total_users": (
            total_users or 0
        ),

        "total_messages": (
            total_messages
        ),

        "latest_activity": (

            latest_conversation.created_at

            if latest_conversation

            else None
        ),
    }