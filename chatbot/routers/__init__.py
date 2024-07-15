from fastapi import APIRouter
from .chat import router as chat_router
from .student import router as user_router
from .auth import router as auth_router
from .staff import router as staff_router

router = APIRouter(prefix="/api/v1")
router.include_router(chat_router)
router.include_router(user_router)
router.include_router(auth_router)
router.include_router(staff_router)


@router.get("/")
def root():
    """
    Handles the "/" GET request.

    This function is an asynchronous handler for the "/" GET request.

    Returns:
        dict
    """
    return {"message": "Server is running"}
