from abc import ABC, abstractmethod


class TextEmbedder(ABC):
    @abstractmethod
    def get_embedding(self, text: str):
        """
        Embed a text into a vector.

        Parameters:
            text (str): The text to be embedded.

        Returns:
            Any
        """
        pass
