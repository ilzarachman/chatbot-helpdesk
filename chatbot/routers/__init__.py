from fastapi import APIRouter
from .chat import router as chat_router
from .student import router as user_router
from .auth import router as auth_router
from .staff import router as staff_router
from .conversation import router as conversation_router
from .document import router as document_router
from .question import router as question_router

router = APIRouter(prefix="/api/v1")
router.include_router(chat_router)
router.include_router(user_router)
router.include_router(auth_router)
router.include_router(staff_router)
router.include_router(conversation_router)
router.include_router(document_router)
router.include_router(question_router)


@router.get("/")
def root():
    """
    Handles the "/" GET request.

    This function is an asynchronous handler for the "/" GET request.

    Returns:
        dict
    """
    return {"message": "Server is running"}
