from datetime import datetime
from typing import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from chatbot.database import SessionLocal
from chatbot.database.models.Message import Message
from chatbot.database.models.Student import Student
from chatbot.dependencies.utils.auth import protected_route, ACL
from chatbot.database.models.Conversation import Conversation
from chatbot.http.Response import Response as ResponseTemplate
from ..Application import Application
from ..app import get_application
from ..dependencies.IntentClassifier import Intent
from chatbot.intent_handler import IntentHandlerFactory
from ..logger import logger
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["Chat"])
# TODO: integrate the chat api endpoints with database.
# - contexts_saving_method: we could do with creating contexts for each interation with user. we could generate the context on every user interaction using generative prompt templating.
# - history_saving_method: or feeds all the message history to the chat model.


class ChatMessage(BaseModel):
    """
    ChatMessage model.
    """

    message: str = "This is a test message"


@router.post("/prompt")
async def chat_prompt(
    chat_message: ChatMessage,
    app: Application = Depends(get_application),
    auth_user: Student = Depends(protected_route(ACL.USER)),
):
    """
    Receives a prompt and returns the response.

    Args:
        chat_message (ChatMessage): The prompt message.
        app (Application, optional): The application. Defaults to Depends(get_application).
        auth_user (User, optional): The authenticated user. Defaults to Depends(protected_route(ACL.USER)).

    Returns:
        dict: The response message.
    """
    logger.debug(f"Received message: {chat_message.message}")
    message: str = chat_message.message
    intent: Intent = await app.intent_classifier.classify(message)

    handler = IntentHandlerFactory.get_handler(intent)
    response = await handler.with_app(app).handle(message)

    logger.debug(f"Response: {response}")

    return StreamingResponse(response, media_type="text/plain")


class StoreChatRequest(BaseModel):
    """
    StoreChatRequest model.
    """

    user_message: str
    assistant_message: str
    conversation_id: int


@router.post("/chat/store", status_code=status.HTTP_201_CREATED)
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
    db = SessionLocal()
    user_message = Message()
    user_message.conversation_id = store_chat_request.conversation_id
    user_message.message_type = "user"
    user_message.text = store_chat_request.user_message

    assistant_message = Message()
    assistant_message.conversation_id = store_chat_request.conversation_id
    assistant_message.message_type = "assistant"
    assistant_message.text = store_chat_request.assistant_message

    db.add(user_message)
    db.add(assistant_message)
    db.commit()

    return ResponseTemplate(
        data=store_chat_request.conversation_id,
        message="Chat stored successfully",
    )


@router.post("/conversation/new", status_code=status.HTTP_201_CREATED)
async def create_conversation(auth_user: Student = Depends(protected_route(ACL.USER))):
    """
    Creates a new conversation for the authenticated user.

    Args:
        auth_user (User, optional): The authenticated user. Defaults to Depends(protected_route(ACL.USER)).

    Returns:
        dict: A dictionary containing the conversation ID.
    """
    db = SessionLocal()
    conversation = Conversation()
    conversation.user_id = auth_user.id
    conversation.start_time = datetime.now()
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return ResponseTemplate(
        data={"id": conversation.id, "start_time": conversation.start_time, "name": conversation.name},
        message="Conversation created successfully",
    )


@router.get("/conversation/all")
async def get_conversations(auth_user: Student = Depends(protected_route(ACL.USER))):
    """
    Retrieves all conversations for the authenticated user.

    Args:
        auth_user (User, optional): The authenticated user. Defaults to Depends(protected_route(ACL.USER)).

    Returns:
        dict: A dictionary containing the conversation ID.
    """
    db = SessionLocal()
    conversations = db.query(Conversation).filter_by(user_id=auth_user.id).all()

    return ResponseTemplate(
        data=conversations,
        message="Conversations retrieved successfully",
    )
