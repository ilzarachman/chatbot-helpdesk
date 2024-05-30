from typing_extensions import Annotated
from fastapi import APIRouter, Depends, Request
from ..Application import Application

router = APIRouter(prefix="/chat", tags=["chat"])

@router.get("/prompt")
async def handle_prompt(req: Request):
    """
    Handles the "/prompt" GET request.

    This function is an asynchronous handler for the "/prompt" GET request.

    Parameters:
        app (Application, optional): An instance of the `Application` class obtained by calling the `get_instance` method. Defaults to None.

    Returns:
        dict
    """
    return {"message": "Handled"}