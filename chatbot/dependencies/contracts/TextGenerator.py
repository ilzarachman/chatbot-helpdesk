from abc import ABC, abstractmethod
from typing import Generator, Optional

class TextGenerator(ABC):
    """
    Abstract class for text generation.
    """
    @abstractmethod
    def generate(self, prompt: str, config: Optional[dict] = None) -> str:
        """
        Generate a text based on the input.

        Parameters:
            text (str): The input text.
            config (dict, optional): The generation config.

        Returns:
            str: The generated text.
        """
        pass

    @abstractmethod
    def stream(self, prompt: str, config: Optional[dict] = None) -> Generator[str, None, None]:
        """
        Generate a text stream based on the input.

        Parameters:
            text (str): The input text.
            config (dict, optional): The generation config.

        Yields:
            str: The generated text stream.
        """
