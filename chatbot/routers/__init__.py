from fastapi import APIRouter
from .chat import router as chat_router

router = APIRouter(prefix="/api/v1", tags=["api"])
router.include_router(chat_router)


@router.get("/")
def root():
    """
    Handles the "/" GET request.

    This function is an asynchronous handler for the "/" GET request.

    Returns:
        dict
    """
    return {"message": "Server is running"}
