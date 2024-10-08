from abc import ABC
from typing import Optional, AsyncIterator, List

from jinja2 import Template

from chatbot.Application import Application
from chatbot.dependencies.InformationRetriever import InformationRetriever
from chatbot.dependencies.IntentClassifier import Intent
from chatbot.dependencies.PromptManager import PromptManager
from chatbot.dependencies.ResponseGenerator import ResponseGenerator
from chatbot.dependencies.contracts.message import Message
from chatbot.logger import logger


class BaseIntentHandler(ABC):
    """
    Base class for intent handlers. An intent handler is responsible for handling an intent.
    """

    def __init__(self):
        self._intent = None
        self._application: Optional[Application] = None
        self._prompt_template: Optional[Template] = None
        self._public_prompt_template: Optional[Template] = None
        self._history: Optional[List[Message]] = None

    @property
    def prompt_template(self) -> Template:
        """
        Gets the prompt template.

        Returns:
            str: The prompt template.
        """
        return self._prompt_template

    @property
    def public_prompt_template(self) -> Template:
        """
        Gets the public prompt template.

        Returns:
            str: The public prompt template.
        """
        return self._public_prompt_template

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

        _public_prompt_template_no_context = PromptManager.get_prompt_template(
            "public_response_generator", intent.name
        )

        self._prompt_template = _prompt_template_no_context
        self._public_prompt_template = _public_prompt_template_no_context
        return self

    def build_prompt_with_information(self, information: str | None) -> str:
        """
        Builds the prompt with information.

        Parameters:
            information (str | None): The information.

        Returns:
            str: The prompt with information.
        """
        if information is None:
            return self._prompt_template.render()
        return self._prompt_template.render(information=information)

    def build_public_prompt_with_information(
        self, information: str | None = None
    ) -> str:
        """
        Builds the prompt with information.

        Parameters:
            information (str | None): The information.

        Returns:
            str: The prompt with information.
        """
        if information is None:
            return self._public_prompt_template.render()
        return self._public_prompt_template.render(information=information)

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

    async def handle(
        self, message: str, history: list[dict] | None = None
    ) -> AsyncIterator[str]:
        """
        Handles the intent of the message.

        This function takes a message as input and returns the response as a string.

        Parameters:
            message (str): The message to be handled.
            history (list[dict]): The history list.

        Returns:
            str: The response to the message.
        """
        if self._intent is None:
            raise NotImplementedError("intent is not set")

        logger.debug(f"Handling intent: {self._intent}")

        message_with_history = (
            "\n".join([f"{message['U']}\n{message['A']}" for message in history])
            + "\n"
            + message
        )

        logger.debug(f"Message with history: {message_with_history}")

        information = await self.information_retriever.retrieve_async(
            message_with_history, self._intent
        )
        prompt_template = self.build_prompt_with_information(information)
        response_generator = ResponseGenerator.with_prompt_template(prompt_template)
        response = response_generator.response_async(message, history)

        return response

    async def handle_public(
        self, message: str, history: list[dict] | None = None
    ) -> AsyncIterator[str]:
        """
        Handles the intent of the message.

        This function takes a message as input and returns the response as a string.

        Parameters:
            message (str): The message to be handled.

        Returns:
            str: The response to the message.
        """
        # if self._intent is None:
        #     raise NotImplementedError("intent is not set")

        # logger.debug(f"Handling public intent: {self._intent}")

        # information = await self.information_retriever.retrieve_public_async(
        #     message, self._intent
        # )
        # prompt_template = self.build_public_prompt_with_information(information)
        # response_generator = ResponseGenerator.with_prompt_template(prompt_template)
        # response = response_generator.response_async(message, [])

        # return response
        if self._intent is None:
            raise NotImplementedError("intent is not set")

        logger.debug(f"Handling public intent: {self._intent}")

        message_with_history = (
            (
                "\n".join([f"{message['U']}\n{message['A']}" for message in history])
                + "\n"
                + message
            )
            if history
            else message
        )

        logger.debug(f"Message with history: {message_with_history}")

        information = await self.information_retriever.retrieve_public_async(
            message_with_history, self._intent
        )
        prompt_template = self.build_prompt_with_information(information)
        response_generator = ResponseGenerator.with_prompt_template(prompt_template)
        response = response_generator.response_async(message, history)

        return response
