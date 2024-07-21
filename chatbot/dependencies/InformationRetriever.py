from langchain_community.vectorstores import FAISS

from chatbot.config import Configuration
from chatbot.dependencies.IntentClassifier import Intent
from chatbot.dependencies.ModelLoader import ModelLoader
from chatbot.dependencies.contracts.TextEmbedder import TextEmbedder
from chatbot.logger import logger


class InformationRetriever:
    """
    This class is responsible for retrieving information from documents based on the intent of the message.

    This class takes a message as input and returns the relevant information from the documents as a string.

    It should be able to handle multiple documents and retrieve the relevant information from each one based on the
    intent of the message.
    """

    def __init__(self):
        self._embedding_model: TextEmbedder = ModelLoader.load_model(
            Configuration.get("document_embedder.embedding_model")
        )

    def retrieve(self, message: str, intent: Intent) -> str:
        """Retrieve the relevant information from the documents based on the intent of the message.

        This function takes a message as input and returns the relevant information from the documents as a string.

        It should be able to handle multiple documents and retrieve the relevant information from each one based on
        the intent of the message.

        Parameters:
            message (str): The message to retrieve information based on.
            intent (str): The intent of the message.

        Returns:
            str: The relevant information from the documents based on the intent of the message.
        """
        _db = self._embedding_model.load_intent_faiss_index(intent.value)
        _result = self._similarity_search(message, _db, k=5)
        return _result

    @staticmethod
    def _similarity_search(query: str, faiss_index: FAISS, k: int = 3, **kwargs) -> str:
        """
        Handles the similarity search using the FAISS index.

        Parameters:
            query (str): The query to search for.
            faiss_index (FAISS): The FAISS index to search in.
            k (int, optional): The number of results to return. Defaults to 3.

        Returns:
            str: The results of the similarity search.
        """
        try:
            _result = faiss_index.similarity_search_with_relevance_scores(query, k, **kwargs)
            _str = "\n".join([x[0].page_content for x in _result])
            return _str
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            raise Exception(f"Error in similarity search: {e}")

    async def retrieve_async(self, message: str, intent: Intent) -> str:
        """Retrieve the relevant information from the documents based on the intent of the message.

        This function takes a message as input and returns the relevant information from the documents as a string.

        It should be able to handle multiple documents and retrieve the relevant information from each one based on
        the intent of the message.

        Parameters:
            message (str): The message to retrieve information based on.
            intent (str): The intent of the message.

        Returns:
            str: The relevant information from the documents based on the intent of the message.
        """
        _db = self._embedding_model.load_intent_faiss_index(intent.value)
        _result = await self._similarity_search_async(message, _db, k=5)
        return _result

    async def retrieve_public_async(self, message: str, intent: Intent) -> str:
        """Retrieve the relevant information from the documents based on the intent of the message.

        This function takes a message as input and returns the relevant information from the documents as a string.

        It should be able to handle multiple documents and retrieve the relevant information from each one based on
        the intent of the message.

        Parameters:
            message (str): The message to retrieve information based on.
            intent (str): The intent of the message.

        Returns:
            str: The relevant information from the documents based on the intent of the message.
        """
        _db = self._embedding_model.load_public_intent_faiss_index(intent.value)
        _result = await self._similarity_search_async(message, _db, k=5, public=True)
        return _result

    @staticmethod
    async def _similarity_search_async(query: str, faiss_index: FAISS, k: int = 3, **kwargs) -> str:
        """
        Handles the similarity search using the FAISS index.

        Parameters:
            query (str): The query to search for.
            faiss_index (FAISS): The FAISS index to search in.
            k (int, optional): The number of results to return. Defaults to 3.

        Returns:
            str: The results of the similarity search.
        """
        try:
            _result = await faiss_index.asimilarity_search_with_relevance_scores(query, k, **kwargs)
            _str = "\n".join([x[0].page_content for x in _result])
            return _str
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            raise Exception(f"Error in similarity search: {e}")
