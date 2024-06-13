from abc import ABC, abstractmethod

from langchain_core.documents import Document


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

    @property
    @abstractmethod
    def model(self):
        """
        Get the internal model.

        Returns:
            Any
        """
        pass

    @abstractmethod
    def save_to_faiss_index(self, documents: list[Document], faiss_dir: str):
        """
        Save the internal model to FAISS index.

        Parameters:
            documents (list[Document]): The documents to be indexed.
            faiss_dir (str): The directory to save the FAISS index.

        Returns:
            None

        Raises:
            Exception: Error saving to FAISS index.
        """
        pass
