from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings as LangChainOpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from ..contracts.TextEmbedder import TextEmbedder
from ...logger import logger


class OpenAIEmbeddings(TextEmbedder):

    def __init__(self, model_name: str = "text-embedding-3-large"):
        """
        Initializes the OpenAIEmbeddings object.

        Args:
            model_name (str): The name of the model to use for embeddings.

        Returns:
            None
        """
        self._model = LangChainOpenAIEmbeddings(model=model_name)

    @property
    def model(self) -> LangChainOpenAIEmbeddings:
        """
        Get the internal model.
        """
        return self._model

    def get_embedding(self, text: str) -> list[float]:
        """
        Embed a text into a vector.

        Args:
            text (str): The text to be embedded.

        Returns:
            Any
        """
        return self._model.embed_query(text)

    def save_to_faiss_index(self, documents: list[Document], faiss_dir: str):
        """
        Save the internal model to FAISS index.

        Args:
            documents (list[Document]): The documents to be indexed.
            faiss_dir (str): The directory to save the FAISS index.

        Returns:
            None

        Raises:
            Exception: Error saving to FAISS index.
        """
        try:
            db: FAISS = FAISS.from_documents(documents, self._model)
            db.save_local(f"{faiss_dir}_db")
        except Exception as e:
            logger.error(f"Error saving to FAISS index: {e}")
