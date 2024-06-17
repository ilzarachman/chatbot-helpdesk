from abc import ABC, abstractmethod
from typing import Generator, Optional, Union

from chatbot.dependencies.contracts.message import Message


class TextGenerator(ABC):
    """
    Abstract class for text generation.
    """

    @abstractmethod
    def generate(self, prompt: list[Message], config: Optional[dict] = None) -> str:
        """
        Generate a text based on the input.

        Parameters:
            prompt (str): The input text.
            config (dict, optional): The generation config.

        Returns:
            str: The generated text.
        """
        pass

    @abstractmethod
    async def generate_async(self, prompt: list[Message], config: Optional[dict] = None) -> str:
        """
        Generate a text based on the input.

        Parameters:
            prompt (str): The input text.
            config (dict, optional): The generation config.

        Returns:
            str: The generated text.
        """
        pass

    @abstractmethod
    async def stream_async(self, prompt: list[Message], config: Optional[dict] = None) -> Generator[str, None, None]:
        """
        Generate a text stream based on the input.

        Parameters:
            prompt (str): The input text.
            config (dict, optional): The generation config.

        Yields:
            str: The generated text stream.
        """
        pass

    @abstractmethod
    def stream(self, prompt: list[Message], config: Optional[dict] = None) -> Generator[str, None, None]:
        """
        Generate a text stream based on the input.

        Parameters:
            prompt (str): The input text.
            config (dict, optional): The generation config.

        Yields:
            str: The generated text stream.
        """
        pass
