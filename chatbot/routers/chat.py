from fastapi import APIRouter, Depends
from ..Application import Application
from ..app import get_application
from ..dependencies.IntentClassifier import Intent
from chatbot.intent_handler import IntentHandlerFactory
from ..logger import logger
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatMessage(BaseModel):
    message: str


@router.post("/prompt")
async def chat_prompt(message: str, app: Application = Depends(get_application)):
    """
    Handles the "/prompt" GET request.

    This function is an asynchronous handler for the "/prompt" GET request.

    Returns:
        dict
    """
    intent: Intent = await app.intent_classifier.classify(message)
    logger.debug(f"Detected intent: {intent}")

    handler = IntentHandlerFactory.get_handler(intent)
    response = await handler.with_app(app).handle(message)

    return {"response": response}
