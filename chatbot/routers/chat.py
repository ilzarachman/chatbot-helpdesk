from fastapi import APIRouter, Depends, Request
from ..Application import Application
from ..app import get_application
from ..dependencies.IntentClassifier import Intent
from ..logger import logger

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/prompt")
async def handle_prompt(req: Request, app: Application = Depends(get_application)):
    """
    Handles the "/prompt" GET request.

    This function is an asynchronous handler for the "/prompt" GET request.

    Returns:
        dict
    """
    message: str = req.query_params.get("message")
    intent: Intent = app.intent_classifier.classify(message)
    print(intent)

    return {"intent": intent}
