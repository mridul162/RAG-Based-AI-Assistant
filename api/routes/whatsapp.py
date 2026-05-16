"""
whatsapp.py

Purpose:
--------
WhatsApp Cloud API webhook routes for the
Hasanah Mart multilingual RAG assistant.

Responsibilities:
-----------------
- Webhook verification
- Receive incoming WhatsApp messages
- Execute RAG pipeline
- Send WhatsApp replies
- Persist conversations
- Log webhook events

Architecture Philosophy:
------------------------
Thin route layer.
Shared RAG service usage.
Production-style webhook handling.
"""

from fastapi import (

    APIRouter,

    Request,

    Depends,
)

from fastapi.responses import (
    PlainTextResponse
)

from sqlalchemy.orm import (
    Session
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
    get_logger
)

# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------

from api.db.database import (
    get_db
)

from api.db.repositories.conversation_repository import (

    save_conversation
)

# ---------------------------------------------------------
# WHATSAPP SERVICE
# ---------------------------------------------------------

from api.services.whatsapp_service import (

    send_whatsapp_message
)


# ---------------------------------------------------------
# LOGGER
# ---------------------------------------------------------

logger = get_logger(__name__)


# ---------------------------------------------------------
# ROUTER
# ---------------------------------------------------------

router = APIRouter(

    prefix="/webhooks/whatsapp",

    tags=["WhatsApp"],
)


# ---------------------------------------------------------
# WEBHOOK VERIFICATION
# ---------------------------------------------------------

@router.get("")
async def verify_webhook(
    request: Request
):
    """
    Verify Meta WhatsApp webhook.
    """

    hub_mode = request.query_params.get(
        "hub.mode"
    )

    hub_verify_token = (

        request.query_params.get(
            "hub.verify_token"
        )
    )

    hub_challenge = (

        request.query_params.get(
            "hub.challenge"
        )
    )

    if (

        hub_mode == "subscribe"

        and

        hub_verify_token
        == settings.whatsapp_verify_token
    ):

        logger.info(
            "WhatsApp webhook verified."
        )

        return PlainTextResponse(

            content=hub_challenge,

            status_code=200,
        )

    logger.warning(
        "WhatsApp webhook verification failed."
    )

    return PlainTextResponse(

        content="Verification failed",

        status_code=403,
    )


# ---------------------------------------------------------
# RECEIVE WHATSAPP EVENTS
# ---------------------------------------------------------

@router.post("")
async def receive_whatsapp_message(

    request: Request,

    db: Session = Depends(get_db),
):
    """
    Receive incoming WhatsApp webhook events.
    """

    payload = await request.json()

    logger.info(
        "Incoming WhatsApp webhook received."
    )

    try:

        # -------------------------------------------------
        # EXTRACT WEBHOOK VALUE
        # -------------------------------------------------

        value = (

            payload["entry"][0]

            ["changes"][0]

            ["value"]
        )

        # -------------------------------------------------
        # IGNORE NON-MESSAGE EVENTS
        # -------------------------------------------------

        if "messages" not in value:

            logger.info(
                "Ignoring non-message webhook."
            )

            return {
                "status": "ignored"
            }

        # -------------------------------------------------
        # EXTRACT MESSAGE
        # -------------------------------------------------

        message = value["messages"][0]

        sender_number = (
            message["from"]
        )

        message_text = (

            message["text"]["body"]
        )

        logger.info(

            f"Incoming message from "
            f"{sender_number}: "
            f"{message_text}"
        )

        # -------------------------------------------------
        # GET SHARED RAG SERVICE
        # -------------------------------------------------

        rag_service = (
            request.app.state.rag_service
        )

        # -------------------------------------------------
        # EXECUTE RAG PIPELINE
        # -------------------------------------------------

        rag_response = rag_service.ask(

            query=message_text,

            top_k=5,

            include_sources=True,
        )

        answer = rag_response["answer"]

        sources = rag_response.get(
            "sources",
            []
        )

        logger.info(
            "Generated RAG response."
        )

        # -------------------------------------------------
        # SEND WHATSAPP REPLY
        # -------------------------------------------------

        send_whatsapp_message(

            to_number=sender_number,

            message=answer,
        )

        logger.info(
            "WhatsApp reply sent."
        )

        # -------------------------------------------------
        # SAVE CONVERSATION
        # -------------------------------------------------

        save_conversation(

            db=db,

            phone_number=sender_number,

            user_message=message_text,

            ai_response=answer,

            retrieved_sources=sources,
        )

        logger.info(
            "Conversation saved to database."
        )

    # -----------------------------------------------------
    # ERROR HANDLING
    # -----------------------------------------------------

    except Exception as e:

        logger.exception(
            "Error processing WhatsApp webhook."
        )

    return {
        "status": "received"
    }