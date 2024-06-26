from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from ..Application import Application
from ..app import get_application
from ..dependencies.IntentClassifier import Intent
from chatbot.intent_handler import IntentHandlerFactory
from ..logger import logger
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatMessage(BaseModel):
    """
    ChatMessage model.
    """
    message: str


@router.post("/prompt")
async def chat_prompt(chat_message: ChatMessage, app: Application = Depends(get_application)):
    """
    Handles the "/prompt" GET request.

    This function is an asynchronous handler for the "/prompt" GET request.

    Returns:
        dict
    """
    logger.debug(f"Received message: {chat_message.message}")
    message: str = chat_message.message
    intent: Intent = await app.intent_classifier.classify(message)

    handler = IntentHandlerFactory.get_handler(intent)
    response = await handler.with_app(app).handle(message)

    return StreamingResponse(response, media_type="text/plain")
