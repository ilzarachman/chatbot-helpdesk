from abc import ABC, abstractmethod


class TextGenerator(ABC):
    """
    Abstract class for text generation.
    """
    @abstractmethod
    def generate(self, text) -> str:
        """
        Generate a text based on the input.

        Parameters:
            text (str): The input text.

        Returns:
            str: The generated text.
        """
        pass

    @abstractmethod
    def stream(self, text) -> str:
        """
        Generate a text stream based on the input.

        Parameters:
            text (str): The input text.

        Returns:
            str: The generated text stream.
        """
        pass