from abc import ABC, abstractmethod
from typing import Optional

from jinja2 import Template
from pydantic import BaseModel

from chatbot.Application import Application
from chatbot.dependencies.IntentClassifier import Intent
from chatbot.dependencies.PromptManager import PromptManager
from chatbot.dependencies.contracts.message import Message, UserMessage


class BaseIntentHandler(ABC):
    """
    Base class for intent handlers. An intent handler is responsible for handling an intent.
    """

    def __init__(self):
        self._application: Optional[Application] = None
        self._prompt_template: Optional[Template] = None

    @property
    def prompt_template(self) -> Template:
        """
        Gets the prompt template.

        Returns:
            str: The prompt template.
        """
        return self._prompt_template

    @property
    def application(self) -> Optional[Application]:
        """
        Gets the application instance.

        Returns:
            Optional[Application]: The application instance.
        """
        return self._application

    def with_app(self, application: Application) -> "BaseIntentHandler":
        """
        Sets the application instance.

        Parameters:
            application (Application): The application instance.

        Returns:
            BaseIntentHandler: The intent handler instance.
        """
        self._application = application
        return self

    def with_prompt_template(self, intent: Intent):
        """
        Sets the prompt template.

        Parameters:
            intent (Intent): The intent.

        Returns:
            str: The prompt template.
        """
        _prompt_template_no_context = PromptManager.get_prompt_template("response_generator", intent.name)
        self._prompt_template = _prompt_template_no_context
        return self

    def build_prompt_with_information(self, information: str) -> str:
        """
        Builds the prompt with information.

        Parameters:
            information (str): The information.

        Returns:
            str: The prompt with information.
        """
        return self._prompt_template.render(information=information)

    @abstractmethod
    async def handle(self, message: str) -> str:
        """
        Handles the intent of the message.

        This function takes a message as input and returns the response as a string.

        Parameters:
            message (str): The message to be handled.

        Returns:
            str: The response to the message.
        """
        pass
