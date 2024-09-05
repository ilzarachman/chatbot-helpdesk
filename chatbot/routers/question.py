from fastapi import APIRouter, Depends, status, BackgroundTasks, HTTPException
from pydantic import BaseModel

from chatbot.database import SessionLocal
from chatbot.database.models.Questions import Question
from chatbot.dependencies.DocumentEmbedder import DocumentEmbedder
from chatbot.dependencies.EmailHandler import EmailHandler, EmailSchema
from chatbot.dependencies.IntentClassifier import Intent
from chatbot.dependencies.utils.auth import protected_route, ACL
from chatbot.http.Response import Response as ResponseTemplate
from chatbot.logger import logger

router = APIRouter(prefix="/question", tags=["Question Answering"])

email_sender = EmailHandler()


class CreateQuestionRequest(BaseModel):
    """
    CreateQuestionRequest model.
    """

    prompt: str
    bot_answer: str
    message: str


@router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_question(
    question_req: CreateQuestionRequest,
    auth_user=Depends(protected_route(ACL.USER)),
):
    """
    Creates a new question and answer for everyone.

    Args:
        question_req (CreateQuestionRequest): The question request.
        auth_user (User, optional): The authenticated user.

    Returns:
        dict: A dictionary containing the question ID.
    """

    with SessionLocal() as db:
        question = Question()
        question.prompt = question_req.prompt
        question.bot_answer = question_req.bot_answer
        question.message = question_req.message
        question.public = False
        question.questioner_email = auth_user.email
        question.questioner_name = auth_user.name

        db.add(question)
        db.commit()
        db.refresh(question)

    return ResponseTemplate(
        message="Question created successfully",
        data={"question_id": question.id},
    )


class PublicCreateQuestionRequest(CreateQuestionRequest):
    """
    PublicCreateQuestionRequest model.
    """

    questioner_email: str
    questioner_name: str


@router.post("/public/new", status_code=status.HTTP_201_CREATED)
async def create_public_question(
    question_req: PublicCreateQuestionRequest,
):
    """
    Creates a new question and answer for everyone.

    Args:
        question_req (PublicCreateQuestionRequest): The question request.

    Returns:
        dict: A dictionary containing the question ID.
    """
    with SessionLocal() as db:
        question = Question()
        question.prompt = question_req.prompt
        question.bot_answer = question_req.bot_answer
        question.message = question_req.message
        question.public = True
        question.questioner_email = question_req.questioner_email
        question.questioner_name = question_req.questioner_name

        db.add(question)
        db.commit()

        question_id = question.id

    return ResponseTemplate(
        message="Question created successfully",
        data={"question_id": question_id},
    )


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_questions(auth_user=Depends(protected_route(ACL.STAFF))):
    """
    Returns all questions.

    Args:
        auth_user (User, optional): The authenticated user.

    Returns:
        list[Question]: A list of questions.
    """
    with SessionLocal() as db:
        questions = db.query(Question).all()
        return questions


async def embed_save_question(
    question: str, answer: str, category: Intent, public: bool
):
    """
    Saves a question and answer to the vectorstorage.

    Args:
        question (str): The question to be saved.
        answer (str): The answer to be saved.
        category (str): The type of the question and answer.
        public (bool): Whether the question and answer are public or not.

    Returns:
        None
    """
    logger.debug(
        f"Embedding question: {question}, answer: {answer}, category: {category}, public: {public}"
    )
    doc = DocumentEmbedder()

    if public:
        doc.save_public_question_answer_to_vectorstore(question, answer, category)
    else:
        doc.save_question_answer_to_vectorstore(question, answer, category)

    logger.debug(f"Finished embedding {question}")


class AnswerQuestionRequest(BaseModel):
    """
    AnswerQuestionRequest model.
    """

    answer: str
    intent: str
    public: bool


@router.post("/answer/{question_id}", status_code=status.HTTP_200_OK)
async def answer_question(
    question_id: int,
    answer: AnswerQuestionRequest,
    background_tasks: BackgroundTasks,
    auth_user=Depends(protected_route(ACL.STAFF)),
):
    """
    Answers a question.

    Args:
        question_id(int): Id of the question.
        answer: Answer of the question.
        background_tasks: Background tasks.
        auth_user: Authenticated user.

    Returns:
        None

    """
    try:
        _intent = Intent(answer.intent)
    except ValueError:
        raise HTTPException(
            detail="Invalid intent. Please use one of the following intents: "
            + ", ".join([str(i) for i in Intent]),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    _email = ""

    with SessionLocal() as db:
        question = db.query(Question).filter_by(id=question_id).first()
        question.answered_by = auth_user.id
        question.staff_answer = answer.answer
        question.intent = answer.intent
        question.public = answer.public

        _email = question.questioner_email

        db.commit()
        db.refresh(question)

    # TODO: Use background task to save question and answer to vectorstore
    background_tasks.add_task(
        embed_save_question,
        question.prompt,
        question.bot_answer,
        _intent,
        answer.public,
    )

    # Send answered question to the email
    await email_sender.send_email(
        EmailSchema(
            email=[_email],
            subject="Answered Question",
            body=f"Your question has been answered. Answer: {question.staff_answer}",
        )
    )

    return ResponseTemplate(
        message="Answered successfully",
        data={"question_id": question_id, "email": _email},
    )


@router.delete("/{question_id}", status_code=status.HTTP_200_OK)
async def delete_question(
    question_id: int,
    auth_user=Depends(protected_route(ACL.STAFF)),
):
    """
    Deletes a question.

    Args:
        question_id (int): Id of the question to be deleted.
        auth_user (User, optional): The authenticated user.

    Returns:
        None
    """
    with SessionLocal() as db:
        question = db.query(Question).filter_by(id=question_id).first()
        db.delete(question)
        db.commit()

    return ResponseTemplate(
        message="Question deleted successfully",
        data={"question_id": question_id},
    )
