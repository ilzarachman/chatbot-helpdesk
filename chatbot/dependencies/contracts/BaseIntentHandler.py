from abc import ABC, abstractmethod
from pydantic import BaseModel

from chatbot.Application import Application


class BaseIntentHandler(ABC):
    """
    Base class for intent handlers. An intent handler is responsible for handling an intent.
    """

    def __init__(self):
        self._application = None

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
