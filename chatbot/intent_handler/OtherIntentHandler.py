import json
from typing import AsyncIterator

from sqlalchemy import func

from logger import logger
from chatbot.dependencies.IntentClassifier import Intent
from chatbot.dependencies.ResponseGenerator import ResponseGenerator
from chatbot.dependencies.contracts.BaseIntentHandler import BaseIntentHandler
from chatbot.database import SessionLocal
from chatbot.database.models.Message import Message


class OtherIntentHandler(BaseIntentHandler):
    """
    Intent handler for other intent.
    """

    _intent: Intent = Intent.OTHER

    def __init__(self):
        super().__init__()
        self.with_prompt_template(self._intent)

    async def handle(self, message: str, conversation_id: int | None = None) -> AsyncIterator[str]:
        """
        Handles the intent of the message.

        This function takes a message as input and returns the response as a string.

        Parameters:
            message (str): The message to be handled.

        Returns:
            str: The response to the message.
        """
        prompt_template = self.build_prompt()
        response_generator = ResponseGenerator.with_prompt_template(prompt_template)

        history = []
        if conversation_id is not None:
            with SessionLocal() as db:
                messages = (
                    db.query(Message)
                    .filter_by(conversation_id=conversation_id)
                    .order_by(Message.created_at)
                    .limit(2)
                    .all()
                )

                for msg in messages:
                    history.append(json.loads(msg.text))
        else:
            history = []

        logger.debug(f"History: {history}")

        response = response_generator.response_async(message, history)

        return response

