import hashlib
import json
from datetime import datetime
from typing import AsyncGenerator, AsyncIterator

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from chatbot.database import SessionLocal
from chatbot.database.models.Message import Message
from chatbot.database.models.Student import Student
from chatbot.dependencies.utils.auth import protected_route, ACL
from chatbot.database.models.Conversation import Conversation
from chatbot.http.Response import Response as ResponseTemplate
from chatbot.dependencies.TitleGenerator import TitleGenerator
from chatbot.database.models.Staff import Staff
from ..Application import Application
from ..app import get_application
from ..dependencies.IntentClassifier import Intent
from chatbot.intent_handler import IntentHandlerFactory
from ..logger import logger
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatMessage(BaseModel):
    """
    ChatMessage model.
    """

    message: str = "This is a test message"
    conversation_uuid: str = ""

class ChatMessageWithHistory(ChatMessage):
    """
    ChatMessageWithHistory model.
    """

    history: str = ""


async def handle_chat_for_authenticated_user(
        chat_message: ChatMessage,
        app: Application,
        user: Student | Staff,
) -> AsyncIterator[str]:
    """
    Handles the chat for an authenticated user.

    Args:
        chat_message (ChatMessage): The chat message.
        app (Application): The application.
        user (Student): The authenticated user.
        history (list[dict]): The history list.

    Returns:
        dict: The response message.
    """
    _conv_id = None
    history: list[dict] = []

    if chat_message.conversation_uuid != "":
        with SessionLocal() as db:
            conversation = (
                db.query(Conversation)
                .filter(Conversation.uuid == chat_message.conversation_uuid and user.id == user.id)
                .first()
            )

            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found",
                )

            _conv_id = conversation.id

            if _conv_id is not None:
                messages = (
                    db.query(Message)
                    .filter_by(conversation_id=_conv_id)
                    .order_by(Message.created_at.asc())
                    .limit(2)
                    .all()
                )

                for msg in messages:
                    history.append(json.loads(msg.text))

    message: str = chat_message.message
    intent: Intent = await app.intent_classifier.classify_with_history(message, history)

    logger.info(f"get intent: {intent.value}")

    handler = IntentHandlerFactory.get_handler(intent)
    response = await handler.with_app(app).handle(message, history=history)

    return response


async def handle_chat_for_non_user(
        chat_message: ChatMessageWithHistory,
        app: Application,
) -> AsyncIterator[str]:
    """
    Handles the chat for a non-authenticated user.

    Args:
        chat_message (ChatMessage): The chat message.
        app (Application): The application.

    Returns:
        dict: The response message.
    """
    history: list[dict] = json.loads(chat_message.history)

    logger.info(f"get history: {history}")

    message: str = chat_message.message
    intent: Intent = await app.intent_classifier.classify_with_history(message, history)

    logger.info(f"get non user intent: {intent.value}")

    handler = IntentHandlerFactory.get_handler(intent)
    response = await handler.with_app(app).handle_public(message, history=history)

    return response


@router.post("/prompt")
async def chat_prompt(
        chat_message: ChatMessageWithHistory,
        app: Application = Depends(get_application),
        user: Student | Staff | None = Depends(protected_route(ACL.ALL)),
):
    """
    Receives a prompt and returns the response.

    Args:
        chat_message (ChatMessage): The prompt message.
        app (Application, optional): The application. Defaults to Depends(get_application).
        user (Student | Staff | None, optional): The authenticated user. Defaults to Depends(protected_route(ACL.USER)).

    Returns:
        dict: The response message.
    """
    logger.debug(f"Received message: {chat_message.message}, conversation_uuid: {chat_message.conversation_uuid}")

    if user is None:
        response = await handle_chat_for_non_user(chat_message, app)
    else:
        response = await handle_chat_for_authenticated_user(chat_message, app, user)

    return StreamingResponse(response, media_type="text/plain")


class StoreChatRequest(BaseModel):
    """
    StoreChatRequest model.
    """

    user_message: str
    assistant_message: str
    conversation_uuid: str


@router.post("/store", status_code=status.HTTP_201_CREATED)
async def store_chat(
        store_chat_request: StoreChatRequest,
        auth_user: Student = Depends(protected_route(ACL.USER)),
):
    """
    Stores the chat history for the authenticated user.

    Args:
        store_chat_request (StoreChatRequest): The chat history.
        auth_user (User, optional): The authenticated user. Defaults to Depends(protected_route(ACL.USER)).

    Returns:
        dict: A dictionary containing the conversation ID.
    """
    with SessionLocal() as db:
        conversation = (
            db.query(Conversation)
            .filter_by(uuid=store_chat_request.conversation_uuid, user_id=auth_user.id)
            .first()
        )

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )

        message = Message()
        text_json = {
            "U": store_chat_request.user_message,
            "A": store_chat_request.assistant_message,
        }

        message.conversation_id = conversation.id
        message.text = json.dumps(text_json)

        db.add(message)
        db.commit()

    return ResponseTemplate(
        data={
            "conversation_uuid": store_chat_request.conversation_uuid,
        },
        message="Chat stored successfully",
    )
