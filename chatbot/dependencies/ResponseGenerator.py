from typing import Optional, Generator, AsyncGenerator, AsyncIterator

from chatbot.config import Configuration
from chatbot.dependencies.ModelLoader import ModelLoader
from chatbot.dependencies.contracts.TextGenerator import TextGenerator
from chatbot.dependencies.contracts.message import (
    Message,
    SystemMessage,
    UserMessage,
    AssistantMessage,
)
from chatbot.logger import logger


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

    def _build_history_messages(
        self, user_prompt: str, history: list[dict]
    ) -> list[Message]:
        """
        Helper method to build the history messages.

        Parameters:
            history (list[dict]): The history list.

        Returns:
            list[Message]: The list of messages.
        """
        prompts: list[Message] = [SystemMessage(self._prompt_template)]

        for msg in history:
            prompts.append(UserMessage(msg["U"]))
            prompts.append(AssistantMessage(msg["A"]))
        prompts.append(UserMessage(user_prompt))

        return prompts

    async def response_async(
        self, message: str, history: list[dict]
    ) -> AsyncIterator[str]:
        """
        Generate a response based on the input.

        This function takes a string as input and returns a string iterator as a response.

        Parameters:
            message (str): The input string.
            history (list[dict]): The history list.

        Yields:
            str: The response string.
        """
        print(message)
        prompts: list[Message] = self._build_history_messages(message, history)

        logger.debug(f"Prompts: {[str(prompt) for prompt in prompts]} ")

        async_res = self._model.stream_async(
            prompts, self._config.get("model_settings")
        )

        async for chunk in aiter(async_res):
            yield chunk
