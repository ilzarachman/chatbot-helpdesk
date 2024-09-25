from typing import AsyncIterator

from chatbot.dependencies.IntentClassifier import Intent
from chatbot.dependencies.ResponseGenerator import ResponseGenerator
from chatbot.dependencies.contracts.BaseIntentHandler import BaseIntentHandler
from chatbot.logger import logger


class OtherIntentHandler(BaseIntentHandler):
    """
    Intent handler for other intent.
    """

    def __init__(self):
        super().__init__()
        self._intent: Intent = Intent.OTHER
        self.with_prompt_template(self._intent)

    async def handle(self, message: str, history: list[dict] | None = None) -> AsyncIterator[str]:
        """
        Handles the intent of the message.

        This function takes a message as input and returns the response as a string.

        Parameters:
            message (str): The message to be handled.
            history (list[dict]): The history list.

        Returns:
            str: The response to the message.
        """
        prompt_template = self.build_prompt()
        response_generator = ResponseGenerator.with_prompt_template(prompt_template)

        logger.debug(f"History: {history}")

        response = response_generator.response_async(message, history)

        return response

    async def handle_public(self, message: str, history: list[dict] | None = None) -> AsyncIterator[str]:
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

        response = response_generator.response_async(message, history)

        return response
