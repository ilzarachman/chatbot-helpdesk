from abc import ABC, abstractmethod


class TextGenerator(ABC):
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