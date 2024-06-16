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
    intent: Intent = await app.intent_classifier.classify(message)
    print(type(intent))

    return {"intent": intent}
