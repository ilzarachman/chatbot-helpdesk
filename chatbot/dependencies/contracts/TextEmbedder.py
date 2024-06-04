from abc import ABC, abstractmethod


class TextEmbedder(ABC):
    """
    Abstract class for text embedding.

    This class defines the interface for text embedding methods.
    """
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
