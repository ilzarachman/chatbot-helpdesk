import hashlib
import json
import os
import shutil
from datetime import datetime
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Request,
    UploadFile,
    BackgroundTasks,
    Form,
)

from chatbot.database import SessionLocal
from chatbot.database.models.Message import Message
from chatbot.database.models.Student import Student
from chatbot.database.models.Document import Document
from chatbot.dependencies.DocumentEmbedder import DocumentEmbedder
from chatbot.dependencies.utils.auth import protected_route, ACL
from chatbot.database.models.Conversation import Conversation
from chatbot.http.Response import Response as ResponseTemplate
from chatbot.dependencies.TitleGenerator import TitleGenerator
from chatbot.database.models.Staff import Staff
from chatbot.dependencies.IntentClassifier import Intent
from ..Application import Application
from ..logger import logger
from chatbot.dependencies.utils.path_utils import project_path
from pydantic import BaseModel

router = APIRouter(prefix="/document", tags=["Document"])


class DocumentUpload(BaseModel):
    name: str
    uploader_id: int
    intent: str
    public: bool


DOCUMENT_DIRECTORY = str(project_path("resources", "documents"))


def embed_document(
    document_path: str, metadata: DocumentUpload, document_id: int
) -> None:
    """
    Embeds a document in the database.

    Parameters:
        document_path (str): The path to the document.
        metadata (DocumentUpload): The metadata of the document.
        document_id (int): The ID of the document.

    Returns:
        None
    """
    document_embedder = DocumentEmbedder()

    logger.debug(f"Embedding document: {document_path}")
    if metadata.public:
        document_embedder.save_public_document_to_vectorstore(
            document_path, Intent(metadata.intent.strip())
        )
    else:
        document_embedder.save_document_to_vectorstore(
            document_path, Intent(metadata.intent.strip())
        )

    with SessionLocal() as db:
        db.query(Document).filter(Document.id == document_id).update(
            {
                Document.embedded: True,
            }
        )
        db.commit()


@router.post("/upload", status_code=status.HTTP_200_OK)
async def upload_document(
    document_file: UploadFile,
    name: Annotated[str, Form()],
    intent: Annotated[str, Form()],
    public: Annotated[bool, Form()],
    background_tasks: BackgroundTasks,
    auth_user=Depends(protected_route(ACL.STAFF)),
):
    """
    Uploads a document to the server.

    Parameters:
        document_file (UploadFile): The file to be uploaded.
        name (str): The name of the document.
        intent (str): The intent of the document.
        public (bool): Whether the document is public.
        background_tasks (BackgroundTasks): The background tasks object.

    Raises:
        HTTPException: If the file type is not supported.

    Returns:
        None
    """
    document_metadata = DocumentUpload(
        name=name, uploader_id=auth_user.id, intent=intent, public=public
    )
    file_extension = document_file.filename.split(".")[-1]

    if file_extension not in DocumentEmbedder.supported_document_types.keys():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File type not supported.",
        )

    uuid_string = str("doc324iyi" + str(datetime.now())).encode()
    uuid_hashed = str(hashlib.sha256(uuid_string).hexdigest())

    save_folder = f"{DOCUMENT_DIRECTORY}/{document_metadata.intent}"
    save_filename = f"{save_folder}/{document_file.filename}-{uuid_hashed}.{file_extension}"

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    with open(
            save_filename,
            "wb",
    ) as buffer:
        contents = await document_file.read()
        buffer.write(contents)

    with SessionLocal() as db:
        document = Document()
        document.name = document_metadata.name
        document.uploader_id = document_metadata.uploader_id
        document.intent = document_metadata.intent
        document.public = document_metadata.public
        document.file_path = save_filename
        document.uuid = uuid_hashed

        db.add(document)
        db.commit()
        db.refresh(document)

    background_tasks.add_task(
        embed_document, save_filename, document_metadata, document.id
    )

    return ResponseTemplate(
        message="Document uploaded successfully",
        data={"document_id": document.id},
    )
