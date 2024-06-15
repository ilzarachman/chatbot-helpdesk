from typing_extensions import Annotated
from fastapi import APIRouter, Depends, Request
from ..Application import Application
from ..app import get_application
from ..logger import logger

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/prompt")
async def handle_prompt(app: Application = Depends(get_application)):
    """
    Handles the "/prompt" GET request.

    This function is an asynchronous handler for the "/prompt" GET request.

    Returns:
        dict
    """
    logger.debug(app)
    return {"message": "Handled"}
