from typing import Optional

from jinja2 import Template

from chatbot.dependencies.contracts.TextGenerator import TextGenerator
from chatbot.dependencies.ModelLoader import ModelLoader
from chatbot.config import Configuration
from chatbot.dependencies.PromptManager import PromptManager
from chatbot.dependencies.contracts.message import Message, SystemMessage, UserMessage


class TitleGenerator:
    _instance: Optional["TitleGenerator"] = None

    def __init__(self):
        """
        Initializes the TitleGenerator instance by loading configuration, model, and prompt template.
        """
        self._config: dict = Configuration.get("title_generator")
        self._model: TextGenerator = ModelLoader.load_model(self._config.get("model"))
        self._prompt_template: str = PromptManager.get_prompt(
            "title_generator", "main_prompt"
        )

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def generate_title(self, message: str) -> str:
        """
        Asynchronously generates a title based on a given message.

        Parameters:
            self: The TitleGenerator instance.
            message (str): The message to generate the title from.

        Returns:
            str: The generated title.
        """
        messages: list[Message] = [
            SystemMessage(self._prompt_template),
            UserMessage(message),
        ]

        response = await self._model.generate_async(messages)

        return response
