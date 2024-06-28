from typing import AsyncIterator

from chatbot.dependencies.IntentClassifier import Intent
from chatbot.dependencies.ResponseGenerator import ResponseGenerator
from chatbot.dependencies.contracts.BaseIntentHandler import BaseIntentHandler


class OtherIntentHandler(BaseIntentHandler):
    """
    Intent handler for other intent.
    """

    _intent: Intent = Intent.OTHER

    def __init__(self):
        super().__init__()
        self.with_prompt_template(self._intent)

    async def handle(self, message: str) -> AsyncIterator[str]:
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
        response = response_generator.response_async(message)

        return response

