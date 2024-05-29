from fastapi import APIRouter
from .chat import router as chat_router

router = APIRouter(prefix="/api/v1", tags=["api"])
router.include_router(chat_router)