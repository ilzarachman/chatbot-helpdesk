from fastapi import APIRouter
from .chat import router as chat_router
from .user import router as user_router

router = APIRouter(prefix="/api/v1", tags=["api"])
router.include_router(chat_router)
router.include_router(user_router)


@router.get("/")
def root():
    """
    Handles the "/" GET request.

    This function is an asynchronous handler for the "/" GET request.

    Returns:
        dict
    """
    return {"message": "Server is running"}
