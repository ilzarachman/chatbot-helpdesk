from abc import abstractmethod, ABC
from typing import Optional


class Message(ABC):
    def __init__(self, message: Optional[str]):
        """
        Initializes a new instance of the class.

        Args:
            message (str): The message to be stored in the instance.
        """
        self.message = message

    @abstractmethod
    def get_message(self) -> dict:
        """
        Returns a string representation of the message.

        Returns:
            dict: The string representation of the message.
        """
        pass


class AssistantMessage(Message):

    def get_message(self) -> dict:
        """
        Returns a string representation of the message.

        Returns:
            dict: The string representation of the message.
        """
        return {"role": "assistant", "content": self.message}

    def __str__(self):
        """
        Returns a string representation of the message.

        Returns:
            str: The string representation of the message.
        """
        return self.message


class UserMessage(Message):

    def get_message(self) -> dict:
        """
        Returns a string representation of the message.

        Returns:
            dict: The string representation of the message.
        """
        return {"role": "user", "content": self.message}

    def __str__(self):
        """
        Returns a string representation of the message.

        Returns:
            str: The string representation of the message.
        """
        return self.message


class SystemMessage(Message):

    def get_message(self) -> dict:
        """
        Returns a string representation of the message.

        Returns:
            dict: The string representation of the message.
        """
        return {"role": "system", "content": self.message}

    def __str__(self):
        """
        Returns a string representation of the message.

        Returns:
            str: The string representation of the message.
        """
        return self.message
