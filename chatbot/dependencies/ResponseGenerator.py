from typing import Optional

from chatbot.config import Configuration
from chatbot.dependencies.ModelLoader import ModelLoader
from chatbot.dependencies.contracts.TextGenerator import TextGenerator
from chatbot.dependencies.contracts.message import Message, SystemMessage, UserMessage


class ResponseGenerator:
    """
    This class represents the response generator.
    """

    def __init__(self, prompt_template: str):
        """
        Initialize the response generator.

        Parameters:
            prompt_template (str): The prompt template.
        """
        self._prompt_template: str = prompt_template
        self._config: dict = Configuration.get("response_generator")
        self._model: TextGenerator = ModelLoader.load_model(
            self._config.get("generator_model")
        )

    @staticmethod
    def with_prompt_template(prompt_template: str) -> "ResponseGenerator":
        """
        Create a response generator with a prompt template.

        Parameters:
            prompt_template (str): The prompt template.

        Returns:
            ResponseGenerator: The response generator.
        """
        return ResponseGenerator(prompt_template)

    def _build_prompt_with_examples(self, message: str) -> list[Message]:
        """
        Helper method to build the prompt with example.

        Parameters:
            message (str): The message to be classified.

        Returns:
            list[Message]: The list of messages.
        """
        prompts: list[Message] = [
            SystemMessage(self._prompt_template),
            UserMessage(message),
        ]

        return prompts

    async def response_async(self, message: str) -> str:
        """
        Generate a response based on the input.

        This function takes a string as input and returns a string as a response.

        Parameters:
            message (str): The input string.

        Yields:
            str: The response string.
        """
        prompts: list[Message] = self._build_prompt_with_examples(message)
        res = await self._model.stream_async(
            prompts, self._config.get("model_settings")
        )
        for chunk in res:
            yield chunk
