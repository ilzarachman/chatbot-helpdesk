import hashlib
import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status

from chatbot.database import SessionLocal
from chatbot.database.models.Message import Message
from chatbot.database.models.Student import Student
from chatbot.dependencies.utils.auth import protected_route, ACL
from chatbot.database.models.Conversation import Conversation
from chatbot.http.Response import Response as ResponseTemplate
from chatbot.dependencies.TitleGenerator import TitleGenerator
from chatbot.database.models.Staff import Staff
from ..Application import Application
from ..logger import logger
from pydantic import BaseModel

router = APIRouter(prefix="/conversation", tags=["Conversation"])


class CreateConversationRequest(BaseModel):
    """
    CreateConversationRequest model.
    """

    assistant_message: str


@router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_conversation(
    conv_req: CreateConversationRequest,
    auth_user: Student | Staff = Depends(protected_route(ACL.USER)),
):
    """
    Creates a new conversation for the authenticated user.

    Args:
        conv_req (CreateConversationRequest): The conversation request.
        auth_user (User, optional): The authenticated user. Defaults to Depends(protected_route(ACL.USER)).

    Returns:
        dict: A dictionary containing the conversation ID.
    """
    with SessionLocal() as db:
        conversation = Conversation()
        conversation.user_id = auth_user.id
        conversation.start_time = datetime.now()
        conversation.uuid = str(
            hashlib.sha256(str(datetime.now()).encode()).hexdigest()
        )
        conversation.user_type = 1 if isinstance(auth_user, Student) else 0
        conversation.name = await TitleGenerator().generate_title(
            conv_req.assistant_message
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    return ResponseTemplate(
        data={
            "uuid": conversation.uuid,
            "start_time": conversation.start_time,
            "name": conversation.name,
        },
        message="Conversation created successfully",
    )


@router.get("/all")
async def get_conversations(
    auth_user: Student | Staff = Depends(protected_route(ACL.USER)),
):
    """
    Retrieves all conversations for the authenticated user.

    Args:
        auth_user (User, optional): The authenticated user. Defaults to Depends(protected_route(ACL.USER)).

    Returns:
        dict: A dictionary containing the conversation ID.
    """
    with SessionLocal() as db:
        user_type = 1 if isinstance(auth_user, Student) else 0
        conversations = (
            db.query(Conversation)
            .filter_by(user_id=auth_user.id, user_type=user_type)
            .order_by(Conversation.start_time.desc())
            .all()
        )

    return ResponseTemplate(
        data={
            "conversations": [
                {
                    "uuid": conversation.uuid,
                    "start_time": conversation.start_time,
                    "name": conversation.name,
                }
                for conversation in conversations
            ]
        },
        message="Conversations retrieved successfully",
    )


@router.get("/messages/{conversation_uid}")
async def get_conversation_by_id(
    conversation_uid: str,
    auth_user: Student | Staff = Depends(protected_route(ACL.USER)),
):
    """
    Retrieves a conversation by ID for the authenticated user.

    Args:
        conversation_uid (int): The conversation ID.
        auth_user (User, optional): The authenticated user. Defaults to Depends(protected_route(ACL.USER)).

    Returns:
        dict: A dictionary containing the conversation ID.
    """
    with SessionLocal() as db:
        user_type = 1 if isinstance(auth_user, Student) else 0
        conversation = (
            db.query(Conversation)
            .filter_by(uuid=conversation_uid, user_id=auth_user.id, user_type=user_type)
            .first()
        )

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )

        messages = (
            db.query(Message)
            .filter_by(conversation_id=conversation.id)
            .order_by(Message.created_at)
            .all()
        )

        for message in messages:
            message.text = json.loads(message.text)

    data = {
        "id": conversation.id,
        "start_time": conversation.start_time,
        "name": conversation.name,
        "messages": [
            {
                "user": message.text["U"],
                "assistant": message.text["A"],
            }
            for message in messages
        ],
    }

    return ResponseTemplate(
        data=data,
        message="Conversation retrieved successfully",
    )
