from fastapi import APIRouter, Depends, Request
from ..Application import Application
from ..app import get_application
from ..dependencies.IntentClassifier import Intent
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
    # TODO: implement this function:
    # 1. classify the intent of the message
    # 2. handle the specific intent (may need separate file for each intent)
    # 3. generate the response using response generator
    intent: Intent = await app.intent_classifier.classify(message)
    logger.debug(f"Detected intent: {intent}")

    return {"intent": intent}
