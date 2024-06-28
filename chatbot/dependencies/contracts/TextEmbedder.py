from abc import ABC, abstractmethod

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from ..utils.path_utils import project_path
from ...logger import logger


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

    def save_to_faiss_index(self, documents: list[Document], faiss_dir: str):
        """
        Save the internal model to FAISS index.

        Disclaimer: This would override the existing FAISS index.

        Args:
            documents (list[Document]): The documents to be indexed.
            faiss_dir (str): The directory to save the FAISS index.

        Returns:
            None

        Raises:
            Exception: Error saving to FAISS index.
        """
        try:
            db: FAISS = FAISS.from_documents(documents, self.model)
            db.save_local(f"{faiss_dir}")
            logger.debug(
                f"Saved {len(documents)} documents to {faiss_dir} FAISS index."
            )
        except Exception as e:
            logger.error(f"Error saving to FAISS index: {e}")
            raise Exception(f"Error saving to FAISS index: {e}")

    def add_data_to_faiss_index(self, documents: list[Document], faiss_dir: str):
        """
        Add data to existing FAISS index.

        Args:
            documents (list[Document]): The documents to be added to the FAISS index.
            faiss_dir (str): The directory to the FAISS index.

        Returns:
            None

        Raises:
            Exception: Error adding data to FAISS index.
        """
        try:
            db: FAISS = FAISS.load_local(
                f"{faiss_dir}", self.model, allow_dangerous_deserialization=True
            )
            db.add_documents(documents)
            db.save_local(f"{faiss_dir}")
            logger.debug(
                f"Added {len(documents)} documents to {faiss_dir} FAISS index."
            )
        except Exception as e:
            logger.error(f"Error adding data to FAISS index: {e}")
            raise Exception(f"Error adding data to FAISS index: {e}")

    def load_intent_faiss_index(self, intent_value: str) -> FAISS:
        """
        Load the FAISS index for the intent.

        Args:
            intent_value (str): The value of the intent.

        Returns:
            FAISS: The FAISS index for the intent.

        Raises:
            Exception: Error loading the FAISS index.
        """
        try:
            faiss_root_dir = project_path("faiss")
            faiss_intent_dir = faiss_root_dir / intent_value
            return FAISS.load_local(
                f"{faiss_intent_dir}",
                self.model,
                allow_dangerous_deserialization=True,
            )
        except FileNotFoundError:
            logger.error(f"FAISS index for {intent_value} not found.")
            raise FileNotFoundError(f"FAISS index for {intent_value} not found.")
        except Exception as e:
            raise Exception(f"Error loading the FAISS index: {e}")
