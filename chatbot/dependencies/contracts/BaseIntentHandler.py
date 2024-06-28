from abc import ABC, abstractmethod
from typing import Optional, AsyncIterator

from jinja2 import Template
from pydantic import BaseModel

from chatbot.Application import Application
from chatbot.dependencies.InformationRetriever import InformationRetriever
from chatbot.dependencies.IntentClassifier import Intent, IntentClassifier
from chatbot.dependencies.PromptManager import PromptManager
from chatbot.dependencies.contracts.message import Message, UserMessage

# TODO: Implement response generator in each intent handlers


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

    @property
    def information_retriever(self) -> InformationRetriever:
        """
        Gets the information retriever.

        Returns:
            InformationRetriever: The information retriever.
        """
        return self._application.information_retriever

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
        _prompt_template_no_context = PromptManager.get_prompt_template(
            "response_generator", intent.name
        )
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

    def build_prompt(self, context: Optional[dict] = None) -> str:
        """
        Builds the prompt with context.

        Parameters:
            context (dict): The context.

        Returns:
            str: The prompt with context.
        """
        if context is None:
            context = {}
        return self._prompt_template.render(**context)

    @abstractmethod
    async def handle(self, message: str) -> AsyncIterator[str]:
        """
        Handles the intent of the message.

        This function takes a message as input and returns the response as a string.

        Parameters:
            message (str): The message to be handled.

        Returns:
            str: The response to the message.
        """
        pass
